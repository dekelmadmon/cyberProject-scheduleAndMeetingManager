import socket

# Set the host and port number
HOST = 'localhost'
PORT = 5000

def request_meeting(attendee, sender):

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))


    # Create a meeting request
    request = f"{sender},{attendee}"

    # Send the meeting request to the server
    client_socket.send(request.encode())

    # Receive the response from the server
    response = client_socket.recv(1024).decode()

    # Print the response
    print(response)

    reassurance = "reassured"

    # Create a meeting request
    request = f"{reassurance}"

    # Send the meeting request to the server
    client_socket.send(request.encode())

    # Close the socket
    client_socket.close()
