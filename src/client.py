import socket

class MeetingRequestClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def request_meeting(self, attendee, sender, date):
        try:
            # Connect to the server
            self.client_socket.connect((self.host, self.port))

            # Create a meeting request
            request = f"{sender},{attendee},{date}"

            # Send the meeting request to the server
            self.client_socket.send(request.encode())

            # Receive the response from the server
            response = self.client_socket.recv(1024).decode()

            # Print the response
            print(response)

            reassurance = "reassured"

            # Create a meeting request
            request = f"{reassurance}"

            # Send the meeting request to the server
            self.client_socket.send(request.encode())

        except ConnectionRefusedError:
            print("Failed to connect to the server.")

        finally:
            # Close the socket
            self.client_socket.close()

# Usage
client = MeetingRequestClient('localhost', 5000)
