class Tile:
    def __init__(self, x, y, piece=None):
        self.x = x
        self.y = y
        self.piece = piece
    def occupied(self):
        return self.piece==None
  
class ChessBoard:
    BLACK = 0
    WHITE = 1
    
    def __init__(self,user_color):
        self.user_color=user_color
        self.board = self.create_board()
        self.king_positions = {
            ChessBoard.WHITE: (7, 4),  # White king starts at e1
            ChessBoard.BLACK: (0, 4),  # Black king starts at e8
        }
        self.is_check = False

    def create_board(self):
        # Create an 8x8 chessboard using a list of lists
        board = [[Tile(x,y) for x in range(8)] for y in range(8)]

        # Place black pieces on the board
        board[0][0] = Tile(0, 0, Rook(ChessBoard.BLACK))
        board[0][1] = Tile(0, 1, Knight(ChessBoard.BLACK))
        board[0][2] = Tile(0, 2, Bishop(ChessBoard.BLACK))
        board[0][3] = Tile(0, 3, Queen(ChessBoard.BLACK))
        board[0][4] = Tile(0, 4, King(ChessBoard.BLACK))
        board[0][5] = Tile(0, 5, Bishop(ChessBoard.BLACK))
        board[0][6] = Tile(0, 6, Knight(ChessBoard.BLACK))
        board[0][7] = Tile(0, 7, Rook(ChessBoard.BLACK))

        for i in range(8):
            board[1][i] = Tile(1, i, Pawn(ChessBoard.BLACK))

        # Place white pieces on the board
        board[7][0] = Tile(7, 0, Rook(ChessBoard.WHITE))
        board[7][1] = Tile(7, 1, Knight(ChessBoard.WHITE))
        board[7][2] = Tile(7, 2, Bishop(ChessBoard.WHITE))
        board[7][3] = Tile(7, 3, Queen(ChessBoard.WHITE))
        board[7][4] = Tile(7, 4, King(ChessBoard.WHITE))
        board[7][5] = Tile(7, 5, Bishop(ChessBoard.WHITE))
        board[7][6] = Tile(7, 6, Knight(ChessBoard.WHITE))
        board[7][7] = Tile(7, 7, Rook(ChessBoard.WHITE))

        for i in range(8):
            board[6][i] = Tile(6, i, Pawn(ChessBoard.WHITE))

        return board

    # def display_board(self, color):
    #     # Handle printing the board for white or black pieces
    #     if color == ChessBoard.BLACK:
    #         pass
    #     else:
    #         pass

    #     # Display the chessboard
    #     for rank in self.board:
    #         rank_str=''
    #         for square in rank:
    #             if(square.piece==None):
    #                 rank_str+=' '
    #             else:
    #                 rank_str+=square.piece.symbol
    #         print(rank_str)
    def display_board(self):
        # ANSI escape codes for text color
        red_color = "\033[91m"  # Red for black pieces
        white_color = "\033[97m"  # White for white pieces
        reset_color = "\033[0m"  # Reset color to default

        # Define the column labels
        column_labels = "  a b c d e f g h"

        # Display the top border
        print("   " + "-" * 17)

        # Display the chessboard
        for row, rank in enumerate(self.board):
            rank_str = str(8 - row) + " |"
            for square in rank:
                if square.piece is None:
                    rank_str += '  '
                else:
                    piece_color = red_color if square.piece.get_color() == ChessBoard.BLACK else white_color
                    rank_str += piece_color + ' ' + square.piece.symbol + reset_color
            rank_str += " |"
            print(rank_str)

        # Display the bottom border and column labels
        print("   " + "-" * 17)
        print(column_labels)
    
    def decode_move(self, move_str):
        move_str = move_str.strip()
        move_dict = {
            'from': {},
            'dest': {}
        }

        # Check if the move string has a valid length (e.g., 'e4' or 'Nf3')
        if len(move_str) < 2:
            print("Invalid move: Too short.")
            return None

        # Extract the source and destination squares from the move string
        from_square = move_str[:-2]
        dest_square = move_str[-2:]

        # Check if the source and destination squares are valid
        if not self.is_valid_square(from_square) or not self.is_valid_square(dest_square):
            print("Invalid move: Invalid square notation.")
            return None

        move_dict['from']['row'], move_dict['from']['col'] = self.square_to_coordinates(from_square)
        move_dict['dest']['row'], move_dict['dest']['col'] = self.square_to_coordinates(dest_square)

        return move_dict

    def is_valid_square(self, square):
        # Check if the square notation is valid (e.g., 'a1' to 'h8')
        if len(square) != 2:
            return False
        file, rank = square[0], square[1]
        return file in 'abcdefgh' and rank in '12345678'

    def square_to_coordinates(self, square):
        # Convert square notation (e.g., 'e4') to row and column indices
        file, rank = square[0], square[1]
        row = 8 - int(rank)
        col = ord(file) - ord('a')
        return row, col

    def move(self, move_str):#Eg of a move is Ne4
        move_decoded = self.decode_move(move_str)
        if move_decoded is None:
            return False
        starting_row=move_decoded['from']['row']
        starting_col=move_decoded['from']['col']
        destination_row=move_decoded['dest']['row']
        destination_column=move_decoded['dest']['col']
        #Get tiles
        start_tile=self.board[starting_row][starting_col]
        dest_tile=self.board[destination_row][destination_column]
        #Get the piece we are moving
        piece=self.board[destination_row][starting_col].piece
        if(piece.color != self.user_color):
            print("You can only move your own pieces!!!")
            return False
        if not piece.validate_move(self, start_tile,dest_tile):
            return False

        # Place a chess piece on the board
        if 0 <= destination_row < 8 and 0 <= destination_column < 8:
            self.board[destination_row][destination_column].piece = piece
            
        else:
            print("Invalid position")
              # Check if the move puts the opponent's king in check
        opponent_color = 1 - self.user_color
        if self.is_in_check(opponent_color):
            print("Check!")
        return True
    
    def update_king_position(self, color, row, col):
        # Update the position of the king for the specified color
        if self.board[row][col].piece.symbol == 'K':
            self.king_positions[color] = (row, col)

    def is_in_check(self, color):
        # Check if the king of the specified color is in check
        king_row, king_col = self.king_positions[color]

        # Iterate through all opponent's pieces and see if any can attack the king
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col].piece
                if piece is not None and piece.color != color:
                    if piece.validate_move(self, row, col, king_row, king_col):
                        return True
        return False

    def capture_piece(self, row, col):
        # Remove a chess piece from the board
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col].piece = None
        else:
            print("Invalid position")

class Piece:
    def __init__(self, color):
        self.color = color  
        self.symbol='%'
    def validate_move():
        print("VALIDATION NOT IMPLEMENTED")
        return False
    #Defaults to piece is not obstructed and the only spot it has to go is its dest
    """In all inherited classes, this is only to be called after validation, other wise the logic will not work
        Returns a list of dicts of x,y to check representing tiles
    """
    def get_piece_path(self,start:Tile,dest:Tile):
        return [dest]
    def get_color(self):
        return self.color

    def __str__(self):
        return self.symbol

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'P'
    def validate_move(self,current:Tile,new:Tile):
        # Calculate the direction of movement based on pawn color
        direction = 1 if self.color == ChessBoard.WHITE else -1

        # Check if the move is within the bounds of the board
        if new.x < 0 or new.x > 7 or new.y < 0 or new.y > 7:
            return False

        # Pawn's initial double move
        if current.x == 1 and new.x == 3 and direction == 1 and current.y == new.y:
            return not new.occupied() #Allowed if free space
        if current.x == 6 and new.x == 4 and direction == -1 and current.y == new.y:
            return not new.occupied() #Allowed if free space

        # Regular pawn move (one square forward)
        if new.x == current.x + direction and new.y == current.y:
            return not new.occupied() #Allowed if free space

        # Pawn capture (diagonal)
        if (new.x == current.x + direction and
            (new.y == current.y + 1 or new.y == current.y - 1)):
            return new.occupied()
        
        # Invalid move
        return False

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'R'
    
    def get_piece_path(self,start:Tile,dest:Tile):
        path=[]
        if start.x == dest.x: #If vertical move
            #Add or subtract to get next space from start
            dir=-1
            if start.y<dest.y:
                dir=1
            #Number of iterations    
            diff=abs(dest.y-start.y)
            #Gets path of piece, excluding start and end
            for i in range(diff):
                if i==0:#Ignore start tile
                    continue
                #Does not need to return 
                coords={'x':start.x, 'y':start.y+(i*dir)}
                path.append(coords)

        elif start.y == dest.y: #If horizontal move
            #Add or subtract to get next space from start
            dir=-1
            if start.x<dest.x:
                dir=1
            #Number of iterations    
            diff=abs(dest.x-start.x)
            #Gets path of piece, excluding start and end
            for i in range(diff):
                if i==0:#Ignore start tile
                    continue
                #Does not need to return 
                coords={'x':start.x+(i*dir), 'y':start.y}
                path.append(coords)
            pass
        else:
            print("Failed rook get piece path")
            raise Exception
        

        return [dest]
    
    def validate_move():

        return 
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
