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
    
    def listen_for_accept(self,*args):
        host=args[0]
        port=args[1]
        challenge=args[2]


        self.server_socket.bind((host, port))

        while not self.is_cancelled() and not self.active_connection:
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
        time.sleep(2)
        #Wait for user input, if entered in time, connection will be cancelled. Otherwise user prompted to enter to continue
        input("Enter anything to attempt to cancel: ")
        if(socket_proc.is_alive()):
            self.cancel()
            # socket_proc.terminate()
            if self.server_socket:#if not None
                self.server_socket.shutdown(socket.SHUT_RDWR)
            print("Cancel succeeded")

        socket_proc.join()

        return self.active_connection


        
#Note, need to make 
# class CancellableAction:
#     def __init__(self,target,args):
#         self.target=target
#         self.args=args
#         self.cancelled=False
#         # self.action=None
    # def listen_cancel(self):
        # try:
        #     input("Enter anything to cancel, if connection is already made enter whatever: ")
        #     print("Post input")
        #     self.cancelled=True
        # except:
        #     pass
    
#     def run(self,cancel_check_interval=0.5):
#         #Thread for the action
#         action=multiprocessing.Process(target=self.target,args=self.args)
#         action.daemon=True
#         #Used process to be able to actually terminate it, threading doesn't allow this, defaults to console input
#         input_proc=multiprocessing.Process(target=self.listen_cancel)
#         input_proc.daemon=True
#         #Run threads
#         input_proc.start()
#         action.start()

#         while (action.is_alive() and not self.cancelled):
#             time.sleep(cancel_check_interval)
#         action.terminate()
#         input_proc.terminate()
#         action.join()
#         input_proc.join()
        
        

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
        self.server_socket=None
        self.client_socket=None
    def await_opponent_move(self):
        while not self.is_users_turn:
            time.sleep(1)
    
    def attempt_connection(self,host,port,challenge:game_request):
        #If this returns and it was cancelled, it means connection didn't happen
        #If it is not cancelled and returns, action must have succeeded
        return self.connection_handler.attempt_connection(host,port,challenge)
    # def await_accept(self,host,port,challenge:game_request):
    #     #Handle where it should cancel request in here

    #     #Now waits for the challenge to be accepted
    #     self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.server_socket.bind((host, port))
    #     connected=False
    #     try:
    #         while not connected:
    #             self.server_socket.listen(1)  # Allow one incoming connection
    #             print("Waiting for challenge to be accepted...")

    #             client_socket, client_address = self.server_socket.accept()
                
    #             if(client_address==challenge.ip):
    #                 connected=True
                    
    #                 self.client_socket=client_socket
    #                 return True
    #             else:
    #                 client_socket.close()
    #         # client_socket.close()
    #     except Exception as e:
    #         print(f"Error: {e}")
    #     self.server_socket.close()
    #     return False
        
    def start(self,is_users_turn):
        self.is_users_turn=is_users_turn
        while not self.game_over:
            self.board.display_board()
            
            move=input("Select piece to move")