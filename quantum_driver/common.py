class Quantity(object):
    def __init__(self, name: str, value=None, ch: int = 1, unit: str = ''):
        self.name = name
        self.default = dict(value=value, ch=ch, unit=unit)


class BaseDriver:
    def __init__(self, addr, timeout, **kw):
        self.addr = addr
        self.timeout = timeout


def get_coef(*args):
    return '', '', '', ''
