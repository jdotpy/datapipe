from threading import Lock
import socketserver
import socket

### Raw Section - Incomplete, use below sections instead for now ###
class NetSocket():
    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port
        self.bind = kwargs.get('bind', False)
        self.receive_buffer = kwargs.get('receive_buffer', 1024)
        self.send_buffer = kwargs.get('send_buffer', 1024)
        self._create_socket()

class UDPSocket(NetSocket):
    protocol = 'udp'
    socket_type = socket.SOCK_DGRAM

    def _create_socket(self):
        self._socket = socket.socket(socket.AF_INET, self.socket_type)
        if self.bind:
            self._socket.bind((UDP_IP, UDP_PORT))
        return self._socket

    def send(self):
        self._socket.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    def receive(self):
        self._socket.recvfrom(self.receive_buffer)

class TCPSocket(NetSocket):
    protocol = 'tcp'
    socket_type = socket.SOCK_STREAM

    def _create_socket(self): 
        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, self.socket_type):
            af, socktype, proto, canonname, sa = res
            try:
                self._socket = socket.socket(af, socktype, proto)
            except OSError as e:
                self._socket = None
                continue
            try:
                if self.bind:
                    self._socket.bind(sa)
                else:
                    self._socket.connect(sa)
            except OSError as e:
                s.close()
                self._socket = None
                continue
            break
        return self._socket

### SocketServer ###
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass
class NSTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        receive_size = self.network_server.options['receive_size']
        payload = self.request.recv(receive_size)
        client = self.client_address[0]
        with self.network_server.event_lock:
            self.network_server.handle(client, payload)

    def reply(self, payload):
        self.request.sendall(payload)

class NSUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        with self.network_server.event_lock:
            self.network_server.handle(self.client_address[0], data)

    def reply(self, payload):
        self.request[1].sendto(payload, self.client_address)

class NetworkServer():
    server = None
    handler = None
    default_options = {
        'receive_size': 1024,
        'send_size': 1024
    }

    def __init__(self, callback, host, port, server=None, handler=None, **options):
        self.callback = callback
        self.host = host
        self.port = port
        self.options = self.default_options.copy()
        self.options.update(options)
        self.event_lock = Lock()

        if server:
            self.server = server or self.server
        if handler:
            self.handler = handler or self.handler
        self.handler = self._configure_handler(handler)

        self._connect()

    def _configure_handler(self, Handler):
        ConfiguredHandler = type('ConfiguredNetHandler', (Handler,), {'network_server': self})
        return ConfiguredHandler

    def _connect(self):
        self.net = self.server((self.host, self.port), self.handler)

    def listen(self):
        self.net.serve_forever()

    def handle(self, client, payload):
        self.callback(client, payload)

class TCPNetworkServer(NetworkServer):
    handler = NSTCPHandler
    server = ThreadedTCPServer

class UDPNetworkServer(NetworkServer):
    handler = NSUDPHandler
    server = ThreadedUDPServer

### Clients ###
class BaseNetworkClient():
    def __init__(self, host, port, callback=None, **options):
        self.host = host
        self.port = port
        self.callback = callback
        self.options = options
        self._connect()

    def listen(self):
        while True:
            payload = self._socket.recv(self.options['receive_size'])
            if self.callback:
                self.callback(payload)

class TCPNetworkClient(BaseNetworkClient):
    def _connect(self, callback):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

    def send(self, payload):
        self._socket.sendall(payload)

class UDPNetworkClient(BaseNetworkClient):
    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, payload):
        self._socket.sendto(payload, (self.host, self.port))
