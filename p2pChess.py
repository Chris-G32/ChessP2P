from menu import Menu,ChallengeFriend,ViewChallenges,ExitApp,Client
from chessboard import ChessBoard
import multiprocessing
from threading import Thread
import signal
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
    # board=ChessBoard()
    # board.display_board(ChessBoard.WHITE)
    # board.

    # exit()
    #Iniitialize shutdown handlers
    # signal.signal(signal.SIGINT, handle_shutdown)
    # signal.signal(signal.SIGTERM,handle_shutdown)
    #Starting background server to listen for challenges
    challenge_listener = Thread(target = Client.start_server)
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
        except:
            error_count+=1
            if(error_count>=MAX_CONSECUTIVE_LOOP_ERRORS):
                print("Application errored too many times. Attempting to clean up and exit..,")
                should_exit=True
    #Shutdown server
    Client.shutdown_server()
    challenge_listener.join()
    # challenge_listener.join()
    print("Resources cleaned up...")
    print("Exiting...")
    