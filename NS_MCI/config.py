import functools
import traceback
from traceback_with_variables import format_exc
# from traceback_with_variables import activate_by_import

from NS_MCI.tools.printLog import *


param_cmd_map = {
    ("系统参考时钟选择",
     "ADC采样率",
     "ADC PLL使能",
     "PLL参考时钟频率",
     "ADC抽取倍数",
     "ADC NCO频率",
     "ADC 奈奎斯特区",
     "DAC采样率",
     "DAC PLL使能",
     "PLL参考时钟频率",
     "DAC抽取倍数",
     "DAC NCO频率",
     "DAC 奈奎斯特区",
     "ADC0增益",
     "ADC0偏置",
     "ADC0相位",
     "ADC0增益步进",
     "ADC0增益截止",
     "ADC1增益",
     "ADC1偏置",
     "ADC1相位",
     "ADC1增益步进",
     "ADC1增益截止",
     "ADC2增益",
     "ADC2偏置",
     "ADC2相位",
     "ADC2增益步进",
     "ADC2增益截止",
     "ADC3增益",
     "ADC3偏置",
     "ADC3相位",
     "ADC3增益步进",
     "ADC3增益截止",
     "ADC4增益",
     "ADC4偏置",
     "ADC4相位",
     "ADC4增益步进",
     "ADC4增益截止",
     "ADC5增益",
     "ADC5偏置",
     "ADC5相位",
     "ADC5增益步进",
     "ADC5增益截止",
     "ADC6增益",
     "ADC6偏置",
     "ADC6相位",
     "ADC6增益步进",
     "ADC6增益截止",
     "ADC7增益",
     "ADC7偏置",
     "ADC7相位",
     "ADC7增益步进",
     "ADC7增益截止",
     "DAC0增益",
     "DAC0偏置",
     "DAC0相位",
     "DAC0衰减步进",
     "DAC0衰减截止",
     "DAC1增益",
     "DAC1偏置",
     "DAC1相位",
     "DAC1衰减步进",
     "DAC1衰减截止",
     "DAC2增益",
     "DAC2偏置",
     "DAC2相位",
     "DAC2衰减步进",
     "DAC2衰减截止",
     "DAC3增益",
     "DAC3偏置",
     "DAC3相位",
     "DAC3衰减步进",
     "DAC3衰减截止",
     "DAC4增益",
     "DAC4偏置",
     "DAC4相位",
     "DAC4衰减步进",
     "DAC4衰减截止",
     "DAC5增益",
     "DAC5偏置",
     "DAC5相位",
     "DAC5衰减步进",
     "DAC5衰减截止",
     "DAC6增益",
     "DAC6偏置",
     "DAC6相位",
     "DAC6衰减步进",
     "DAC6衰减截止",
     "DAC7增益",
     "DAC7偏置",
     "DAC7相位",
     "DAC7衰减步进",
     "DAC7衰减截止"): '初始化',
    ("基准PRF周期",
     "基准PRF数量"): '内部PRF产生',
}


class RPCMethodExecuteError(RuntimeError):
    pass


def solve_exception(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = format_exc()
            printWarning(error_message)
            printException(e)
            printWarning('请求报错')
            raise RPCMethodExecuteError(error_message)
    return wrap
