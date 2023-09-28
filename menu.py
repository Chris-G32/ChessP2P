
import socket
from game_request import game_request
import json
import collections
from game import Game
from datetime import datetime
import psutil
from bson import json_util

def get_first_non_local_address():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                return addr.address
    return None

received_requests=[]
class Client:
    CHALLENGE_PORT=12345
    PLAY_ON_PORT=12346
    ip=get_first_non_local_address()
    keep_listening=False
    server_up=False
    server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def add_request(game_req:game_request):
        global received_requests
        received_requests.append(game_request(game_req.ip,game_req.user,game_req.timestamp))
        if received_requests.__len__()>10:
            received_requests.pop(0)
        
    def shutdown_server():
        Client.server_socket.shutdown(socket.SHUT_RDWR)
        print("Shutting down server...")
        Client.keep_listening=False
    def start_server():
        Client.keep_listening=True
        Client.server_up=True
        host = Client.ip  
        port = Client.CHALLENGE_PORT
        
        try:
            # server_socket=Client.server_socket
            # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Client.server_socket.bind((host, port))
            Client.server_socket.listen(10)  # Allow ten incoming connection

            # print("Waiting for a connection...")

            while Client.keep_listening:
                try:
                    client_socket, client_address = Client.server_socket.accept()
                    data = client_socket.recv(2048).decode()
                except OSError:
                    print("Server shut down!")
                    return

                try:
                    tmp_dict=json.loads(data,object_hook=json_util.object_hook)
                    challenge=game_request(**tmp_dict)
                    Client.add_request(challenge)
                except (ValueError , TypeError):
                    data_copy=data
                    data_copy.replace("\n",'')
                    # Handle the exception
                    with open('invalid_requests.log', 'a') as file:
                        log_str=f"Invalid challenge request from {client_address[0]} over port {client_address[1]}, Received: {data_copy}"
                        file.writelines(log_str)

                if not data:
                    break
                client_socket.close()
        except Exception as e:
            print(e)
            # print("--error in challenge listener, please restart app--")
            
        Client.server_socket.close()
        Client.server_up=False
    
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
        except Exception as e:
            print(e)
            return
        
        client_socket.settimeout(None)
        
        message = json.dumps(challenge_msg.__dict__,default=json_util.default)
        client_socket.send(message.encode())
        client_socket.close()
        
        #Wait for connection back from challenged IP
        challenge_accepted= game.await_challenge_response(Client.PLAY_ON_PORT,Client.ip,friend_ip)

        if challenge_accepted:
            game.start()

    def execute(self):
        ip_to_challenge=input("Enter your friends IP address: ")
        name=input("Enter a name for your friend to see, or a message (: ")
        my_ip=Client.ip
        challenge=game_request(my_ip,name)
        ChallengeFriend.send_game_request(ip_to_challenge,challenge)
        
class ViewChallenges(MenuOption):
    DISPLAY_TEXT="View Incoming Challenges"
    #Returns none on invalid input
    def validate_input(self,inp:str,max_val:int):
        try:
            inp=int(inp)
        except ValueError:
            print("Please enter an integer number")
            return None
        if inp<0 or inp>max_val:
            print(f"Enter a number between 0 and {max_val}")
            return None
        
        return inp
    def accept_challenge(challenge:game_request):
        game=Game(is_host=False)
        challenge_connected=game.respond_to_challenge(Client.PLAY_ON_PORT,challenge=challenge)
        if challenge_connected:
            game.start()
        else:
            print("Failed to accept challenge")
    def execute(self):
        global received_requests
        #Check not empty
        if received_requests.__len__()<1:
            print("No challenges...")
            return
        
        #Get requests that are too old
        remove_candidates=[]
        for i in received_requests:
            REQUEST_EXPIRE_TIME_SECONDS=60*4#4 minutes
            time_since_received=(datetime.now()-i.timestamp).total_seconds()
            if time_since_received>REQUEST_EXPIRE_TIME_SECONDS:
                remove_candidates.append(i)

        #Remove old requests
        for i in remove_candidates:
            received_requests.remove(i)
        
        #Check again that all requests weren't expired
        if received_requests.__len__()<1:
            print("No challenges...")
            return
        
        #Display to user
        print("\t0: Exit")
        count=1
        for i in received_requests:
            print(f"\t{count}: {i.ip} - {i.user}")
            count+=1

        selection=None
        while selection==None:
            selection=input("Enter the challenges number to accept, or 0 to go back: ")
            selection=self.validate_input(selection,count)

        if selection>0:
            ViewChallenges.accept_challenge(received_requests[selection-1])
        
        
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
        
        option=self.options[choice-1]
        ret=option.execute()
        self.exit_requested=(ret==EXIT_STR)
        

    def display(self):
        print(Menu.MENU_HEADER)
        for i in range(self.options.__len__()):
            OPTION_TEXT=self.options[i].get_formatted_text(i+1)
            print(OPTION_TEXT)
    