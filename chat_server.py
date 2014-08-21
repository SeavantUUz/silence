# coding: utf-8
import socket
from gevnet import monkey
monkey.patch_socket()
import select
mokey.patch_select()

class Server(object):
    def __init__(self):
        self.users = []
        self.records = []
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = 3657

    def start(self):
        self.server_socket.bind(("0,0,0,0",self.port))
        self.server_socket.listen(5)
        self._accept_loop()

    def _accept_loop(self):

        
