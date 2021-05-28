import socket


class MessageUdpServer:

    _local_port = 6045
    _remote_port = 6044
    _conn_ip = "172.19.5.184"
    _serial_num = 1
    _timeout = None

    def __init__(self):
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_server.bind(("", self._local_port))
        self._udp_server = udp_server
        self.settimeout(self._timeout)
        self._recv_addr = (self._conn_ip, self._remote_port)

    def recv(self, size=1024):
        while True:
            recv, addr = self._udp_server.recvfrom(size)
            if addr == self._recv_addr:
                return recv
            # print(f"接收到addr: {addr}信息")

    def send(self, data):
        return self._udp_server.sendto(data, self._recv_addr)

    def close(self):
        self._udp_server.close()

    def __del__(self):
        self.close()

    def settimeout(self, value=2):
        self._udp_server.settimeout(value)

    def get_number(self):
        return self._serial_num

    def update_number(self):
        self._serial_num += 1


class CommandTCPServer:

    _local_port = 5000
    _remote_port = 5001
    _conn_ip = "192.168.1.161"
    _serial_num = 1
    _timeout = None

    def __init__(self):
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.connect((self._conn_ip, self._remote_port))
        self._tcp_server = tcp_server
        self.settimeout(self._timeout)
        self._recv_addr = (self._conn_ip, self._remote_port)

    def recv(self, size=1024):
        return self._tcp_server.recv(size)

    def send(self, data):
        return self._tcp_server.send(data)

    def close(self):
        self._tcp_server.shutdown(socket.SHUT_RDWR)
        self._tcp_server.close()

    def __del__(self):
        self.close()

    def settimeout(self, value=2):
        self._tcp_server.settimeout(value)

    def get_number(self):
        return self._serial_num

    def update_number(self):
        self._serial_num += 1


class CommandUdpServer(MessageUdpServer):

    _local_port = 6044
    _remote_port = 6044
    _conn_ip = '172.19.5.184'
    _timeout = 5