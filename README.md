## RFS_demo

* 打包方法

  `pyinstaller -Fw console.py`

* 环境安装
  
  `pip install -r requirements.txt`

## 变更记录
### v2.0

* 建立连接后立即发送RF配置指令，可在icd.json中自定义连接后发送的指令
* DDS配置与系统开启加入弹窗，可直观的展示、修改要下发的所有参数
* 修复自定义指令执行bug
* 界面调整，贴合RFSoc运行逻辑
* 每次成功开启采集后都会在数据文件夹下生成一个icd_run.json
* 波形快视不进行抽取
* 界面增加参数：基准PRF来源

### v2.1

* 波形装载支持总览界面与一键配置，可记录文件路径，（双击文件路径可清除选择）

### v2.2

* 加入未归一化的频谱显示
* 快视刷新间隔从 `>1秒` 调整成 `>1.5秒` 

### v2.3

* 加入QMC配置
* 修复bug不能下发浮点数

### v2.4

* 加入参数关系解析，
  `"ADC0增益":    ["ADC0增益", "double", 0, "10**(x/20)"]`
  发送时会根据表达式对参数的数值做运算