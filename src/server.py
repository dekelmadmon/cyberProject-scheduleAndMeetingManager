import json
import socket
import threading
import os
from sys import argv

from src.managers.meetingManager import MeetingManager


class SocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.meetingManager = None

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

        threading.Thread(target=self.accept_connections, args=(server_socket,), daemon=True).start()

    def accept_connections(self, server_socket):
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"Connected to client: {client_address[0]}:{client_address[1]}")

                threading.Thread(target=self.handle_request, args=(client_socket,), daemon=True).start()
            except json.JSONDecodeError:
                print("Connection failed!")

    def handle_request(self, client_socket):
        request_json = client_socket.recv(1024).decode("utf-8").strip()
        print(f"Received JSON: {request_json}")

        try:
            request_data = json.loads(request_json)
            request_type = request_data.get("request_type")
            email = request_data.get("email")
        except json.JSONDecodeError:
            print("Invalid JSON format received")
            return

        if request_type and email:
            print(f"Received request: {request_type} from {email}")
            json_response = self.process_request(request_data)
            print(f"Response JSON: {json_response}")
            client_socket.sendall(json_response.encode())
        else:
            print("Incomplete request received")

    def process_request(self, request_data):
        if self.meetingManager is None:  # Check if client already exists
            self.meetingManager = MeetingManager()

        request_type = request_data.get("request_type")
        if request_type == "create_invitation":
            self.meetingManager.create(request_data)
            return "Invitation created"
        elif request_type == "receive_invitation":
            return self.meetingManager.retrieve(request_data)
        elif request_type == "update_invitation":
            self.meetingManager.update(request_data)
            return "Invitation updated"
        else:
            print("Invalid request type received")
            return "Invalid request type"

    def run(self):
        # Start the server
        self.start()

        # Keep the server running
        while True:
            pass

def get_ipv4():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Usage example
server = SocketServer(get_ipv4(), 18080)
server.run()
