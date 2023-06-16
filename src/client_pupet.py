import json
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
        '''while True:
            self.send_receive_invitation()
            time.sleep(5)  # Wait for 5 seconds before sending the next ping
        '''
    def send_create_invitation(self, date, recipient):
        request_data = {
            "request_type": "create_invitation",
            "email": self.email,
            "date": date,
            "recipient": recipient,
        }
        request_json = json.dumps(request_data)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(request_json.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8").strip()
            print(f"Received response: {response}")

    def send_receive_invitation(self):
        request_data = {
            "request_type": "receive_invitation",
            "email": self.email
        }
        request_json = json.dumps(request_data)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(request_json.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8").strip()
            print(f"Received response: {response}")
            return response


