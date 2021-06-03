import socket


class CommandTCPServer:

    _local_port = 5000
    _remote_port = 5001
    _conn_ip = "192.168.1.161"
    _serial_num = 1
    _timeout = 5

    def __init__(self):
        self._tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.settimeout(self._timeout)
        self._tcp_server.connect((self._conn_ip, self._remote_port))
        self._recv_addr = (self._conn_ip, self._remote_port)

    def recv(self, size=1024):
        return self._tcp_server.recv(size)

    def send(self, data):
        return self._tcp_server.send(data)

    def close(self):
        try:
            self._tcp_server.shutdown(socket.SHUT_RDWR)
            self._tcp_server.close()
        except Exception as e:
            pass

    def __del__(self):
        self.close()

    def settimeout(self, value=2):
        self._tcp_server.settimeout(value)

    def get_number(self):
        return self._serial_num

    def update_number(self):
        self._serial_num += 1


class DataTCPServer:
    _local_port = 5002
    _remote_port = 5002
    _conn_ip = "192.168.1.161"
    _serial_num = 1
    _timeout = None

    def __init__(self):
        self._tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._tcp_server.bind(('0.0.0.0', self._local_port))
        self._tcp_server.listen(1)
        self._recv_server = None
        self._recv_addr = (self._conn_ip, self._remote_port)
        self.settimeout(self._timeout)

    def accept(self):
        self._recv_server, self._recv_addr = self._tcp_server.accept()

    def recv(self, size=1024):
        return self._recv_server.recv(size, socket.MSG_WAITALL)

    def send(self, data):
        return self._recv_server.send(data)

    def close(self):
        try:
            self._recv_server.shutdown(socket.SHUT_RDWR)
            self._recv_server.close()
            self._tcp_server.close()
        except Exception as e:
            pass

    def __del__(self):
        self.close()

    def settimeout(self, value=2):
        self._tcp_server.settimeout(value)

    def get_number(self):
        return self._serial_num

    def update_number(self):
        self._serial_num += 1

    @property
    def recv_server(self):
        return self._recv_server
