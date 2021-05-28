from debug_ctl import *
from data_solve import *
import random


class UploadCtl(DebugControl):

    def __init__(self, update_record_status=lambda x: x):
        super(UploadCtl, self).__init__(update_record_status=update_record_status)
        self.processor = DataSolve()
        self.filelist = []  # [[file_id, filename, sample_channel_count, file_size], ...]
        self.current_unload_thread = None

    def get_filelist(self):
        """ 获取文件列表 """
        self.filelist.clear()
        if simulation_ctl:
            size_range = [1024, 1024 * 128]  # MB
            chnl_count_choice = [1, 2, 3, 4, 6]
            for i in range(256):
                chnl_num = random.choice(chnl_count_choice)
                self.filelist.append(
                    [i, f'ID{i}_20201101_1725_M1_2500Hz_64K.dat', chnl_num, random.randint(*size_range)]
                )
        else:
            result = get_files(self.cmd_udp_server)
            assert isinstance(result, list), "get file list fail."

            for info in result:
                file_id = info[2]
                filesize = info[7]  # MB
                sample_channel_count = info[9]
                # year = binascii.a2b_hex(str(info[4]).encode()).decode()
                # md = binascii.a2b_hex(str(info[5]).encode()).decode()
                # hm = binascii.a2b_hex(str(info[6]).encode()).decode()
                year = str(info[4])
                md = str(info[5]).zfill(4)
                hm = str(info[6]).zfill(4)
                filename = f"id{file_id}_{year + md}_{hm}_M{info[8]}_{info[12]}Hz_{info[10]}K.dat"
                self.filelist.append([file_id, filename, sample_channel_count, filesize])
        return True

    def start_unload(self, *args, finally_call=str):
        """ 启动卸载 """
        try:
            if self.current_unload_thread and self.current_unload_thread.is_alive():
                printWarning('working now, try upload later.')
                return False
            # args: sel_files, filepath, de_interleave, label_show
            self.current_unload_thread = threading.Thread(target=self.processor.start_unload,
                                                          args=(self._start_unload, finally_call, *args))
            self.current_unload_thread.start()
            return self.processor.get_state()
        except Exception as e:
            printException(e)
            return False

    @simulation(simulation_ctl, sim_start_unload)
    def _start_unload(self, *args):
        return start_unload(self.cmd_udp_server, *args)

    def stop_unload(self, *args, **kwargs):
        """ 停止卸载 """
        result = self._stop_unload(*args, **kwargs)
        if not result:
            return result
        self.processor.stop_unload(self.current_unload_thread.is_alive())
        while self.current_unload_thread.is_alive():
            pass
        return result

    @simulation(simulation_ctl, sim_stop_unload)
    def _stop_unload(self, *args, **kwargs):
        return stop_unload(self.cmd_udp_server)

    @simulation(simulation_ctl, sim_format)
    def format(self, pthread=None):
        """ 格式化 """
        return data_format(self.cmd_udp_server)
