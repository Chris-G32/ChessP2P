
import socket
from game_request import game_request
import json
import collections
from game import Game
class Client:
    CHALLENGE_PORT=12345
    PLAY_ON_PORT=12346
    
    received_requests=collections.deque(maxlen=10)
    ip=socket.gethostbyname(socket.gethostname())
    keep_listening=False
    server_up=False

    def add_request(game_req:game_request):
        Client.received_requests.append(game_req)

    def start_server():
        Client.keep_listening=True
        Client.server_up=True
        host = Client.ip  
        port = Client.CHALLENGE_PORT
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(10)  # Allow ten incoming connection

            # print("Waiting for a connection...")
            client_socket, client_address = server_socket.accept()
            print("Connected to:", client_address)

            while Client.keep_listening:
                data = client_socket.recv(1024).decode()
                client_socket.close()
                if not data:
                    break
                print("Received:", data)
            # client_socket.close()
        except:
            print("error in challenge listener, please restart app")
            
        server_socket.close()
        Client.server_up=False

    def shutdown_server():
        Client.keep_listening=False
    



class MenuOption:
    DISPLAY_TEXT="USING DEFAULT TEXT, INHERITED FROM MENU_OPTION"
    def __init__(self)->None:
        pass

    def execute(self):
        print("BASE")

    def get_formatted_text(self,option_number):
        return f"\n\t{option_number}: {self.DISPLAY_TEXT}"
    
class ChallengeFriend(MenuOption):
    DISPLAY_TEXT="Challenge Friend"
     
    def send_game_request(friend_ip,challenge_msg:game_request):
        #Send challenge
        host = friend_ip # IP address of the server
        port = Client.CHALLENGE_PORT
        game=Game(is_host=True)
        
        #Send initial challenge object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)
        try:
            #Attempt connect to challenged ip
            client_socket.connect((host, port))
        except:
            print("Failed to send challenge! :(")
            return
        
        client_socket.settimeout(None)
        
        message = json.dumps(challenge_msg)
        client_socket.send(message.encode())
        client_socket.close()
        
        #Wait for connection back from challenged IP
        challenge_accepted= game.attempt_connection(Client.ip,Client.PLAY_ON_PORT,challenge_msg)

        if challenge_accepted:
            game.start(True)

    def execute(self):
        ip_to_challenge=input("Enter your friends IP address: ")
        name=input("Enter a name for your friend to see, or a message (: ")
        my_ip=Client.ip
        challenge=game_request(my_ip,name)
        ChallengeFriend.send_game_request(ip_to_challenge,challenge)
        
class ViewChallenges(MenuOption):
    def execute(self):
        print('"executed view"')
EXIT_STR="exit"
class ExitApp(MenuOption):
    DISPLAY_TEXT="Exit"
    def execute(self):
        return EXIT_STR
    
class Menu:
    MENU_HEADER="Hi, Welcome to P2PChess!\nOptions:"
    exit_requested=False
    def __init__(self,options):
        self.options=options

    def select(self,option_selection:str):
        try:
            choice = int(option_selection)
            if choice < 1 or choice > self.options.__len__():
                print("Invalid choice. Please select a valid option.")            
        except ValueError:
            print("Invalid input. Please enter a number.")
        try:
            option=self.options[choice-1]
            ret=option.execute()
            self.exit_requested=(ret==EXIT_STR)
        except Exception as e:
            print("Error in executing option")
            print(e)

    def display(self):
        print(Menu.MENU_HEADER)
        for i in range(self.options.__len__()):
            OPTION_TEXT=self.options[i].get_formatted_text(i+1)
            print(OPTION_TEXT)
    