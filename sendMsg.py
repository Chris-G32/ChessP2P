import socket

def start_client():
    host = '10.14.81.60'  # IP address of the server
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("Enter a message or 'exit' to exit: ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode())

    client_socket.close()

start_client()