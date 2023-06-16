import socket
import threading
import time
from sys import argv
from clientSide import app
from flask import Flask

class SocketClient:
    def __init__(self, host, port, email):
        self.host = host
        self.port = port
        self.email = email

    def start(self):
        while True:
            self.send_get_request()
            time.sleep(5)  # Wait for 5 seconds before sending the next ping

    def send_get_request(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(self.email.encode("utf-8"))
            request = "GET"
            client_socket.send(request.encode("utf-8"))
            client_socket.close()

    def send_set_request(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(self.email.encode("utf-8"))
            request = "SET"
            client_socket.send(request.encode("utf-8"))
            client_socket.close()


