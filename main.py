import time
from xmlrpc.client import ServerProxy
from NS_MCI import RFSKit
from typing import Union
from rpcserver import RFSKitRPCServer
import numpy as np

a: Union[RFSKitRPCServer, RFSKit] = ServerProxy('http://192.168.1.194:10801', use_builtin_types=True)
a.start_command()
a.execute_command('初始化')
a.execute_command('DAC配置')
a.execute_command('ADC配置')
# a.clear_ad_cache()
a.set_param_value('基准PRF周期', 10000000)
a.init_dma()
print(a.get_param_value('基准PRF周期'))
a.execute_command('内部PRF产生')
# time.sleep(2)
b = a.get_adc_data(0, False)
c = np.frombuffer(b[0], dtype=b[1])
c = c.reshape(b[2])
