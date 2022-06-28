from NS_MCI.tools.printLog import printWarning
from NS_MCI.xdma.LightDMA import LightDMAMixin
simulation_ctl = True
try:
    if simulation_ctl:
        from .xdma_sim import Xdma
    else:
        from .xdma import Xdma
except OSError as e:
    printWarning(e)
    from .xdma_sim import Xdma
