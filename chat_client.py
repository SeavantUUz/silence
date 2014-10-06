# coding:utf-8
import socket
import logging
## import gevent
## from gevent import monkey
## monkey.patch_socket()
import select
## monkey.patch_select()
import sys,os
from ui import UI
import threading

class Client(object):
    def __init__(self):
        # self.records = []
        self.host = "0.0.0.0"
        self.port = 3657
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.stdin = sys.stdin
        # self.local_socket_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # self.local_socket_client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # self.sockets = [self.stdin, self.client_socket]
        # self.sockets = [self.local_socket_server, self.client_socket]
        self.interrupt_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.remove('client_termin_io.sock')
        except OSError:
            pass
        self.s_termin_io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c_termin_io = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_termin_io.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.c_termin_io.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockets = [self.client_socket]
        self.sockets.append(self.s_termin_io)
        self.is_started = False
        self.io_port = 3659

    def run(self):
        #if not self.is_started:
        #self.start()
        self._loop()

    def start(self):
        self.s_termin_io.bind(('localhost', self.io_port))
        self.s_termin_io.listen(1)
        self.client_socket.connect(("localhost", self.port))
        self.interrupt_socket.bind('client_interrupt.sock')
        self.interrupt_socket.listen(1)
        self.ui = UI(self.c_termin_io, self.io_port, True) 
        client_run = self.run
        ui_run = self.ui.run
        threading.Thread(target=ui_run).start()
        client_run()

    def end(self):
        self.client_socket.close()
        try:
            os.remove('client_interrupt.sock')
        except OSError:
            pass
        #self.ui.end()

    def _loop(self):
        logging.info("in loop")
        try:
            while True:
                rsockets,wsockets,esockets = select.select(self.sockets,[],[])
                for _socket in rsockets:
                    # receive msg
                    if _socket == self.client_socket:
                        data = _socket.recv(4096)
                        if data:
                            # self.records.append(data)
                            logging.info(data)
                            self.ui.append(data)
                        else:
                            logging.error("\nDisconnect from server")
                            sys.exit()
                    elif _socket == self.interrupt_socket:
                        continue
                    elif _socket == self.s_termin_io:
                        try:
                            sockfd, addr = _socket.accept()
                            self.io = sockfd
                            self.sockets.append(self.io)
                            data = self.io.recv(4096)
                            if data:
                                self.client_socket.send(data)
                        except:
                            self.io.close()
                            logging.info("socket err, einfo {}".format(einfo()))
                    else:
                        data = _socket.recv(4096)
                        if data:
                            logging.info("data: {}".format(data))

                    # send msg
                    # elif _socket == self.local_socket_server:
                    #     msg = _socket.recv(4096)
                    #     self.client_socket.send(msg)
                    # else:
                        # msg = sys.stdin.readline()
                        # self.client_socket.send(msg)
                        # send message to server
                    #    msg = _socket.recv(4096)
                    #    self.client_socket.send(msg)
        finally:
            self.end()

if __name__ == "__main__":
    logging.basicConfig(filename="client.log", level=logging.INFO)
    client = Client()
    client.start()
