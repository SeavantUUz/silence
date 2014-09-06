# coding: utf-8
import socket
import logging
import gevent
from gevent import monkey
monkey.patch_socket()
import select
monkey.patch_select()
from ui import UI
import threading

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
        self.is_started = False
        self.test = test
    
    def run(self):
        logging.info("run!")
        #if not self.is_started:
        #    self.start()
        self._accept_loop()

    def start(self):
        self.server_socket.bind(("0.0.0.0",self.port))
        self.server_socket.listen(5)
        server_run = self.run
        ui_run = self.ui.run
        self.is_started = True
        # gevent.spawn(server_run)
        #threading.Thread(target=server_run).start()
        gevent.joinall([
                        gevent.spawn(server_run),
                        gevent.spawn(ui_run),
                        ])

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
        logging.info("loop!")
        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.connect_sockets, [], [])
            logging.info("select trigger")
            end_socks = []
            for sock in read_sockets:
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    logging.info(addr)
                    self.connect_sockets.append(sockfd)
                    self.ui.append("{} enter the room".format(addr))
                    logging.info("new client enter")
                    self.broadcast(sock, "{} enter the room".format(addr))
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
    logging.basicConfig(filename="log",level=logging.INFO)
    server = Server()
    server.start()
