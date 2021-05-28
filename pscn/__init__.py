from printLog import printWarning, simulation_ctl
try:
    if simulation_ctl:
        from .xdma_sim import Xdma
    else:
        from .xdma import Xdma
except OSError as e:
    printWarning(e)
    from .xdma_sim import Xdma
