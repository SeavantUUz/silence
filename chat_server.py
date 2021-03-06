# coding: utf-8
import socket
import logging
# import gevent
# from gevent import monkey
# monkey.patch_socket()
import select
# monkey.patch_select()
from ui import UI
import threading
import os
from traceback import format_exc as einfo

class Server(object):
    def __init__(self):
        # self.users = []
        self.records = []
        self.connect_sockets = []
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.interrupt_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s_termin_io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_termin_io.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.c_termin_io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c_termin_io.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = 3657
        self.io_port = 3658
        self.connect_sockets.append(self.server_socket)
        self.connect_sockets.append(self.interrupt_socket)
        self.connect_sockets.append(self.s_termin_io)
        self.is_started = False
        self.is_continue = True
    
    def run(self):
        logging.info("run!")
        #if not self.is_started:
        #    self.start()
        self._accept_loop()

    def start(self):
        self.s_termin_io.bind(('localhost', self.io_port))
        self.s_termin_io.listen(1)
        # self.c_termin_io.connect(('localhost',self.io_port))
        self.ui = UI(self.c_termin_io, self.io_port)
        self.server_socket.bind(("localhost",self.port))
        self.server_socket.listen(5)
        try:
            os.remove('server_interrupt.sock')
        except OSError:
            pass
        self.interrupt_socket.bind('server_interrupt.sock')
        self.interrupt_socket.listen(1)
        server_run = self.run
        ui_run = self.ui.run
        self.is_started = True
        # gevent.spawn(server_run)
        #threading.Thread(target=server_run).start()
        ## gevent.joinall([
        ##                 gevent.spawn(server_run),
        ##                 gevent.spawn(ui_run),
        ##                 ])
        threading.Thread(target=ui_run).start()
        server_run()

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
        while True and self.ui.is_continue and self.is_continue:
            read_sockets, write_sockets, error_sockets = select.select(self.connect_sockets, [], [], 1)
            end_socks = []
            for sock in read_sockets:
                if sock == self.server_socket:
                    logging.info('server socket target')
                    sockfd, addr = self.server_socket.accept()
                    self.connect_sockets.append(sockfd)
                    self.ui.append("{} enter the room".format(addr))
                    logging.info("new client enter")
                    self.broadcast(sock, "{} enter the room".format(addr))
                elif sock == self.interrupt_socket:
                    continue
                elif sock == self.s_termin_io:
                    try:
                        sockfd, addr = sock.accept()
                        self.io = sockfd
                        self.connect_sockets.append(self.io)
                        data =  self.io.recv(4096)
                        logging.info("termin io data {}".format(data))
                        if data:
                            data = data.replace('\r','').replace('\n','')
                            content = str("someone >" + data)
                            self.broadcast(sock, content)
                    except:
                        self.io.close()
                        logging.info("socket error, einfo {}".format(einfo()))
                elif sock == self.io:
                    try:
                        data = sock.recv(4096)
                        if data:
                            data = data.replace('\r','').replace('\n','')
                            content = str("someone >" + data)
                            self.broadcast(sock, content)
                    except:
                        self.io.close()
                        logging.info("socket io error, einfo {}".format(einfo()))
                else:
                    try:
                        logging.info("else target")
                        data = sock.recv(4096)
                        if data:
                            logging.info("data: {}".format(type(data)))
                            data = data.replace('\r','').replace('\n','')
                            content = str(sock.getpeername())+">"+data
                            # self.records.append(content)
                            self.ui.append(content)
                            self.broadcast(sock, content)
                    except:
                        logging.info("sock error, einfo {}".format(einfo()))
                        self.broadcast(sock, "Client {} is offline".format(addr))
                        sock.close()
                        end_socks.append(sock)
            for _socket in end_socks:
                self.connect_sockets.remove(_socket)
        logging.info("server socket end")
        try:
            os.remove('server_interrupt.sock')
        except OSError:
            pass
        # self.server_socket.close()
        for sock in self.connect_sockets:
            sock.close()

if __name__ == "__main__":
    logging.basicConfig(filename="log",level=logging.INFO)
    server = Server()
    server.start()
