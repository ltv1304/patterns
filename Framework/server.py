import socket
from select import select

from Framework.http_lib import RequestTestServer
from web_app import app


class TestServer:
    def __init__(self):
        self.to_monitor = []

    def runserver(self, port=8001, host='localhost'):
        host = 'localhost' if host is None else host
        self.init_server_socket(port, host)
        self.to_monitor.append(self.server_socket)
        self.event_loop()

    def init_server_socket(self, port, host):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

    def event_loop(self):
        while True:
            ready_to_read, _, _ = select(self.to_monitor, [], [])
            for sock in ready_to_read:
                if sock is self.server_socket:
                    self.accept_connection()
                else:
                    self.handle_connection(sock)

    def accept_connection(self):
        client_socket, addr = self.server_socket.accept()
        print(f'Connection from {addr}')
        self.to_monitor.append(client_socket)

    def handle_connection(self, client_socket):
        bytes = client_socket.recv(4096)
        if bytes:
            request = RequestTestServer(bytes)
            http_responce = app(request)

            client_socket.send(f'{http_responce.response_proto} {http_responce.response_status}'.encode())
            client_socket.send(http_responce.headers.encode())
            client_socket.send('\n'.encode())  # to separate headers from body
            client_socket.send(http_responce.body)
            self.to_monitor.remove(client_socket)
            client_socket.close()
        else:
            self.to_monitor.remove(client_socket)
            client_socket.close()




