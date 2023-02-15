import datetime
import os
import struct
import time
import zipfile
from dataclasses import dataclass, field
from typing import List, Dict, Any, TYPE_CHECKING

import numpy as np
from serial.tools import list_ports

from tools.data_unpacking import UnPackage
from tools.get_snr import get_db, get_snr, to_csv
from tools.printLog import *

if TYPE_CHECKING:
    from core import RFSKit


@dataclass
class Record:
    serial_number: str = ''
    """核心板编号"""
    dna: bytes = b''
    """RFSoc DNA"""
    reports: "List[Report]" = field(default_factory=list)
    """各项测试的报告储存类"""
    start_time: datetime.datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    """测试开始时间"""
    end_time: datetime.datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    """测试结束时间"""

    def get_dna(self, rfs_kit: "RFSKit"):
        ...

    def export(self, path):
        """根据reports、

        :param path:
        :return:
        """
        ...


@dataclass
class Report:
    cmd_name: "str" = ''  # 指令
    cmd_result: "bytes" = b''  # 指令返回数据
    cmd_run_right: "bool" = False  # 测试执行结果
    log_data: "List[str]" = field(init=False, default_factory=list)  # log
    serial_data: "List[bytes]" = field(init=False, default_factory=list)  # 串口打印
    result_detail: "List[str]" = field(init=False, default_factory=list)  # 测试结果详情

    def run(self, rfs_kit: "RFSKit"):
        ...

    def result(self):
        ...

    def report(self):
        ...


def append_log(log, serial_data, cmd_name, cmd_result, cmd_run_right):
    log.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}指令名称：{cmd_name}")
    log.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}串口打印：{serial_data}")
    log.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}指令返回数据：{cmd_result}")
    log.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}指令执行结果：{cmd_run_right}")


def scan_coms():
    coms = {}
    for com in list_ports.comports():
        coms[str(com)] = com.device
    return coms


class serial_report(Report):

    def run(self, rfs_kit: "RFSKit"):
        try:
            self.cmd_name = '串口测试，无指令'
            time.sleep(15)
            if len(self.serial_data) != 0:
                self.cmd_run_right = True
            append_log(self.log_data, self.serial_data, self.cmd_name, self.cmd_result, self.cmd_run_right)
        except Exception as e:
            self.log_data.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}:err：{e}")

    def result(self):
        return self.cmd_result

    def report(self):
        return self.log_data


class rf_report(Report):

    def run(self, rfs_kit: "RFSKit"):
        try:
            self.cmd_name = 'RF配置'
            self.cmd_run_right = True
            self.cmd_result = rfs_kit.execute_command(self.cmd_name, need_feedback=True, check_feedback=True)
            if self.cmd_result[0] == '':
                self.cmd_result[2] = struct.unpack('=I', self.cmd_result[2])[0]
                status = self.cmd_result[2]
                if status == 0:
                    self.cmd_run_right = True
                    self.log_data.append("RF配置成功")
                    self.result_detail.append("RF配置成功")
                elif status == 1:
                    self.cmd_run_right = False
                    self.log_data.append("ltc6952状态异常")
                    self.result_detail.append("ltc6952状态异常")
                elif status == 2:
                    self.cmd_run_right = False
                    self.log_data.append("PL_CLOCK未锁定")
                    self.result_detail.append("PL_CLOCK未锁定")
                elif status == 3:
                    self.cmd_run_right = False
                    self.log_data.append("ADC启动失败")
                    self.result_detail.append("ADC启动失败")
                elif status == 4:
                    self.cmd_run_right = False
                    self.log_data.append("DAC启动失败")
                    self.result_detail.append("DAC启动失败")
                elif status == 5:
                    self.cmd_run_right = False
                    self.log_data.append("SYSREF没检测到")
                    self.result_detail.append("SYSREF没检测到")
                elif status == 6:
                    self.cmd_run_right = False
                    self.log_data.append("MTS失败")
                    self.result_detail.append("MTS失败")
            else:
                self.cmd_run_right = False
            append_log(self.log_data, self.serial_data, self.cmd_name, self.cmd_result, self.cmd_run_right)
        except Exception as e:
            self.log_data.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}:err：{e}")

    def result(self):
        return self.cmd_result

    def report(self):
        return self.log_data


class chnl_report(Report):

    def run(self, rfs_kit: "RFSKit"):
        try:
            self.cmd_name = 'AD/DA自测试'
            _pd = 17
            _td = 8
            _data = []

            rfs_kit.start_stream(filepath='_data/', file_name='adda')
            for ch in range(_td):
                rfs_kit.set_param_value(f'dds{ch}脉宽', 500)
                rfs_kit.set_param_value(f'DAC{ch}播放波门宽度', 500 * 1000)
                rfs_kit.set_param_value(f'ADC{ch}采样延迟', 80002000)
                rfs_kit.set_param_value(f'DAC{ch}播放波门延迟', 80000000)
                rfs_kit.set_param_value(f'dds{ch}中心频率', 100)
                rfs_kit.set_param_value(f'dds{ch}频率扫描步进', 500 * 1000)
                rfs_kit.set_param_value(f'dds{ch}频率扫描范围', 8000)
            rfs_kit.set_param_value('基准PRF数量', _pd+3)
            rfs_kit.execute_command('DDS配置')
            self.cmd_result = rfs_kit.execute_command('系统开启')
            time.sleep(3)
            rfs_kit.execute_command('系统停止')
            time.sleep(1)
            rfs_kit.stop_stream()

            # 数据处理-------------->
            with open('_data/data-adda_0.data', 'rb') as fp:
                data: np.ndarray = np.frombuffer(fp.read(), dtype='u4')
            try:
                unpack_data = UnPackage.channel_data_filter(data, list(range(_pd)), list(range(_td)))
            except Exception as e:
                self.cmd_result[2] = (1, 1, 1, 1, 1, 1, 1, 1)
                self.result_detail.append(f'数据不全:{e}')
                raise RuntimeError(f'数据不全,{e}')
            for pd in range(_pd):
                td_list = []
                for td in range(_td):
                    td_list.append(unpack_data[0][pd][td])
                _data.append(td_list)
            _data = np.array(_data)

            # 将结果写入到self.cmd_result[2]中
            # 结果数据说明 0:正确  1:错误  每一个数字代表一组adda的分析结果
            # 结果类型(int,int,int,int,int,int,int,int) 例如(0,0,0,0,0,1,1,1)
            res = []
            snr = []
            for freq in _data:
                _snr, _res = [], []
                for ch in freq:
                    _res.append(get_db(ch, 1))
                    _snr.append(get_snr(data, samplerate=5e9)[0])
                res.append(_res)
                snr.append(_snr)
            snr, res = np.array(snr), np.array(res)
            # band_snr, band_power, band_noise = res[:, :, 0].T, res[:, :, 1].T, res[:, :, 2].T
            np.savetxt(f'_data/band_snr.csv', snr, delimiter=',')
            # np.savetxt(f'_data/band_power.csv', band_power, delimiter=',')
            # np.savetxt(f'_data/band_noise.csv', band_noise, delimiter=',')
            np.savetxt(f'_data/sample_db.csv', res, delimiter=',')
            standard_signal = rfs_kit.icd_param.icd_data.get('standard_signal', None)
            if not standard_signal:
                self.cmd_result[2] = (1, 1, 1, 1, 1, 1, 1, 1)
                self.result_detail.append(f'icd.json中不存在标准带内信号功率')
                raise RuntimeError(f'請聯繫我方，在icd.json中加入標準帶內信號功率')
            standard_signal = np.array(standard_signal)
            compare_res = res.T[:standard_signal.shape[0], :standard_signal.shape[1]]
            self.cmd_result[2] = np.any(standard_signal - compare_res > 2, axis=1)

            if self.cmd_result[0] == '':
                for index, result in enumerate(self.cmd_result[2]):
                    if result == 0:
                        self.log_data.append(f'通道{index}结果正确')
                        self.result_detail.append(f'通道{index}结果正确')
                        self.cmd_run_right = True
                    elif result == 1:
                        self.log_data.append(f'通道{index}结果错误')
                        self.result_detail.append(f'通道{index}结果错误')
                        self.cmd_run_right = False
                # 将处理后结果放入此处加入报告--->
                self.log_data.append(f'处理后结果为:\n'
                                     f'{to_csv(res, "%.9f", ",")}\n\n'
                                     f'{to_csv(snr, "%.9f", ",")}\n\n')
                # <---将处理后结果放入此处加入报告
            else:
                self.cmd_run_right = False
                self.log_data.append(self.cmd_result[0])
            # <--------------数据处理结束
            append_log(self.log_data, self.serial_data, self.cmd_name, self.cmd_result, self.cmd_run_right)
        except Exception as e:
            self.log_data.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}:err：{e}")

    def result(self):
        return self.cmd_result

    def report(self):
        return self.log_data


class ddr_report(Report):

    def run(self, rfs_kit: "RFSKit"):
        try:
            self.cmd_name = 'DDR测试'
            self.cmd_run_right = True
            self.cmd_result = rfs_kit.execute_command(self.cmd_name, need_feedback=True, check_feedback=True)
            if self.cmd_result[0] == '':
                self.cmd_result[2] = struct.unpack('=I', self.cmd_result[2])[0]
                status = self.cmd_result[2]
                if status == 0:
                    self.cmd_run_right = True
                    self.log_data.append("DDR测试成功")
                    self.result_detail.append("DDR测试成功")
                elif status == 1:
                    self.cmd_run_right = False
                    self.log_data.append("DDR初始化失败")
                    self.result_detail.append("DDR初始化失败")
                elif status == 2:
                    self.cmd_run_right = False
                    self.log_data.append("DDR数据读写校验失败")
                    self.result_detail.append("DDR数据读写校验失败")
            else:
                self.cmd_run_right = False
            append_log(self.log_data, self.serial_data, self.cmd_name, self.cmd_result, self.cmd_run_right)
        except Exception as e:
            self.log_data.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}:err：{e}")

    def result(self):
        return self.cmd_result

    def report(self):
        return self.log_data


class gty_report(Report):

    def run(self, rfs_kit: "RFSKit"):
        try:
            self.cmd_name = 'GTY测试'
            self.cmd_run_right = True
            self.cmd_result = rfs_kit.execute_command(self.cmd_name, need_feedback=True, check_feedback=True)
            if self.cmd_result[0] == '':
                self.cmd_result[2] = struct.unpack('=I', self.cmd_result[2])[0]
                status = self.cmd_result[2]
                if status == 0:
                    self.cmd_run_right = True
                    self.log_data.append("GTY测试成功")
                    self.result_detail.append("GTY测试成功")
                elif status == 1:
                    self.cmd_run_right = False
                    self.log_data.append("GTY没有link")
                    self.result_detail.append("GTY没有link")
                elif status == 2:
                    self.cmd_run_right = False
                    self.log_data.append("GTY数据传输校验失败")
                    self.result_detail.append("GTY数据传输校验失败")
            else:
                self.cmd_run_right = False
            append_log(self.log_data, self.serial_data, self.cmd_name, self.cmd_result, self.cmd_run_right)
        except Exception as e:
            self.log_data.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}:err：{e}")

    def result(self):
        return self.cmd_result

    def report(self):
        return self.log_data


class gpio_report(Report):

    def run(self, rfs_kit: "RFSKit"):
        try:
            self.cmd_name = 'GPIO测试'
            self.cmd_run_right = True
            self.cmd_result = rfs_kit.execute_command(self.cmd_name, need_feedback=True, check_feedback=True)
            if self.cmd_result[0] == '':
                self.cmd_result[2] = struct.unpack('=' + 'I' * (len(self.cmd_result[2]) // 4), self.cmd_result[2])
                for index, result in enumerate(self.cmd_result[2]):
                    if result == 0:
                        self.log_data.append(f'GPIO{index},收发均正常')
                        self.result_detail.append(f'GPIO{index},收发均正常')
                    elif result == 1:
                        self.log_data.append(f'GPIO{index},异常')
                        self.result_detail.append(f'GPIO{index},异常')
                        self.cmd_run_right = False
            else:
                self.cmd_run_right = False
            append_log(self.log_data, self.serial_data, self.cmd_name, self.cmd_result, self.cmd_run_right)
        except Exception as e:
            self.log_data.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}:err：{e}")

    def result(self):
        return self.cmd_result

    def report(self):
        return self.log_data


class emmc_report(Report):

    def run(self, rfs_kit: "RFSKit"):
        try:
            self.cmd_name = '固件更新'
            self.cmd_run_right = True
            self.cmd_result = rfs_kit.execute_command(self.cmd_name, need_feedback=True, check_feedback=True,
                                                      file_name='emmc/BOOT-krfs1156gen3_demoV3_autotest.bin', wait=30)
            if self.cmd_result[0] == '':
                self.cmd_result[2] = struct.unpack('=I', self.cmd_result[2])[0]
                status = self.cmd_result[2]
                if status == 0:
                    self.cmd_run_right = True
                    self.log_data.append("固件更新成功")
                    self.result_detail.append("固件更新成功")
                elif status == 1:
                    self.cmd_run_right = False
                    self.log_data.append("固件更新失败")
                    self.result_detail.append("固件更新失败")
            else:
                self.cmd_run_right = False
            append_log(self.log_data, self.serial_data, self.cmd_name, self.cmd_result, self.cmd_run_right)
        except Exception as e:
            self.log_data.append(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}:err：{e}")

    def result(self):
        return self.cmd_result

    def report(self):
        return self.log_data


class test_record(Record):
    rfs_kit = None

    def __init__(self, rfs_kit):
        self.serial_report = serial_report()
        self.rf_report = rf_report()
        self.chnl_report = chnl_report()
        self.ddr_report = ddr_report()
        self.gty_report = gty_report()
        self.gpio_report = gpio_report()
        self.emmc_report = emmc_report()

        self.serial_number = None
        self.rfs_kit = rfs_kit
        self.reports = [self.serial_report, self.rf_report, self.chnl_report, self.ddr_report, self.gty_report,
                        self.gpio_report, self.emmc_report]
        # self.reports = [self.serial_report, self.rf_report, self.chnl_report, self.ddr_report, self.gty_report, self.gpio_report]
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

    def get_dna(self, rfs_kit: "RFSKit"):
        self.dna = rfs_kit.execute_command('DNA查询', need_feedback=True, check_feedback=True)
        if self.dna[0] == '':
            _result = ''
            self.dna = struct.unpack('=III', self.dna[2])
            for result in self.dna:
                _result += (str(result) + ',')
            self.dna = _result
        else:
            self.dna = self.dna[0]

    def export(self, path='export/'):
        with open(f"_data/{self.serial_number}_{self.start_time}----{self.end_time}.txt", 'w', encoding='utf-8') as wf:
            wf.write(f"核心板编号：{self.serial_number}\n")
            wf.write(f"核心板dna：{self.dna}\n")
            wf.write(f"测试开始时间：{self.start_time}\n")
            wf.write(f"测试结束时间：{self.end_time}\n")
            for report in self.reports:
                wf.write(f"\t\t指令名称：{report.cmd_name}\n")
                wf.write(f"\t\t测试返回数据：{report.cmd_result}\n")
                wf.write(f"\t\t测试结果：{report.cmd_run_right}\n")
                wf.write(f"\t\t测试日志----------------------->\n")
                for log in report.log_data:
                    wf.write(f"\t\t\t\t{log}\n")
                wf.write(f"\t\t测试日志<-----------------------\n\n")
        with open(f"_data/{self.serial_number}_{self.start_time}----{self.end_time}_serial_data.txt", 'w',
                  encoding='utf-8') as wf:
            wf.write(f'{self.start_time}\n')
            for report in self.reports:
                for serial_data in report.serial_data:
                    wf.write(serial_data)
            wf.write(f'{self.end_time}')
        filelist = os.listdir('_data/')
        with zipfile.ZipFile(f'{path}{self.serial_number}_{self.start_time}----{self.end_time}.zip', 'w',
                             compression=zipfile.ZIP_STORED) as zip_file:
            for file in filelist:
                with open(f'_data/{file}', "rb") as datafile:
                    zip_file.writestr(f'{file}', datafile.read())
