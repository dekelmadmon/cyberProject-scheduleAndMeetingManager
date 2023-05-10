import socket

# Define the server's host and port number
HOST = 'localhost'
PORT = 5000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen()
print(f"Server listening on {HOST}:{PORT}")

while True:
    # Accept a connection
    client_socket, address = server_socket.accept()
    print(f"Connected to {address}")

    # Receive a meeting request from the client
    request = client_socket.recv(1024).decode()

    # Parse the request into sender and recipient
    try:
        sender, recipient = request.split(',')
    except ValueError:
        print(f"Invalid meeting request received from {address}")
        continue

    # Print the request details
    print(f"Meeting request from {sender} to {recipient}")

    # Send a response back to the sender
    response = f"Meeting request sent from {sender} to {recipient}"
    client_socket.send(response.encode())

    # Wait for reassurance response
    reassurance_response = client_socket.recv(1024).decode()

    # Print the reassurance message from the client
    print(reassurance_response)

    # Close the client socket
    client_socket.close()

# Close the server socket
server_socket.close()
