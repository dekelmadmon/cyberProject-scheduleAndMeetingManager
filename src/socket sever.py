import socket

# Set the host and port number
HOST = 'localhost'
PORT = 5000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))
while True:

    # Listen for incoming connections
    server_socket.listen()

    # Accept a connection
    client_socket, address = server_socket.accept()
    print(f"Connected to {address}")

    # Receive a meeting request from the client
    request = client_socket.recv(1024).decode()

    # Split the request into sender and recipient
    sender, recipient = request.split(',')

    # Print the request
    print(f"Meeting request from {sender} to {recipient}")

    # Send a response back to the sender
    response = f"Meeting request sent from {sender} to {recipient}"
    client_socket.send(response.encode())

    reassurance_response = client_socket.recv(1024).decode()

    print(reassurance_response)

# Close the socket
client_socket.close()
server_socket.close()
