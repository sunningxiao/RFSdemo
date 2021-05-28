import struct
import time
from utils import *

__all__ = ["connect", "start_record", "stop_record", "get_files", "data_format", "start_unload", "stop_unload",
           "status_echo_data", "filtering_factor_issue", "send_block_size"]

value_type = {
    "uint8": "B",
    "int8": "b",
    "uint16": "H",
    "int16": "h",
    "uint32": "I",
    "int32": "i",
    "float": "f",
    "double": "d"
}

type_size = {
    "uint8": 1,
    "int8": 1,
    "uint16": 2,
    "int16": 2,
    "uint32": 4,
    "int32": 4,
    "float": 4,
    "double": 8
}

feedback_value_fmt = {
    "uint8": "%#x",
    "int8": "%d",
    "uint16": "%#x",
    "int16": "%d",
    "uint32": "%#x",
    "int32": "%d",
    "float": "%f",
    "double": "%f"
}

send_block_size = 1024  # 单次发送或接收大小
recv_block_size = 1024
max_sample_channel_count = 6  # 最大采集通道数
_fmt_mode = "<"  # pack/unpack 大小端模式
_reply_cmd_type = 0x6A
COMMON_MSG = "失败原因未知"

once_file_info_fmt = r"B2IB4I2B3I"
once_file_info_size = 40


@solve_exception()
def connect(conn):
    """
        建立连接
    """
    cmd_type = 0x66
    send_cmd(conn, cmd_type, _cmd_pack(f"4s", b'\x00'))
    fd_len = 4
    status, cause, *_ = cmd_feedback(conn, cmd_type, f"{fd_len}B", fd_len)
    if status:
        return True
    else:
        return {
                0: "数据错误",
                1: "记录仪未启动"
            }.get(cause, COMMON_MSG)


@solve_exception()
def start_record(conn, *args):
    """
        记录启动
    :param conn: netconn.py内类对象
    :param args:
        工作模式、采集通道数、脉冲内采样点数、PRF、预处理使能、[年、月日、时分]
    :return: 指令执行状态
    """

    cmd_type = 0x61
    data = _cmd_pack(r"2BIB4IB", *args[:3], 0, *args[-1], *args[3: 5])
    send_cmd(conn, cmd_type, data, data_sum=sum(args[:-1]) + sum(args[-1]))
    fd_len = 4
    status, cause, *_ = cmd_feedback(conn, cmd_type, f"{fd_len}B", fd_len)
    if status:
        return True
    else:
        return {
                0: "数据错误",
                1: "ssd没准备好",
                2: "存储空间不足",
                3: "文件个数大于500"
            }.get(cause, COMMON_MSG)


@solve_exception()
def stop_record(conn):
    """
        记录停止
    """
    cmd_type = 0x62
    send_cmd(conn, cmd_type, _cmd_pack(r"4s", b'\x00'))
    fd_len = 4
    status, cause, *_ = cmd_feedback(conn, cmd_type, f"{fd_len}B", fd_len)
    if status:
        return True
    else:
        return {
            0: "数据错误",
            1: "无法停止"
            }.get(cause, COMMON_MSG)


@solve_exception(True)
def get_files(conn):
    """
        获取文件列表
    """
    cmd_type = 0x63
    file_bytes = b""
    file_cnt = 0
    while True:
        send_cmd(conn, cmd_type, _cmd_pack(r"4s", b'\x00'))

        tail, _file_cnt, _file_bytes = _get_file(conn, cmd_type)
        file_bytes += _file_bytes
        file_cnt += _file_cnt
        if tail:
            break

    file_list = []
    for i in range(file_cnt):
        _d = _cmd_unpack(once_file_info_fmt, file_bytes[once_file_info_size * i: once_file_info_size * (i + 1)])
        file_list.append(_d)
    return file_list


def _get_file(conn, cmd_type):
    cmd_len, rcvd, data_sum = cmd_feedback(conn, cmd_type, flag=True)
    data_sum += sum(rcvd[: -1])
    assert data_sum & 0xff == rcvd[-1], "接收反馈校验错误"
    tail_flag, file_cnt = _cmd_unpack(r'BI', rcvd[:5])
    file_list_info = rcvd[5:]  # 文件列表数据
    return tail_flag, file_cnt, file_list_info[: file_cnt * once_file_info_size]


@solve_exception()
def data_format(conn):
    """
        格式化
    """
    cmd_type = 0x64
    send_cmd(conn, cmd_type, _cmd_pack(r"4s", b'\x00'))
    fd_len = 4
    try:
        conn.settimeout(None)  # 阻塞、等待反馈
        status, cause, *_ = cmd_feedback(conn, cmd_type, f"{fd_len}B", fd_len)
    except Exception as e:
        assert 0, e
    finally:
        conn.settimeout()
    if status:
        return True
    else:
        return {
            0: "数据错误",
            1: "正在记录中"
            }.get(cause, COMMON_MSG)


@solve_exception()
def filtering_factor_issue(conn, count, gen_data):
    """
        匹配滤波因子下发
        先发送包头 (0x5A5A5A5A, 16, 0x45, count),
        再以send_block_size大小循环发送
    :param conn: netconn.py内类对象
    :param count: 匹配滤波因子数量
    :param gen_data: 匹配滤波因子数据生成器
    :return:
    """
    cmd_type = 0x65
    # 发送包头
    data_sum = send_cmd(conn, cmd_type, _cmd_pack(r"I", count), tail=False, exclude_len=count * 2 * 4 + 1)
    # 发送数据
    for data in gen_data:
        length = len(data)
        sent, data_sum = _send_cmd(conn, rf"{length}f", *data, data_sum=data_sum, tail=False)
        if length * 4 != sent:
            gen_data.send(True)
            assert 0, "滤波因子数据发送丢失"
    sent, _ = _send_cmd(conn, r"B", data_sum & 0xff, tail=False)
    assert sent == 1, "滤波因子数据发送丢失(tail)"
    fd_len = 4
    status, cause, *_ = cmd_feedback(conn, cmd_type, f"{fd_len}B", fd_len)
    if status:
        return True
    else:
        return {
            0: "数据错误",
            1: "自定义"
            }.get(cause, COMMON_MSG)


@solve_exception(True)
def start_unload(conn, *args):
    """
        启动卸载
        arg: 文件个数(1)、文件起始位置偏移、文件卸载大小、文件编号
    """
    cmd_type = 0x51
    send_cmd(conn, cmd_type, _cmd_pack(rf"{len(args)}I", *args))
    fd_len = 4
    status, *_ = cmd_feedback(conn, cmd_type, f"{fd_len}B", fd_len)
    return status


@solve_exception(True)
def stop_unload(conn):
    """
        停止卸载
    """
    cmd_type = 0x52
    send_cmd(conn, cmd_type, _cmd_pack(r"5s", b'\x00'))
    fd_len = 4
    status, *_ = cmd_feedback(conn, cmd_type, f"{fd_len}B", fd_len)
    return status


@solve_exception(True)
def status_echo_data(conn):
    """
        状态或回波数据获取
    """
    cmd_type, result, *_ = cmd_feedback(conn, 0, cmd_type_function={
        0x70: status_data,
        0x71: echo_data
    }, ignore=True)
    return cmd_type == 0x70, result


def status_data():
    """
        状态数据获取
    """
    t_cmd_length = 10  # 除回波数据外的长度, 4Byte
    return 0x70, rf"{t_cmd_length}IB", t_cmd_length * 4 + 1


def echo_data():
    """
        回波数据获取
    """
    echo_data_len = 1000  # uint8
    return 0x71, rf"{echo_data_len + 1 + 1}B", echo_data_len + 1 + 1


def send_cmd(conn, cmd_type, cmd_content=b"", data_sum=0, tail=True, exclude_len=0):
    # exclude_len: 发送包不包含的数据长度, 一般和tail同时存在 (tail=False, exclude_len != 0)
    head = 0x5A5A5A5A
    origin_number = 0x05
    target_num = 0x24
    cmd_len = 15 + len(cmd_content) + exclude_len
    if tail:
        cmd_len += 1
    sent, data_sum = _send_cmd(conn, r"3I3B", head, cmd_len, conn.get_number(), origin_number, target_num, cmd_type,
                               cmd_content=cmd_content, data_sum=data_sum, tail=tail)
    if exclude_len != 0:
        return data_sum
    assert sent == cmd_len, f"指令发送失败, 指令总长: {cmd_len}, 发送: {sent}"


def _send_cmd(conn, fmt, *args, cmd_content=b"", data_sum=0, tail=True):
    # 返回发送数据量
    cmd_data = _cmd_pack(fmt, *args) + cmd_content
    data_sum += sum(cmd_data)
    if tail:
        check_number = _cmd_pack("B", data_sum & 0xff)
    else:
        check_number = b""
    cmd_data += check_number
    total_size = len(cmd_data)
    sent = 0
    once_send = send_block_size
    stime = time.time()
    while once_send:
        assert time.time() - stime < 2, "发送超时(2s)"
        sent += conn.send(cmd_data[sent: sent + once_send])
        left_size = total_size - sent
        if left_size < once_send:
            once_send = left_size
    return sent, data_sum


def cmd_feedback(conn, cmd_type, fd_fmt="", fd_fmt_len=0, tail=True, flag=False, ignore=False, cmd_type_function: dict=None):
    # flag：截取接收; ignore: 忽略校验应答指令类型
    rcvd = _cmd_feedback(conn)
    head, = _cmd_unpack('I', rcvd[:4])
    assert head == 0x5B5B5B5B, "Fail to receive the data"
    cmd_len, = _cmd_unpack('I', rcvd[4: 8])
    if not flag:
        assert cmd_len == len(rcvd), f"udp接收数据丢包, length {cmd_len} rcvd {len(rcvd)}"

    # (serial_number, ), cmd_data = _cmd_unpack("I", rcvd[8: 12]), rcvd[12:]
    cmd_data = rcvd[12:]
    if ignore:
        offset = 3
        result = _cmd_unpack(f'{offset}B', cmd_data[:offset])
        origin_number, target_num, f_cmd_type = result
    else:
        offset = 4
        result = _cmd_unpack(f'{offset}B', cmd_data[:offset])
        origin_number, target_num, reply_cmd_type, f_cmd_type = result
        assert reply_cmd_type == _reply_cmd_type, f"应答指令类型不匹配({reply_cmd_type:X})"

    if cmd_type_function and isinstance(cmd_type_function, dict) and cmd_type_function.get(f_cmd_type):
        cmd_type, fd_fmt, fd_fmt_len = cmd_type_function[f_cmd_type]()
        return_cmd_type = True
    else:
        return_cmd_type = False

    assert f_cmd_type == cmd_type, f"指令类型不匹配(发送指令类型: {cmd_type:X}, 接收指令类型: {f_cmd_type:X})"

    data_sum = sum(rcvd[:12 + offset])
    if flag:
        return cmd_len - (12 + offset), cmd_data[offset:], data_sum

    result = _cmd_unpack(fd_fmt, cmd_data[offset: offset + fd_fmt_len])
    if tail:
        *result, check_number = result
        assert (data_sum + sum(cmd_data[offset: offset + fd_fmt_len - 1])) & 0xff == check_number, "接收反馈校验错误"
    left_fd_data = cmd_data[offset + fd_fmt_len:]

    if left_fd_data:
        if return_cmd_type:
            return cmd_type, result, left_fd_data
        return result, left_fd_data
    if return_cmd_type:
        return cmd_type, result
    return result


def _cmd_feedback(conn, block_size=recv_block_size):
    return conn.recv(block_size)


def _cmd_pack(fmt, *args) -> bytes:
    return struct.pack(_fmt_mode + fmt, *args)


def _cmd_unpack(fmt, data) -> tuple:
    return struct.unpack(_fmt_mode + fmt, data)
