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
    def __del__(self):
        self.finalize_connection()
    def finalize_connection(self):
        try:
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except Exception as e:
            print(e)
    def listen_for_accept(self,*args):
        host=args[0]
        friend=args[1]
        port=args[2]
        # self.server_socket.shutdown(socket.SHUT_RDWR)#Shutdown server if up
        self.server_socket.bind((host, port))

        while not self.is_cancelled():
            self.server_socket.listen(2)  # Allow one incoming connection

            #Stop none issues
            client_socket=None
            client_address=None
            
            try:
                client_socket, client_address = self.server_socket.accept()
            except OSError as e:
                continue
            
            if(client_address[0]==friend and not self.is_cancelled()):
                self.active_connection=True
                self.client_socket=client_socket
                print("\nMatch connection succeeded. Enter anything to continue...")
                return                   
            else:
                if client_socket:
                    client_socket.close()
                    
            if(self.is_cancelled()):
                print("Challenge cancelled")

        if(not self.active_connection or self.is_cancelled()):
            self.server_socket.close()
        
    #Returns true on success, false on fail or cancel
    def attempt_connection(self,port,host_ip,friend_ip):
        #Start listening for response to challenge
        socket_proc=Thread(target=self.listen_for_accept,args=[host_ip,friend_ip,port])
        socket_proc.daemon=True
        socket_proc.start()

        #Wait for user input, if entered in time, connection will be cancelled. Otherwise user prompted to enter to continue
        input("Enter anything to attempt to cancel: ")
        if(socket_proc.is_alive()):
            self.cancel()
            if self.server_socket:#if not None
                try:
                    self.server_socket.shutdown(socket.SHUT_RDWR)
                    self.server_socket.close()
                except:
                    pass
            print("Cancel succeeded")
        socket_proc.join()

        return self.client_socket!=None 
    def attempt_connection_to_server(self,port,challenge:game_request):
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



class Game:
    def __init__(self,is_host):
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

    # """If challenge"""
    # def attempt_connection(self,port,host_on=None,friend_ip=None,challenge:game_request=None):
    #     if challenge==None:
    #         #If this returns and it was cancelled, it means connection didn't happen
    #         #If it is not cancelled and returns, action must have succeeded
    #         return self.connection_handler.attempt_connection(port,host_on,friend_ip)
    #     else:
    #         return self.connection_handler.attempt_connection_to_server(port,challenge)
        
    def await_challenge_response(self,port:str,host_on:str,friend_ip:str):
        return self.connection_handler.attempt_connection(port,host_on,friend_ip)   
    def respond_to_challenge(self,port:str,challenge:game_request):
        return self.connection_handler.attempt_connection_to_server(port,challenge)
    
    def is_game_over(self,mate_is_loss:bool):
        #Possible bug here
        board_state=self.board.is_checkmate_or_stalemate(self.board.user_color)
        result_msg=""
        if board_state == None:
            return False
        elif board_state=="CM":
            result_msg="Checkmate! "
            if(mate_is_loss):
                result_msg+="You lose :("
            else:
                result_msg+="You win!!!"
        elif board_state=="SM":
           result_msg="Stalemate... Awkkkwarddddd..."
        
        print(result_msg)
        return True
    def start(self):
        self.is_users_turn=(self.board.user_color==ChessBoard.WHITE)
        self.board.display_board()
        print("Starting game!!!")

        while not self.game_over:
            if(self.is_users_turn):
                valid_move=False
                while not valid_move:
                    move = input("Enter your move, or 'quit' to quit: ")
                
                    if move.lower() == 'quit':
                        self.game_over=True
                        break
                    valid_move=self.board.move(move)
                #Once again check if game is over
                if self.is_game_over(mate_is_loss=False):
                    self.game_over=True
                    
                self.connection_handler.client_socket.settimeout(30)
                try:
                    self.connection_handler.client_socket.send(move.encode())
                except TimeoutError:
                    print("Error! Connection timed out. Game over...")
                    return
                self.connection_handler.client_socket.settimeout(None)
                #End turn
                self.is_users_turn=not self.is_users_turn
                if self.is_game_over(mate_is_loss=False):
                    self.game_over=True
            else:
                print("Wait for your opponents move...")
                resp=self.connection_handler.client_socket.recv(1028).decode()
                print(resp)
                self.board.move(resp,True)
                #Check if the last move you received ended your game
                if self.is_game_over(mate_is_loss=True):
                    self.game_over=True
                self.is_users_turn=not self.is_users_turn
            self.board.display_board()
        