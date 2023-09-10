class Tile:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
    def occupied(self):
        return self.piece!=None
class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)
 
    def style_text(code):
        return "\33[{code}m".format(code=code)
 
    def color_text(code):
        return "\33[{code}m".format(code=code)  
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
        board = [[Tile(row,col) for col in range(8)] for row in range(8)]

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
    def alternate_background(background):
        if background==47:
            background=40
        else:background=47
        return background

    def display_board(self):
        # ANSI escape codes for text color
        red_color = "\033[31m"  # Red for black pieces
        blue_color = "\033[96m"  # White for white pieces
        reset_color = "\033[0m"  # Reset color to default

        # Define the column labels
        column_labels = "    a b c d e f g h"

        # Display the top border
        print("   " + "-" * 17)

        white_first=True
        # Display the chessboard
        for row, rank in enumerate(self.board):
            rank_str = str(8 - row) + " |"
            background=40
            if white_first:
                background=47
            for square in rank:
                if square.piece is None:
                    rank_str +=ANSI.background(background)+ '  '
                else:
                    piece_color = red_color if square.piece.get_color() == ChessBoard.BLACK else blue_color
                    rank_str += ANSI.background(background)+piece_color + ' ' + square.piece.symbol + reset_color
                background=ChessBoard.alternate_background(background)
            rank_str += ANSI.background(49)+" |"
            print(rank_str)
            white_first=not white_first

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
        return rank in '12345678' and file in 'abcdefgh'

    def square_to_coordinates(self, square):
        # Convert square notation (e.g., 'e4') to row and column indices
        file, rank = square[0], square[1]
        row = 8-int(rank) #Decrement here to keep in range 0-7
        col = ord(file) - ord('a')
        return row, col

    def full_move_validation(self,start_tile:Tile,dest_tile:Tile):
        #Get the piece we are moving
        piece=start_tile.piece
        if piece == None:
            print(f"No piece at that starting square!")
            return False
        if(piece.color != self.user_color):
            print("You can only move your own pieces!!!")
            return False
        if not piece.validate_move(start_tile,dest_tile):
            return False
        if self.path_obstructed(piece.get_piece_path(start_tile,dest_tile)):
            print("Can't make this move, there are pieces in the way.")
            return False
        if dest_tile.piece!=None:
            if dest_tile.piece.color==self.user_color:
                print("Can't capture your own pieces!!!")
                return False
        return True
    def full_move_validation_for_checks(self,start_tile:Tile,dest_tile:Tile):
        #Get the piece we are moving
        piece=start_tile.piece
        if piece == None:
            return False
        # if(piece.color != self.user_color):
        #     return False
        if not piece.validate_move(start_tile,dest_tile):
            return False
        if self.path_obstructed(piece.get_piece_path(start_tile,dest_tile)):
            return False
        if dest_tile.piece!=None:
            if dest_tile.piece.color==self.user_color:
                return False
        return True    
    def make_move(self,start_tile,dest_tile):
        self.board[dest_tile.row][dest_tile.col].piece=start_tile.piece
        self.board[start_tile.row][start_tile.col].piece =None
        
    def move(self, move_str,receiving_move=False):#Eg of a move is Ne4
        
        move_decoded = self.decode_move(move_str)
        if move_decoded is None:
            return False
        starting_row=move_decoded['from']['row']
        starting_col=move_decoded['from']['col']
        destination_row=move_decoded['dest']['row']
        destination_col=move_decoded['dest']['col']
        
        #Get tiles
        start_tile=self.board[starting_row][starting_col]
        dest_tile=self.board[destination_row][destination_col]
        if receiving_move:
            self.make_move(start_tile,dest_tile)
            return True
        if(self.full_move_validation(start_tile,dest_tile)==False):
            return False
        #Check if move puts themself in check
        self.make_move(start_tile,dest_tile)
        if self.is_in_check(self.user_color):
            print("Can't move yourself into check!")
            #Undo move if it puts yourself in check
            self.make_move(dest_tile,start_tile)
            return False
        
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
        king_tile=self.board[king_row][king_col]
        # Iterate through all opponent's pieces and see if any can attack the king
        for row in range(8):
            for col in range(8):
                tile=self.board[row][col]
                piece = tile.piece
                if piece is not None and piece.color != color:
                    if self.full_move_validation_for_checks(tile,king_tile):
                        return True
        return False
    #Takes a list of x and y's to conver to tiles
    def path_obstructed(self,crossed_tiles:list):
        if len(crossed_tiles)==0:
            return False
        for i in crossed_tiles:
            tile=self.board[i['row']][i['col']]
            if tile.occupied():
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
        return []
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
        direction = -1 if self.color == ChessBoard.WHITE else 1

        # Check if the move is within the bounds of the board
        if new.row < 0 or new.row > 7 or new.col < 0 or new.col > 7:
            return False

        # Pawn's initial double move
        if current.row == 1 and new.row == 3 and direction == 1 and current.col == new.col:
            return not new.occupied() #Allowed if free space
        if current.row == 6 and new.row == 4 and direction == -1 and current.col == new.col:
            return not new.occupied() #Allowed if free space

        # Regular pawn move (one square forward)
        if new.row == current.row + direction and new.col == current.col:
            return not new.occupied() #Allowed if free space

        # Pawn capture (diagonal)
        if (new.row == current.row + direction and
            (new.col == current.col + 1 or new.col == current.col - 1)):
            return new.occupied()
        
        # Invalid move
        return False

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'R'
    
    def get_piece_path(self,start:Tile,dest:Tile):
        path = []

        # Calculate the direction and number of iterations based on the move direction
        if start.row == dest.row:  # Vertical move
            dir_y = 1 if start.col < dest.col else -1
            diff_y = abs(dest.col - start.col)

            for i in range(1, diff_y):  # Exclude start and end
                path.append({'row': start.row, 'col': start.col + i * dir_y})

        elif start.col == dest.col:  # Horizontal move
            dir_x = 1 if start.row < dest.row else -1
            diff_x = abs(dest.row - start.row)

            for i in range(1, diff_x):  # Exclude start and end
                path.append({'row': start.row + i * dir_x, 'col': start.col})

        else:
            print("Failed rook get piece path")
            raise Exception

        return path
        
    def validate_move(self,start:Tile,dest:Tile):
        # Rook move validation
        if start.row == dest.row or start.col == dest.col:
            return True
        return False
        
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'N'
    def validate_move(self,start:Tile,dest:Tile):
        # Knight move validation
        row_diff = abs(dest.row - start.row)
        col_diff = abs(dest.col - start.col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'B'

    def validate_move(self, start:Tile,dest:Tile):
        # Bishop move validation
        row_diff = abs(dest.row - start.row)
        col_diff = abs(dest.col - start.col)
        return row_diff == col_diff
    
    def get_piece_path(self, start: Tile, dest: Tile):
        path = []

        # Calculate the direction for row and column
        row_dir = 1 if dest.row > start.row else -1
        col_dir = 1 if dest.col > start.col else -1

        # Determine the number of iterations (squares to move diagonally)
        num_iterations = abs(dest.row - start.row)

        for i in range(1, num_iterations):
            path.append({'row': start.row + i * row_dir, 'col': start.col + i * col_dir})

        return path
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'Q'

    def validate_move(self, start:Tile,dest:Tile):
        # Queen move validation (combines Rook and Bishop moves)
        if start.row == dest.row or start.col == dest.col:
            return True
        row_diff = abs(dest.row - start.row)
        col_diff = abs(dest.col - start.col)
        return row_diff == col_diff
    def get_piece_path(self, start: Tile, dest: Tile):
        path = []
        #Rook like
        if start.row == dest.row or start.col == dest.col:
            # Calculate the direction and number of iterations based on the move direction
            if start.row == dest.row:  # Vertical move
                dir_y = 1 if start.col < dest.col else -1
                diff_y = abs(dest.col - start.col)

                for i in range(1, diff_y):  # Exclude start and end
                    path.append({'row': start.row, 'col': start.col + i * dir_y})

            elif start.col == dest.col:  # Horizontal move
                dir_x = 1 if start.row < dest.row else -1
                diff_x = abs(dest.row - start.row)

                for i in range(1, diff_x):  # Exclude start and end
                    path.append({'row': start.row + i * dir_x, 'col': start.col})

            else:
                print("Failed queen get piece path")
                raise Exception
        #Bishop like
        else: 
            # Calculate the direction for row and column
            row_dir = 1 if dest.row > start.row else -1
            col_dir = 1 if dest.col > start.col else -1

            # Determine the number of iterations (squares to move diagonally)
            num_iterations = abs(dest.row - start.row)

            for i in range(1, num_iterations):
                path.append({'row': start.row + i * row_dir, 'col': start.col + i * col_dir})
            pass
        return path
    
class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'K'
    def validate_move(self, start:Tile,dest:Tile):
        row_diff = abs(dest.row - start.row)
        col_diff = abs(dest.col - start.col)
        if row_diff<=1 and col_diff<=1:
            return True
        return False
    