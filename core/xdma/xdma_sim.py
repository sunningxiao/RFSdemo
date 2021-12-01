# -*- coding:utf-8 -*-
############################
# PSCN SIMULATION
# Writer: tony
# Date: Jan. 3, 2019
############################
import platform
from tools.printLog import *
import numpy as np
import random

PCIESTREAMCNT = 1


class Xdma(object):

    isWindows = platform.system() == "Windows"

    def __init__(self):
        self.sd_dict = {}
        self.board_info = ""
        self.board_set = set()

        self.reg = {}
        printInfo("xdma模拟初始化")

    def open_board(self, board):
        return True

    def get_fpga_version(self, board=0):
        return 0

    def close_board(self, board):
        return True

    def get_info(self, board=0):
        return ""

    # 申请内存
    def alloc_buffer(self, board, length):
        return 1

    # 获取内存
    @staticmethod
    def get_buffer(fd, length):
        # data = np.random.rand(length//2)
        # data.dtype = np.uint32
        data = np.arange(length, dtype='u4')
        return data

    def free_buffer(self, fd):
        return True

    def alite_write(self, addr, data, board=0):
        self.reg[addr] = data
        printDebug("板卡%x, 接收写寄存器，地址：%x, 值：%x" % (board, addr, data))
        return True

    def alite_read(self, addr, board=0):
        try:
            val = self.reg[addr]
        except:
            val = random.randint(0, 10)
        printDebug("板卡%x, 接收读寄存器，地址：%x, 返回值：%x" % (board, addr, val))
        return True, val

    def reset_board(self, board):
        printDebug("接收到板卡%x复位" % board)
        return True

    def stream_write(self, board, chnl, fd, length, offset=0, stop_event=None, flag=1):
        # printInfo("板卡%x, 接收到数据流下行指令，通道号：%d，数据量：%d" % (board, chnl, length))
        return True

    def stream_read(self, board, chnl, fd, length, offset=0, stop_event=None, flag=1):
        return True
