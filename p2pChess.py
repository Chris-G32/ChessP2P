from menu import Menu,ChallengeFriend,ViewChallenges,ExitApp,Client
from chessboard import ChessBoard
from threading import Thread
import time
def create_menu():
    options=[ChallengeFriend(),ViewChallenges(),ExitApp()]
    return Menu(options=options)

shutdown_received=False
def handle_shutdown():
    shutdown_received=True
    Client.shutdown_server()
    while Client.server_up:
        time.sleep(0.5)
    print("Process exited gracefully")


if __name__=="__main__":
    #Starting background server to listen for challenges
    challenge_listener = Thread(target = Client.start_server,daemon=True)
    challenge_listener.start()

    MENU=create_menu()
    MAX_CONSECUTIVE_LOOP_ERRORS=15
    should_exit=False
    error_count=0
    
    while(not MENU.exit_requested and not shutdown_received):
        try:
            MENU.display()
            print(f"Your IP: {Client.ip}")
            MENU.select(input("Enter an option: "))
            error_count=0
        except KeyboardInterrupt:
            print("\nTerminating process...")
            break
        except:
            error_count+=1
            if(error_count>=MAX_CONSECUTIVE_LOOP_ERRORS):
                print("Application errored too many times. Attempting to clean up and exit..,")
                should_exit=True
        
    Client.shutdown_server()
    challenge_listener.join()

    #Shutdown server
    print("Exiting...")
    