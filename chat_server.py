# coding: utf-8
import socket
import logging
from gevent import monkey
monkey.patch_socket()
import select
monkey.patch_select()
import UI

class Server(object):
    def __init__(self):
        # self.users = []
        self.records = []
        self.connect_sockets = []
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = 3657
        self.connect_sockets.append(self.server_socket)
        self.ui = UI()
    
    def run(self):
        self._accept_loop()

    def start(self):
        self.server_socket.bind(("0.0.0.0",self.port))
        self.server_socket.listen(5)
        server_run = self.run
        ui_run = self.ui.run
        gevent.spawn(server_run)
        gevent.spawn(ui_run)

    def broadcast(self, sock, data):
        end_socks = []
        for _socket in self.connect_sockets[:]:
            if  _socket != self.server_socket and _socket != sock:
                try:
                    _socket.send(data)
                except:
                    _socket.close()
                    end_socks.append(_socket)
        for _socket in end_socks:
            self.connect_sockets.remove(_socket)

    def _accept_loop(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.connect_sockets, [], [])
            end_socks = []
            for sock in read_sockets:
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.connect_sockets.append(sockfd)
                    self.broadcast(sock, "{} enter the room".format(addr))
                    print "{} enter the room".format(addr)
                else:
                    try:
                        data = sock.recv(4096)
                        if data:
                            content = str(sock.getpeername())+">"+data
                            # self.records.append(content)
                            self.ui.append(content)
                            self.broadcast(sock, content)
                    except:
                        self.broadcast(sock, "Client {} is offline".format(addr))
                        sock.close()
                        end_socks.append(sock)
            for _socket in end_socks:
                self.connect_sockets.remove(_socket)
        self.server_socket.close()

if __name__ == "__main__":
    server = Server()
    server.start()
