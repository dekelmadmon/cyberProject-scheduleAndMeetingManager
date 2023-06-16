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

            threading.Thread(target=self.handle_request, args=(client_socket, ), daemon=True).start()

    def handle_request(self, client_socket):
        email = client_socket.recv(1024).decode("utf-8").strip()
        request = client_socket.recv(1024).decode("utf-8").strip()

        if request:
            print(f"Received request: {request} from {email}, counter is {self.counter}")
            self.process_request(request, email)
        else:
            print("Empty request received")

    def process_request(self, request):
        if request == "SET":
            self.counter += 1
        if request == "GET":
            self.counter -= 1

    def create_temporary_database(self):
        # Connect to the temporary SQLite database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Create a table to store the requests
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                address REAL PRIMARY KEY,
                sender TEXT ,
                recipient TEXT,
                date TEXT,
                status TEXT
            )
            """
        )

        # Commit the changes and close the database connection
        connection.commit()
        connection.close()

    def create_temporary_database(self):
        # Connect to the temporary SQLite database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Close the database connection
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
server = SocketServer("localhost", 12345)
server.run()
