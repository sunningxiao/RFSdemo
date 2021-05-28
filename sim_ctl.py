#! /usr/bin/python3
# -*- coding:utf-8 -*-

import numpy as np


def sim_connect():
    return True


def sim_start_unload():
    return True


def sim_stop_unload():
    return True


def sim_format():
    return True


def sim_start_record():
    return True


def sim_stop_record():
    return True


def sim_update_coe():
    return True


def sim_get_filelist():
    return True, [
        [0, 'ID0_20201101_1725_M1_2500Hz_64K.dat', 128 * 1024 ** 2],
        [1, 'ID1_20201101_1725_M1_2500Hz_64K.dat', 20 * 1024 ** 3],
        [2, 'ID2_20201101_1725_M1_2500Hz_64K.dat', 5 * 1024 ** 3]
    ]


i = 0


def sim_update_status():
    global i
    chnl_count = 6
    chnl = np.arange(1, 128, 128 / chnl_count).reshape(chnl_count, 1)
    s_data = np.arange(0, 100, 0.1)
    data = s_data.repeat(chnl_count).reshape(1000, chnl_count, 1)
    data = np.einsum("abc->cba", data).reshape(chnl_count, 1000)
    data = data[..., :] + i
    graph = 128 + chnl * np.sin(data)
    graph = graph.astype('u1')
    state = {'state': 1, 'mode': 1, 'chnl_count': chnl_count, 'left': 1000, 'bandwidth': '3200',
             'round_number': 0, 'fpga_temperature': 0}
    i += 1
    return True, state, [(i % chnl_count) + 1, *graph[i % chnl_count]]

