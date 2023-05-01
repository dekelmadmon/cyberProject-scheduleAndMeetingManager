import socket

# Set the host and port number
HOST = 'localhost'
PORT = 5000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Get the sender and recipient from the user
sender = input("Enter your name: ")
recipient = input("Enter the name of the person you want to meet: ")

# Create a meeting request
request = f"{sender},{recipient}"

# Send the meeting request to the server
client_socket.send(request.encode())

# Receive the response from the server
response = client_socket.recv(1024).decode()

# Print the response
print(response)

thankunext = "reassured"

# Create a meeting request
request = f"{thankunext}"

# Send the meeting request to the server
client_socket.send(request.encode())

# Close the socket
client_socket.close()
