import socket
from threading import Thread

class MeetingRequestServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = []
        socket_server_thread = Thread(target=self.start)
        socket_server_thread.start()

    def start(self):
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connected to {address}")

            useremail = client_socket.recv(1024).decode()  # Receive useremail from client
            print(f"Received useremail: {useremail}")

            client_socket.send("Useremail received".encode())  # Send response to the client

            client_handler = ClientHandler(client_socket, address, self, useremail)  # Pass the server object and useremail
            client_handler.start()  # Start the client handler thread

            self.clients.append(client_handler)
            represent = repr(client_handler)
            print(represent)

    def stop(self):
        for client_handler in self.clients:
            client_handler.client_socket.close()
        self.server_socket.close()

    def find_client(self, useremail):
        for client_handler in self.clients:
            if client_handler.useremail == useremail:
                return client_handler
        return None


class ClientHandler(Thread):
    def __init__(self, client_socket, address, server, useremail):
        super().__init__()
        self.client_socket = client_socket
        self.address = address
        self.server = server
        self.useremail = useremail

    def __repr__(self):
        return f"ClientHandler object - Address: {self.address}, Useremail: {self.useremail}"

    def run(self):
        while True:
            request = self.client_socket.recv(1024).decode()

            if not request:
                print(f"Connection closed by {self.address}")
                break

            if request == "reassured":
                reassurance_response = "Reassurance received successfully"
                self.client_socket.send(reassurance_response.encode())
                continue

            try:
                sender, recipient, date = request.split(',')
            except ValueError:
                print(f"Invalid meeting request received from {self.address}")
                continue

            # Find the client handler for the recipient
            recipient_client = self.server.find_client(recipient)
            print(recipient_client)
            if recipient_client is not None:
                # Send meeting invitation to recipient
                invitation = f"You are invited to a meeting from {sender} at {date}"
                recipient_client.client_socket.send(invitation.encode())

                # Send reassurance response to sender
                reassurance_response = "Meeting invitation sent successfully"
                self.client_socket.send(reassurance_response.encode())
            else:
                reassurance_response = f"Recipient {recipient} not found"
                self.client_socket.send(reassurance_response.encode())

        self.client_socket.close()


# Usage
server = MeetingRequestServer('localhost', 5002)