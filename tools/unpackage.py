import numpy as np
from printLog import *

QvLength = 1024


class UnPackage:
    data_bit = 4
    head_length = [256, 32]  # Byte
    _sql_data_type_relate = {
        0: [np.uint16, 16, False],
        1: [np.int16, 16, False],
        2: [np.uint8, 8, False],
        3: [np.int8, 8, False],
        4: [np.uint32, 32, False],
        5: [np.int32, 32, False],
        6: [np.uint32, 32, True]  # complex类型, IQ int16组合
    }
    _common_data_type_relate = {
        4: [np.uint16, 16, False],
        5: [np.int16, 16, False],
        2: [np.uint8, 8, False],
        3: [np.int8, 8, False],
        0: [np.uint32, 32, False],
        1: [np.int32, 32, False],
        6: [np.uint32, 32, True]  # complex类型, IQ int16组合
    }

    def __init__(self):
        pass

    @classmethod
    def solve_source_data(cls, data, channel_chart_show_status: iter, *args, file_callback_function=None, task_parser=False, step=0, for_save=False):
        """
        :param channel_info: 通道模型类对象.get_dict()
        :param data: 解析数据
        :param channel_chart_show_status: 通道显示状态
        :param args:
        :param file_callback_function: 文件快视回调方法
        :param task_parser: 任务数据解析
        :param step: 抽取间隔
        :return:
        """

        try:
            result_data = {}
            filename = None
            chnl_position = None
            chnl_value_bit = 2
            pack_info = None
            qv_length = QvLength  # 快视数据截取长度
            pack_mode = False
            first_num = 0

            head_info = cls.get_head_info(first_num, pack_mode, data, pack_info, chnl_position, chnl_value_bit)
            assert head_info is not None, "没有匹配的包头格式"
            head_index, head_list, head_list_length = head_info

            data = data[head_index:]

            pack_length, mode, data_length, head_length, data_dtype, width, bit_con_byte, chnl_count, include_tail, is_complex = cls.get_pack_info(pack_mode, data, pack_info)

            if file_callback_function is not None:
                pack_num = cls.get_pack_num(pack_mode, data, pack_info)
                if mode != 2:
                    total_pack_length = pack_length // 4 * chnl_count  # 4Byte
                else:
                    total_pack_length = pack_length
                result = file_callback_function(total_pack_length, head_index, pack_num, *args)
                if not isinstance(result, tuple):
                    assert result, "未匹配到指定包号"
                filename, data = result
                if not (data[: head_list_length] == head_list).all():
                    assert 0, "任务数据异常"

                cut_length = data_length
            elif task_parser:
                return head_index, pack_length, chnl_count, mode, data_dtype, width, bit_con_byte, head_length, data_length, include_tail
            else:
                if for_save:
                    cut_length = data_length
                else:
                    cut_length = qv_length * bit_con_byte  # 截取长度单位为数据位宽

            # head_data uint32, data 数据位宽决定
            head_data, data = cls.unpack_data(mode, data, pack_length, chnl_count, data_dtype, width, bit_con_byte, cut_length, head_length, data_length, step, is_complex)

            cls.__build_result(head_data, data, channel_chart_show_status, result_data, mode, *[pack_info, chnl_count, pack_mode, chnl_position, chnl_value_bit, is_complex])
            return result_data
        except AssertionError as e:
            if file_callback_function is not None or task_parser:
                return f"{e}"
            # print(e)
            return {}
        except Exception as e:
            printException(e)
            if file_callback_function is not None or task_parser:
                return f"{e}"
            return {}

    @classmethod
    def __build_result(cls, head_data, data, channel_chart_show_status, result_data, mode, *args):
        pack_info, chnl_count, pack_mode, chnl_position, chnl_value_bit, is_complex = args
        result_data["head"] = head_list = []
        for index, d in enumerate(data):
            if not channel_chart_show_status[index]:
                continue
            head_dict = {}
            head_list.append(head_dict)
            # if filename:
            #     temp_dict["filename"] = filename
            channel_name = 'chl'
            if mode != 2:
                sub_head_data = head_data[index]
                channel_num = int(
                    0 if chnl_count == 1 else cls.get_chnl_number(pack_mode, sub_head_data, chnl_position, chnl_value_bit))
            else:
                sub_head_data = head_data
                channel_num = index
            head_dict["name"] = name = f"{channel_name}_{channel_num}"
            head_dict["pkgcnt"] = int(cls.get_pack_num(pack_mode, sub_head_data, pack_info))
            head_dict["data"] = sub_head_data

            if isinstance(channel_chart_show_status, dict):
                # chart推送
                temp_channel_show = channel_chart_show_status.get(name)
                if temp_channel_show is not None:
                    channel_show_mode = temp_channel_show
                    if temp_channel_show == 2:
                        channel_chart_show_status.update({name: 0})  # 将状态至为0
                else:
                    channel_show_mode = 0
            else:
                # 文件快视
                try:
                    channel_show_mode = channel_chart_show_status[index]
                except:
                    channel_show_mode = 0

            head_dict["show"] = True if channel_show_mode == 1 else False
            result_data[f"chl_{index}"] = d
            # if channel_show_mode:
            #     result = Custom.solve_chart_data(d, channel_info["chnl"], channel_show_mode, is_complex)
            #     if result:
            #         chart_name, chart_data = result
            #         try:
            #             chart_num_list = result_data[chart_name]
            #         except:
            #             result_data[chart_name] = chart_num_list = []
            #         for sub_num, sub_data in enumerate(chart_data):
            #             sub_data_dict = {}
            #             chart_num_list.append(sub_data_dict)
            #             sub_data_dict["name"] = name
            #             sub_data_dict["type"] = "line"
            #             sub_data_dict["xAxisIndex"] = sub_num
            #             sub_data_dict["yAxisIndex"] = sub_num
            #             sub_data_dict["data"] = sub_data

    @classmethod
    def get_head_info(cls, first_num, pack_mode, data, pack_info, *args):
        # 解析头部信息
        if pack_mode:
            head_list = [int(i, 16) for i in pack_info["headword"].split("-")]
        else:
            head_list = [0x18EFDC01]
        head_list_length = len(head_list)
        max_head_value = max(head_list)
        max_head_index = head_list.index(max_head_value)

        head_indexes = np.where(data == max_head_value)[0]
        for index in head_indexes:
            if head_list_length != 1:
                head_index = index - max_head_index
                check_data = data[head_index: index + (head_list_length - max_head_index)]
                if not (check_data == head_list).all():
                    continue
            else:
                head_index = index

            chnl_num = cls.get_chnl_number(pack_mode, data, *args, head_index)
            if chnl_num == first_num:
                return head_index, head_list, head_list_length
        else:
            return None  # 没有匹配的包头格式

    @classmethod
    def get_chnl_number(cls, pack_mode, data, chnl_position, chnl_value_bit, index=0):
        if pack_mode:
            start_index = index + chnl_position // cls.data_bit

            chnl_num = cls.get_index_data(data, start_index, chnl_position, chnl_value_bit)
        else:
            chnl_num = data[index + 4] >> 16 & 0xffff
        return chnl_num

    @classmethod
    def get_pack_num(cls, pack_mode, data, pack_info=None):
        if pack_mode:
            pack_num_index = pack_info["packnum"]
            pack_num = data[pack_num_index // cls.data_bit]
        else:
            pack_num = data[1]
        return pack_num

    @classmethod
    def get_pack_info(cls, pack_mode, data, pack_info=None):
        """
        pack_length, mode, data_length, head_length, data_dtype, width, bit_con_byte, chnl_count, include_tail, is_complex
        pack_length: 包长, 包含包头与包尾
        mode: 0: 交织打包, 1: 数据段打包, 2: 单包头交织打包
        data_length: 数据长度
        data_dtype: 数据类型
        width: 交织力度, 仅交织打包模式下有效
        bit_con_byte: 字节数
        chnl_count: 通道数
        include_tail: 是否包含包尾
        is_complex: 是否是复数类型
        """
        if pack_mode:
            pack_length_site = pack_info["packlength"]
            pack_length_bit = pack_info["packlengthbit"]
            start_index = pack_length_site // cls.data_bit
            pack_length = cls.get_index_data(data, start_index, pack_length_site, pack_length_bit)
            pack_length_unit = pack_info["packlengthunit"]
            pack_length *= pack_length_unit
            chnl_count = pack_info["count"]
            mode = pack_info["mode"]
            include_tail = pack_info["tail"]
            head_length = pack_info["headlength"]
            data_type = pack_info["bit"]  # 数据类型
            width = pack_info["width"]  # 交织力度 Byte
            lengthmode = pack_info["lengthmode"]
            data_dtype, bit, is_complex = cls._sql_data_type_relate.get(data_type, [np.uint32, 32, False])

        else:
            pack_length = data[2]
            mode_info = data[3] & 0xff
            if mode_info >> 4 & 1:
                mode = 2  # 单包头交织打包
            else:
                mode = mode_info & 1  # 0: 交织打包; 1: 数据段打包;
            include_tail = mode_info >> 1 & 1
            if mode_info >> 3 & 1:  # 使能超长包头
                head_length = 512
            else:
                head_length = cls.head_length[mode_info >> 2 & 1]
            # bit = data[3] >> 8 & 0xff
            width = data[3] >> 16 & 0xffff
            chnl_count = data[4] & 0xffff
            data_type = data[6] & 0xff
            lengthmode = True
            data_dtype, bit, is_complex = cls._common_data_type_relate.get(data_type, [np.uint32, 32, False])

        bit_con_byte = bit // 8
        assert not width % bit_con_byte, "交织力度*8不能整除数据位宽"

        if lengthmode:
            if include_tail:
                data_length = pack_length - head_length * 2
            else:
                data_length = pack_length - head_length
        else:
            # 长度不包含包头
            data_length = pack_length
            if include_tail:
                pack_length += head_length * 2
            else:
                pack_length += head_length
        if mode == 2:
            data_length = (data_length - data_length % chnl_count) // chnl_count  # 去掉不能整除的部分
        return pack_length, mode, data_length, head_length, data_dtype, width, bit_con_byte, chnl_count, include_tail, is_complex

    @classmethod
    def get_index_data(cls, data, start_index, total_size, total_bit):
        left_bit = total_size % cls.data_bit
        if cls.data_bit - left_bit < total_bit / 8:
            current_pack_length_bit = (cls.data_bit - left_bit) * 8
            next_pack_length_bit = total_bit - current_pack_length_bit
        else:
            current_pack_length_bit = total_bit
            next_pack_length_bit = 0
        if left_bit:
            result = data[start_index] >> (left_bit * 8) & (2 ** current_pack_length_bit - 1)
        else:
            result = data[start_index] & (2 ** current_pack_length_bit - 1)
        if next_pack_length_bit:
            result = (result << next_pack_length_bit) + (data[start_index + 1] & (2 ** next_pack_length_bit - 1))
        return result

    @classmethod
    def unpack_data(cls, mode, data, pack_length, chnl_count, data_dtype, width, bit_con_byte, cut_length, head_length, data_length, step, is_complex):
        temp_head_length = head_length // bit_con_byte
        temp_pack_length = pack_length // bit_con_byte
        data_length //= bit_con_byte
        cut_length //= bit_con_byte
        head_length //= cls.data_bit
        pack_length //= cls.data_bit

        # step: -1包长等间隔采样
        if step == -1:
            step = data_length // cut_length
        else:
            step += 1
        total_cut_length = (cut_length - 1) * step + 1  # 总长 = (截图长度 - 1) * step + 1  , 起始为0
        if total_cut_length > data_length:
            total_cut_length = data_length
        width_count = width // bit_con_byte  # 基于数据位宽的交织数
        if mode == 1:
            # 数据段打包
            ceil_total_cut_length = total_cut_length
        else:
            # 截取长度向上取交织力度的整倍数
            remainder = total_cut_length % width_count  # 取余
            ceil_total_cut_length = total_cut_length + width_count - remainder if remainder else total_cut_length

        step_index = range(0, total_cut_length, step)  # 取索引
        # 0: 交织打包, 1: 数据段打包, 2: 单包头交织
        data = data[: pack_length * chnl_count]
        if mode == 2:
            head_data = data[: head_length]
            data = data[head_length:]
            data.dtype = data_dtype
            solve_data = data[: ceil_total_cut_length * chnl_count]  # 获取要截取的包长
            assert len(solve_data) >= ceil_total_cut_length * chnl_count, "匹配的数据长度 < 单采集通道截取长度 * 采集通道数"
            data = solve_data.reshape(ceil_total_cut_length // width_count, chnl_count, width_count)
            data = np.einsum("abc->bac", data).reshape(chnl_count, ceil_total_cut_length)
        else:
            if mode:
                assert len(data) >= pack_length * chnl_count, "匹配的包数据长度 < 包长 * 采集通道数"
                head_data = data.reshape(chnl_count, pack_length)[..., : head_length]
                data.dtype = data_dtype
                data = data[: temp_pack_length * chnl_count].reshape(chnl_count, temp_pack_length)
                data = data[..., temp_head_length: ceil_total_cut_length + temp_head_length]
            else:
                head_data = data[: head_length * chnl_count].reshape(head_length // (width // 4), chnl_count, width // 4)
                head_data = np.einsum("abc->bac", head_data).reshape(chnl_count, head_length)
                data.dtype = data_dtype
                solve_data = data[temp_head_length * chnl_count: (ceil_total_cut_length + temp_head_length) * chnl_count]
                assert len(solve_data) >= ceil_total_cut_length * chnl_count, "匹配的包数据长度 < (截取长度 + 包头长度) * 采集通道数"
                data = solve_data.reshape(ceil_total_cut_length // width_count, chnl_count, width_count)
                data = np.einsum("abc->bac", data).reshape(chnl_count, ceil_total_cut_length)

        data = data[..., step_index].astype("i8")
        # if is_complex:
        #     data = cls.unpack_complex(data)
        return head_data.tolist(), data

    # @classmethod
    # def unpack_complex(cls, data):
    #     data = np.array(Custom.unpack_complex(data))
    #     return np.einsum("abc->bac", data)


if __name__ == '__main__':
    with open('D://test_0.data', 'rb') as fp:
        data = fp.read(526336-4)

    data_ = np.frombuffer(data, dtype='u4')
    datas = UnPackage.solve_source_data(data_, [False, True, True, False, True, True, True, True])
    info = UnPackage.get_pack_info(False, data_[:64])
    print(datas)
