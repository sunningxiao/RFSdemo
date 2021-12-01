import socket
from typing import Union
from threading import Thread, Event

from core.xdma import Xdma

from tools.dqueue import Queue
from tools.utils import SingletonType, APIBaseType


class __RFSAPIInterface(APIBaseType, SingletonType):
    _METHODS = frozenset({
        "recv_cmd", "send_cmd",
        "read_data", "write_data", "pre_read", "pre_write", "lookup_data",
        "accept", "close", "set_timeout"
    })
    _ATTRS = {
        "queue_size": 10
    }


class CommandTCPInterface(metaclass=__RFSAPIInterface, _root=True):

    _local_port = 5000
    _remote_port = 5001
    _conn_ip = "192.168.1.161"
    _serial_num = 1
    _timeout = 5

    def __init__(self):
        self._tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.set_timeout(self._timeout)
        self._tcp_server.connect((self._conn_ip, self._remote_port))
        self._recv_addr = (self._conn_ip, self._remote_port)

    def recv_cmd(self, size=1024):
        return self._tcp_server.recv(size)

    def send_cmd(self, data):
        return self._tcp_server.send(data)

    def close(self):
        try:
            self._tcp_server.shutdown(socket.SHUT_RDWR)
            self._tcp_server.close()
        except Exception as e:
            pass

    def __del__(self):
        self.close()

    def set_timeout(self, value=2):
        self._tcp_server.settimeout(value)

    def get_number(self):
        return self._serial_num

    def update_number(self):
        self._serial_num += 1


class DataTCPInterface(metaclass=__RFSAPIInterface, _root=True):
    _local_port = 5002
    _remote_port = 5002
    _conn_ip = "192.168.1.161"
    _serial_num = 1
    _timeout = None
    queue_size = 10

    def __init__(self):
        self.fd = None
        self.read_put_queue: Union[None, Queue] = None
        self.read_get_queue: Union[None, Queue] = None
        self.stop_event: Union[None, Event] = None

        self._tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._tcp_server.bind(('0.0.0.0', self._local_port))
        self._tcp_server.listen(1)
        self._recv_server = None
        self._recv_addr = (self._conn_ip, self._remote_port)
        self.set_timeout(self._timeout)

    def accept(self, stop_event: Event, queue=Queue):
        self._recv_server, self._recv_addr = self._tcp_server.accept()
        self.read_put_queue = queue(self.queue_size)
        # self.read_get_queue = queue(self.queue_size)
        self.stop_event = stop_event

    def read_data(self):
        return self.read_put_queue.m_get()

    def pre_read(self, size=1024):
        self.fd = self._recv_server.recv(size, socket.MSG_WAITALL)

        while not self.stop_event.is_set():
            if self.read_put_queue.m_put(self.fd):
                break
        return True

    def write_data(self):
        return

    def pre_write(self, data):
        self.fd = data

    def close(self):
        try:
            self._tcp_server.close()
            self._recv_server.shutdown(socket.SHUT_RDWR)
            self._recv_server.close()
        except Exception as e:
            pass

    def close_recv(self):
        try:
            self._recv_server.shutdown(socket.SHUT_RDWR)
            self._recv_server.close()
        except Exception as e:
            pass

    def __del__(self):
        self.close()

    def set_timeout(self, value=2):
        self._tcp_server.settimeout(value)

    def get_number(self):
        return self._serial_num

    def update_number(self):
        self._serial_num += 1

    @property
    def recv_server(self):
        return self._recv_server
    
    
class XdmaInterface(metaclass=__RFSAPIInterface, _root=True):
    _board_id = 0
    chnl = 0
    xdma_length = 16*1024**2
    queue_size = 10

    def __init__(self):
        super(XdmaInterface, self).__init__()
        self.xdma = Xdma()
        self.buffer_list = []

    def accept(self, stop_event: Event, queue=Queue):
        self.xdma.open_board(self._board_id)
        self.buffer_list = [self.xdma.alloc_buffer(self._board_id, self.xdma_length) for _ in range(self.queue_size)]

    def read_data(self, size=1024):
        return self._recv_server.recv(size, socket.MSG_WAITALL)

    def write_data(self, data):
        return self._recv_server.send(data)
