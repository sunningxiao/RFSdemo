## RFS_demo

* 打包方法

  `pyinstaller --add-binary='.\core\xdma\xdma_api.dll;./core/xdma' -Fw main.py`

* 环境安装
  
  `pip install -r requirements.txt`

## 变更记录
### v2
* UI界面修改与搭建
### v3
* 整合RFSKit，封装一套针对RFS的二次开发接口，包括指令下发、基于网络/xdma的数据上行、下行