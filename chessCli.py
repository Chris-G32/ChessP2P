import socket
import time, multiprocessing
from options import Menu,options

def wait_for_request():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)  # Allow one incoming connection

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

def send_game_request(friend_ip):
    host = '127.0.0.1'  # IP address of the server
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("Enter a message: ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode())
    
    client_socket.close()


OPTIONS=options()
def validate_input(inp):
    try:
        choice = int(inp)
        if choice < 1 or choice > OPTIONS.MAX_VAL:
            print("Invalid choice. Please select a valid option.")
            return False
        return True
    except ValueError:
        print("Invalid input. Please enter a number.")
        return False

def challenge_friend(ip):
    pass

MENU= f"Hi, Welcome to P2PChess!\nOptions:\n\t{OPTIONS.FIND_GAME}: Find game\
\n\t{OPTIONS.CHALLENGE_FRIEND}: Challenge friend\n\t{OPTIONS.PLAY_BOT}Play bot\n\t5Your ip address is: {socket.gethostbyname(socket.gethostname())}"
def start_session():
    #Start listening for 

    choice=None
    valid_choice=False
    #Get selection
    while(not valid_choice):
        choice=input(MENU)
        valid_choice=validate_input(choice)
    
    #Handle input
    if choice == OPTIONS.FIND_GAME:
        pass
    elif choice == OPTIONS.CHALLENGE_FRIEND:
        friend_ip=input("Enter your friends IP address. You will be the host machine.")
        challenge_friend(friend_ip)

    elif choice == OPTIONS.PLAY_BOT:
        pass
    else:
        print("VALUE ERROR, CLOSING PROCESS")

    menu=Menu()
    menu.display_menu()
    menu.execute_choice()

if __name__ == "__main__":
    menu_selector = multiprocessing.Process(target = start_session)
    menu_selector.start()

    menu_selector.terminate()
    menu_selector.join()
