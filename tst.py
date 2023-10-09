import chessboard
from chessboard import ChessBoard
def parse_chessboard_string(chessboard_string:str):
    chessboard_array = []
    chessboard_string=chessboard_string.replace("[","")
    chessboard_string=chessboard_string.replace("]","")
    chessboard_string=chessboard_string.replace('"',"")
    chars = chessboard_string.strip().split(", ")

    row_data=[]
    count=0
    for i in chars:
        if count%4==0 and not count==0:
            chessboard_array.append(row_data)
            row_data=[]
        try:
            i=int(i)
        except ValueError:
            pass
        row_data.append(i)
        count+=1
    return chessboard_array

board_ob='[[0, 0, "R", 0], [0, 1, "N", 0], [0, 2, "B", 0], [0, 3, "Q", 0], [0, 4, "K", 0], [0, 5, "B", 0], [0, 6, "N", 0], [0, 7, "R", 0], [1, 0, "P", 0], [1, 1, "P", 0], [1, 2, "P", 0], [1, 5, "P", 0], [1, 6, "P", 0], [1, 7, "P", 0], [2, 4, "P", 1], [6, 0, "P", 1], [6, 1, "P", 1], [6, 2, "P", 1], [6, 3, "P", 1], [6, 5, "P", 1], [6, 6, "P", 1], [6, 7, "P", 1], [7, 0, "R", 1], [7, 1, "N", 1], [7, 2, "B", 1], [7, 3, "Q", 1], [7, 4, "K", 1], [7, 5, "B", 1], [7, 6, "N", 1], [7, 7, "R", 1]]'
parsed=parse_chessboard_string(board_ob)
board_1=ChessBoard(ChessBoard.WHITE)
board_1.load_board_from_array(parsed)
board_2=ChessBoard(ChessBoard.BLACK)
board_2.load_board_from_array(parsed)
board_1.display_board()
while True:
    move_1_valid=False
    move_1=""
    while move_1_valid==False:
        move_1=input("enter move for white: ")
        move_1_valid=board_1.move(move_1)
    board_2.move(move_1,True)
    state=board_2.is_checkmate_or_stalemate(board_2.user_color)
    # print(state)
    board_1.display_board()
    if state=="CM":
        print("Checkmate! White wins")
        exit()
    elif state=="SM":
        print("Stalemate")
        exit()
    
    move_2_valid=False
    move_2=""
    while move_2_valid==False:
        move_2=input("enter move for black: ")
        move_2_valid=board_2.move(move_2)
    board_1.move(move_2,True)
    state=board_1.is_checkmate_or_stalemate(board_1.user_color)
    board_2.display_board()
    
    # print(state)
    if state=="CM":
        print("Checkmate! Black wins")
        exit()
    elif state=="SM":
        print("Stalemate")
        exit()

