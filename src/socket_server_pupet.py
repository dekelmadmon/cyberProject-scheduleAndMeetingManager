import json
import socket
import threading
import sqlite3
import tempfile
import os


class SocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.counter = 0

        self.temp_file = tempfile.NamedTemporaryFile(delete=True)
        self.db_path = self.temp_file.name
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "database.db")

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

        threading.Thread(target=self.accept_connections, args=(server_socket,), daemon=True).start()

    def accept_connections(self, server_socket):
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to client: {client_address[0]}:{client_address[1]}")

            threading.Thread(target=self.handle_request, args=(client_socket,), daemon=True).start()

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
            print(f"Received request: {request_type} from {email}, counter is {self.counter}")
            response = self.process_request(request_data)
            client_socket.sendall(response.encode("utf-8"))
        else:
            print("Incomplete request received")

    def process_request(self, request_data):
        request_type = request_data.get("request_type")
        if request_type == "create_invitation":
            self.save_invitation(request_data)
            return "Invitation created"
        elif request_type == "receive_invitation":
            self.counter -= 1
            return "Invitation received"
        else:
            print("Invalid request type received")
            return "Invalid request type"

    def create_temporary_database(self):
        # Connect to the temporary SQLite database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Create a table to store the requests
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                address REAL,
                sender TEXT,
                recipient TEXT,
                date TEXT,
                status TEXT
            )
            """
        )

        # Commit the changes and close the database connection
        connection.commit()
        connection.close()

    def save_invitation(self, request_data):
        # Connect to the temporary SQLite database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Insert a new row into the requests table
        cursor.execute(
            """
            INSERT INTO requests (sender, recipient, date, status)
            VALUES (?, ?, ?, ?)
            """,
            (request_data.get("email"), request_data.get("recipient"), request_data.get("date"), "pending"),
        )

        # Commit the changes and close the database connection
        connection.commit()
        connection.close()

    def cleanup_temporary_database(self):
        self.temp_file.close()

    def run(self):
        try:
            self.create_temporary_database()

            # Start the server
            self.start()

            # Keep the server running
            while True:
                pass

        finally:
            self.cleanup_temporary_database()


# Usage example
server = SocketServer("localhost", 18080)
server.run()
