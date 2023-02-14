import numpy as np

from tools.data_unpacking import UnPackage
from tools.get_snr import get_db

_pd = 17
_td = 8
_data = []

with open(r"C:\Users\56585\Downloads\data-adda_0.data", 'rb') as fp:
    data: np.ndarray = np.frombuffer(fp.read(), dtype='u4')

unpack_data = UnPackage.channel_data_filter(data, list(range(_pd)), list(range(_td)))

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
for freq in _data:
    _res = []
    for ch in freq:
        _res.append(get_db(ch, 1))
    res.append(_res)
res = np.array(res)

standard_signal = [
    [85.63706486, 84.33821298, 84.83262966, 83.47855133, 83.44610464, 83.37962213, 82.89502035, 82.19603298, 80.82963684, 80.26125352],
    [85.61519498, 84.20103289, 84.63488179, 83.5696279, 82.87449181, 82.61534764, 81.74295387, 81.03813991, 79.70705928, 76.95028126],
    [85.58159715, 84.27269676, 84.81891785, 83.40011916, 83.57374956, 83.56959438, 83.0860739, 82.65826351, 81.26920941, 80.69755561],
    [85.56760136, 84.14091691, 84.62752148, 83.52664871, 82.99606922, 82.85297491, 82.34746259, 81.89226611, 80.93809342, 79.32566772],
    [85.60071587, 84.2831173, 84.82961334, 83.49429634, 83.66303899, 83.38622477, 82.75366184, 81.91619546, 80.16657407, 80.05354637],
    [85.65811612, 84.29051687, 84.79589116, 83.82286485, 83.39031481, 83.35730717, 82.76315077, 82.09714449, 81.39459286, 80.7136994],
    [85.60657198, 84.31656786, 84.84655036, 83.67313114, 83.77819468, 83.55961011, 83.09160653, 82.41122009, 80.53709699, 80.56000723],
    [85.60557799, 84.31915151, 84.73248253, 83.92962919, 83.52650684, 83.46233988, 83.02037595, 82.5844581, 81.68596529, 80.12961759]
]
standard_signal = np.array(standard_signal)
compare_res = res.T[:standard_signal.shape[0], :standard_signal.shape[1]]
