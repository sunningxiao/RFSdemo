import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, TYPE_CHECKING
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
    start_time: datetime.datetime = datetime.datetime.now()
    """测试开始时间"""
    end_time: datetime.datetime = datetime.datetime.now()
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
    cmd_name: "str" = ''
    cmd_result: "bytes" = b''
    cmd_run_right: "bool" = True
    log_data: "List[str]" = field(init=False, default_factory=list)
    serial_data: "List[bytes]" = field(init=False, default_factory=list)

    def run(self, rfs_kit: "RFSKit"):
        ...

    def result(self):
        ...

    def show_result(self, widget):
        ...

    def report(self):
        ...
