import chessboard

board_1=chessboard.ChessBoard(chessboard.ChessBoard.WHITE)
board_2=chessboard.ChessBoard(chessboard.ChessBoard.BLACK)
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
    board_2.display_board()
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
    board_1.display_board()
    
    # print(state)
    if state=="CM":
        print("Checkmate! Black wins")
        exit()
    elif state=="SM":
        print("Stalemate")
        exit()