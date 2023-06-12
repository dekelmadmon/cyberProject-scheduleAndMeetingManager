import socket
import threading


class MeetingRequestServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = []

    def start(self):
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connected to {address}")

            client_handler = ClientHandler(client_socket, address)
            self.clients.append(client_handler)
            client_handler.start()
    def stop(self):
        for client_socket in self.clients:
            client_socket.close()
        self.server_socket.close()




    def run(self):
        while True:
            request = self.client_socket.recv(1024).decode()

            if not request:
                print(f"Connection closed by {self.address}")
                break

            try:
                sender, recipient, date = request.split(',')
            except ValueError:
                print(f"Invalid meeting request received from {self.address}")
                continue

            print(f"Meeting request from {sender} to {recipient} at {date}")

            response = f"Meeting request sent from {sender} to {recipient} at {date}"
            self.client_socket.send(response.encode())

            reassurance_response = self.client_socket.recv(1024).decode()
            print(reassurance_response)

        self.client_socket.close()
    def find_client(self, username):
        for client in self.clients:
            if client.username == username:
                client.send(invitation)
class ClientHandler(threading.Thread):
    def __init__(self, client_socket, address):
        super().__init__()
        self.client_socket = client_socket
        self.address = address

# Usage
server = MeetingRequestServer('localhost', 5000)
server.start()
