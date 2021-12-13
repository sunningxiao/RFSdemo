from core import RFSKit
from core.interface import CommandSerialInterface, DataTCPInterface


# 实例化
rfs_kit = RFSKit(auto_write_file=False,                 # 是否开启自动写盘，关闭后可使用get_stream_data方法获取数据，默认开启
                 cmd_interface=CommandSerialInterface,  # 指定使用的指令interface  默认CommandTCPInterface
                 data_interface=DataTCPInterface)       # 指定使用的数据流interface默认DataTCPInterface

# 指令下发
# 指令下发初始化
rfs_kit.start_command('COM10', 115200)
# 获取参数
dac_sample = rfs_kit.get_param_value('DAC采样率')
dac_insert = rfs_kit.get_param_value('DAC 抽取倍数')
# 修改参数
rfs_kit.set_param_value('DDS采样率', dac_sample/dac_insert)
# 指令下发
rfs_kit.execute_command('DDS配置', callback=lambda: print('下发成功'))

# 数据上行
# 开启数据流上下行
rfs_kit.start_stream()
# 获取数据
data = rfs_kit.get_stream_data()
# 数据快视, 不影响数据流的获取一包数据
view_data = rfs_kit.view_stream_data()
