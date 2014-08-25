# coding:utf-8
import socket
import logging
from gevent import monkey
monkey.patch_socket()
import select
monkey.patch_select()
import sys

class Client(object):
    def __init__(self):
        self.records = []
        self.host = "0.0.0.0"
        self.port = 3657
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stdin = sys.stdin
        self.sockets = [self.stdin, self.client_socket]

    def start(self):
        try:
            self.client_socket.connect((self.host,self.port))
        except:
            logging.error("unable to connect")
            sys.exit()
        else:
            self._loop()

    def end(self):
        self.client_socket.close()

    def _loop(self):
        try:
            while True:
                rsockets,wsockets,esockets = select.select(self.sockets,[],[])
                for _socket in rsockets:
                    if _socket == self.client_socket:
                        data = _socket.recv(4096)
                        if data:
                            self.records.append(data)
                            print data
                        else:
                            logging.error("\nDisconnect from server")
                            sys.exit()
                    else:
                        msg = sys.stdin.readline()
                        self.client_socket.send(msg)
        except KeyboardInterrupt:
            self.end()

if __name__ == "__main__":
    client = Client()
    client.start()
