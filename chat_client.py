# coding:utf-8
import socket
import logging
from gevent import monkey
monkey.patch_socket()
import select
monkey.patch_select()
import sys,os
from ui import UI

class Client(object):
    def __init__(self):
        # self.records = []
        self.host = "0.0.0.0"
        self.port = 3657
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.stdin = sys.stdin
        self.local_socket_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.local_socket_client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # self.sockets = [self.stdin, self.client_socket]
        self.sockets = [self.local_socket_server, self.client_socket]
        self.is_started = False

    def run(self):
        if not self.is_started:
            self.start()
        self._loop()

    def start(self):
        try:
            try:
                os.remove("/tmp/silence.sock")
            except OSError:
                pass
            # local server listen open
            self.local_socket_server.bind('/tmp/silence.sock')
            self.local_socket_server.listen(1)
            # local client connect
            self.local_socket_client.connect('/tmp/silence.sock')
            self.client_socket.connect((self.host,self.port))
            self.ui = UI(self.local_socket_client) 
        except:
            logging.error("unable to connect")
            self.end()
            sys.exit()
        else:
            client_run = self.run
            ui_run = self.ui.run
            gevent.spawn(client_run)
            gevent.spawn(ui_run)

    def end(self):
        self.client_socket.close()
        self.local_socket_client.close()
        self.local_socket_server.close()
        try:
            os.remove('/tmp/silence.sock')
        except OSError:
            pass
        #self.ui.end()

    def _loop(self):
        try:
            while True:
                rsockets,wsockets,esockets = select.select(self.sockets,[],[])
                for _socket in rsockets:
                    # receive msg
                    if _socket == self.client_socket:
                        data = _socket.recv(4096)
                        if data:
                            # self.records.append(data)
                            self.ui.append(data)
                        else:
                            logging.error("\nDisconnect from server")
                            sys.exit()
                    # send msg
                    else:
                        # msg = sys.stdin.readline()
                        # self.client_socket.send(msg)
                        # send message to server
                        msg = _socket.recv(4096)
                        self.client_socket.send(msg)
        finally:
            self.end()

if __name__ == "__main__":
    client = Client()
    client.start()
