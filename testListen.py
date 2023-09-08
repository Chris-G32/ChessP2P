import socket
def start_server():
    host = '10.14.81.60'  # Listen on all available interfaces
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Allow one incoming connection

    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print("Connected to:", client_address)

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print("Received:", data)

    client_socket.close()
    server_socket.close()

start_server()