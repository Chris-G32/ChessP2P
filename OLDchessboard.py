class Tile:
    def __init__(self,x,y,piece=None):
        self.x=x
        self.y=y
        piece=piece

class ChessBoard:
    BLACK=0
    WHITE=1
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        # Create an 8x8 chessboard using a list of lists
        board = [[None for _ in range(8)] for _ in range(8)]
        
        return board

    def display_board(self,color):
        #Handle printing board for white or black pieces
        if(color==ChessBoard.BLACK):
            pass
        else:
            pass

        # Display the chessboard
        for row in self.board:
            print(' '.join(row))

    def place_piece(self, piece, row, col):
        # Place a chess piece on the board
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
        else:
            print("Invalid position")

    def remove_piece(self, row, col):
        # Remove a chess piece from the board
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = ' '
        else:
            print("Invalid position")

# Example usage:
# chessboard = ChessBoard()
# chessboard.display_board()
# chessboard.place_piece('K', 0, 0)
# chessboard.place_piece('p', 6, 4)
# chessboard.display_board()


class Piece:
    def __init__(self, color):
        self.color = color  # 'W' for white, 'B' for black
        self.symbol='%'
    def validate_move():
        print("VALIDATION NOT IMPLEMENTED")
        return False

    def get_color(self):
        return self.color

    def __str__(self):
        return self.symbol

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'P'
    def validate_move(current,new):
        if
        return False

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'R'

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'N'

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'B'

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'Q'

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'K'

# Example usage:
# white_pawn = Pawn('W')
# black_rook = Rook('B')

# print(f"White pawn: {white_pawn.get_color()} {white_pawn}")
# print(f"Black rook: {black_rook.get_color()} {black_rook}")
