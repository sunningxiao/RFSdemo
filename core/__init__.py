from typing import Union, IO, List
from _io import BufferedReader
from itertools import product
import numpy as np

from core import config
# from core.data_solve import DataSolve
# from core import interface
# from core.icd_parser import ICDParams

from tools.data_unpacking import UnPackage
from tools.utils import SingletonType, APIBaseType

__all__ = ['RFSCore']


class __RFSAPICore(APIBaseType, SingletonType):
    _METHODS = frozenset({
        "execute_socket_command", "set_param_value", "get_param_value",
        "append_dma_data", "view_dma_data", "get_dma_data",
    })
    _ATTRS = {}


class RFSCore(metaclass=__RFSAPICore, _root=True):
    def __init__(self):
        # self.icd_param = ICDParams()
        # self.data_interface = interface.XdmaInterface()
        # self.cmd_interface = interface.CommandTCPInterface()
        # self.data_solve = DataSolve(self.data_interface)
        pass

    def channel_data_filter(self, _data: Union[BufferedReader, List[BufferedReader], bytes, np.ndarray],
                            frame_idx: List[int], chnl_idx: List[int]):
        if isinstance(_data, (BufferedReader, list)):
            return self.__filter_from_file(_data, frame_idx, chnl_idx)

        if isinstance(_data, bytes):
            _data = np.frombuffer(_data, dtype='u4')
        return self.__filter_from_array(_data, frame_idx, chnl_idx)

    @staticmethod
    def __read_file(fp: BufferedReader, offset=0, length=0):
        fp.seek(offset)
        data = fp.read(length)
        fp.seek(0)
        return data

    def __filter_from_file(self, _fp: Union[BufferedReader, List[BufferedReader]],
                           frame_idx: List[int], chnl_idx: List[int]):
        if isinstance(_fp, BufferedReader):
            _fp = [_fp]
        _head = np.frombuffer(_fp[0].read(256), dtype='u4')
        _fp[0].seek(0)

        (pack_length, mode, data_length, head_length, data_dtype, width,
         bit_con_byte, chnl_count, include_tail, is_complex) = UnPackage.get_pack_info(False, _head, None)

        frame_length = pack_length*chnl_count

        frames = {fp: {idx: self.__read_file(fp, idx*frame_length, frame_length) for idx in frame_idx} for fp in _fp}

        for fp, idx in product(_fp, frame_idx):
            _data = np.frombuffer(frames[fp][idx], dtype='u4')
            _, (__, _data) = UnPackage.common_solve_data(_data, qv_length=pack_length, head_tag=0x18EFDC01)
            frames[fp][idx] = {chnl_id: _data[chnl_id] for chnl_id in chnl_idx}

        return frames

    def __filter_from_array(self, _data: np.ndarray, frame_idx: List[int], chnl_idx: List[int]):
        if len(_data.shape) == 1:
            _data = _data.reshape(1, _data.size)
        _head = _data[0, :64]

        (pack_length, mode, data_length, head_length, data_dtype, width,
         bit_con_byte, chnl_count, include_tail, is_complex) = UnPackage.get_pack_info(False, _head, None)

        frame_length = (pack_length * chnl_count)//4

        frames = {index: {idx: data[idx*frame_length: (idx+1)*frame_length] for idx in frame_idx}
                  for index, data in enumerate(_data)}

        for (index, data), idx in product(enumerate(_data), frame_idx):
            _data = frames[index][idx]
            _, (__, _data) = UnPackage.common_solve_data(_data, qv_length=pack_length, head_tag=0x18EFDC01)
            frames[index][idx] = {chnl_id: _data[chnl_id] for chnl_id in chnl_idx}

        return frames
