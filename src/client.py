import socket
from threading import Thread


class MeetingRequestClient:
    def __init__(self, host, port, useremail):
        self.host = host
        self.port = port
        self.useremail = useremail
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        self.client_socket.connect((self.host, self.port))

        # Send the useremail to the server after connection
        self.client_socket.sendall(self.useremail.encode())

        # Receive the response from the server
        response = self.client_socket.recv(1024)
        print(response.decode())  # Print the server response
        self.receive_thread = Thread(target=self.receive_requests)  # Thread for receiving requests
        self.receive_thread.start()  # Start the receive thread

    def request_meeting(self, recipient, sender, date):
        try:
            # Create a meeting request
            request = f"{sender},{recipient},{date}"

            # Send the meeting request to the server
            self.client_socket.send(request.encode())
            print("Waiting for response...")

            # Receive the response from the server
            response = self.client_socket.recv(1024).decode()

            # Print the response
            print(response)

        except ConnectionRefusedError:
            print("Failed to connect to the server.")

    def receive_requests(self):
        try:
            while True:
                # Receive incoming requests from the server
                request = self.client_socket.recv(1024).decode()

                if not request:
                    break

                # Check if the received request has the expected format
                if ',' not in request:
                    print(f"Invalid request received: {request}")
                    continue

                # Process the received request
                sender, date = request.split(',')
                print(f"Received meeting request from {sender} at {date}")

                # You can handle the received meeting request here and take appropriate actions

        except ConnectionResetError:
            print("Connection to the server was reset.")
        finally:
            self.client_socket.close()
