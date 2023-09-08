from typing import Any
from chessboard import ChessBoard
from game_request import game_request
from threading import Thread
import multiprocessing
import time
import socket
import os
import signal

from cancellable_action import CancellableAction

class GameConnectionHandler(CancellableAction):
    def __init__(self):
        super().__init__()
        self.active_connection=False
        self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket=None
    
    def listen_for_accept(self,*args):
        host=args[0]
        port=args[1]
        challenge=args[2]

        self.server_socket.bind((host, port))

        while not self.is_cancelled():
            self.server_socket.listen(2)  # Allow one incoming connection

            #Stop none issues
            client_socket=None
            client_address=''
            
            try:
                client_socket, client_address = self.server_socket.accept()
            except OSError:
                pass

            if(client_address==challenge.ip and not self.is_cancelled()):
                self.active_connection=True
                self.client_socket=client_socket
                print("Match connection succeeded. Enter anything to continue...")
                return                   
            else:
                if client_socket:
                    client_socket.close()
                    
            if(self.is_cancelled()):
                print("Challenge cancelled")

        if(not self.active_connection or self.is_cancelled()):
            self.server_socket.close()
        
    #Returns true on success, false on fail or cancel
    def attempt_connection(self,host,port,challenge:game_request):
        #Start listening for response to challenge
        socket_proc=Thread(target=self.listen_for_accept,args=[host,port,challenge])
        socket_proc.daemon=True
        socket_proc.start()

        #Wait for user input, if entered in time, connection will be cancelled. Otherwise user prompted to enter to continue
        input("Enter anything to attempt to cancel: ")
        if(socket_proc.is_alive()):
            self.cancel()
            if self.server_socket:#if not None
                self.server_socket.shutdown(socket.SHUT_RDWR)
            print("Cancel succeeded")

        socket_proc.join()

        return self.client_socket!=None 
    def attempt_connection_to_server(self,host,port,challenge:game_request):
        self.client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(30)
        try:
            self.client_socket.connect((challenge.ip,port))
            self.client_socket.settimeout(None)
            return True
        except ConnectionRefusedError:
            print("Connection was refused. Server may be down or unreachable.")
        except Exception as e:
            print(f"An error occurred while connecting: {str(e)}")
        return False


# import asyncio
class Game:
    def __init__(self,is_host=False):
        if is_host:
            user_color=ChessBoard.WHITE
        else:
            user_color=ChessBoard.BLACK
        self.connection_handler=GameConnectionHandler()
        self.board=ChessBoard(user_color)
        self.game_over=False
        self.is_users_turn=None

    def await_opponent_move(self):
        while not self.is_users_turn:
            time.sleep(1)

    def attempt_connection(self,host,port,challenge:game_request,is_host):
        if is_host:
            #If this returns and it was cancelled, it means connection didn't happen
            #If it is not cancelled and returns, action must have succeeded
            return self.connection_handler.attempt_connection(host,port,challenge)
        elif not is_host:
            return self.connection_handler.attempt_connection_to_server(host,port,challenge)
        
        
    def start(self,is_users_turn):
        self.is_users_turn=is_users_turn
        while not self.game_over:
            while True:
                message = input("Enter a message or 'exit' to exit: ")
                if message.lower() == 'exit':
                    self.game_over=True
                if(self.is_users_turn):
                    self.connection_handler.client_socket.send(message.encode())
                    #End turn
                    self.is_users_turn=not self.is_users_turn
                else:
                    print("Not your turn... Please wait for a response")

            # self.board.display_board()
            
            # move=input("Select piece to move")