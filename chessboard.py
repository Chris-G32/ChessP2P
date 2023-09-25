from copy import deepcopy
class Tile:
    def __init__(self, row, col=None, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
    def occupied(self):
        return self.piece!=None
#Utility class for coloring text
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
    class MoveDecoder:
        def __init__(self,chessboard):
            self.chessboard=chessboard
            """Translates a move string into the starting tile and destination tile. Returns a tuple of start tile then destination"""
        def decode_move(self, move_str):
            start_tile=None
            dest_tile=None

            move_str = move_str.strip()
            
            move_dict = {
                'from': {},
                'dest': {}
            }
            
            # Check if the move string has a valid length (e.g., 'e4' or 'Nf3')
            if len(move_str) < 2:
                print("Invalid move: Too short.")
                return start_tile,dest_tile

            # Extract the source and destination squares from the move string
            from_square = move_str[:-2]
            dest_square = move_str[-2:]

            # Check if the source and destination squares are valid
            if not self.is_valid_square(from_square) or not self.is_valid_square(dest_square):
                print("Invalid move: Invalid square notation.")
                return start_tile,dest_tile

            from_row,from_col=self.square_to_coordinates(from_square)
            to_row,to_col=self.square_to_coordinates(dest_square)
            
            #Get tiles
            start_tile=self.chessboard.get_tile(from_row,from_col)
            dest_tile=self.chessboard.get_tile(to_row,to_col)

            return start_tile,dest_tile

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
    
    def __init__(self,user_color):
        self.user_color=user_color
        
        self.king_positions = {
            ChessBoard.WHITE: (7, 4),  # White king starts at e1
            ChessBoard.BLACK: (0, 4),  # Black king starts at e8
        }
        self.move_decoder=ChessBoard.MoveDecoder(self)
        self.move_buffer=[]#Contains the updated tiles on a given move
        self.white_pawns=[]#Used to store all the pawns to handle en passant
        self.black_pawns=[]
        self.board = self.create_board()
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
            self.black_pawns.append(board[1][i])

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
            self.white_pawns.append(board[6][i])

        return board
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


    
    def full_move_validation(self,start_tile:Tile,dest_tile:Tile):
        #Get the piece we are moving
        piece=start_tile.piece
        if piece == None:
            print("No piece at that starting square!")
            return False
        if(piece.color != self.user_color):
            print("You can only move your own pieces!!!")
            return False
        
        if isinstance(piece,Pawn):
            left=self.get_tile(start_tile.row,start_tile.col-1)
            right=self.get_tile(start_tile.row,start_tile.col+1)
            if not piece.validate_move(start_tile,dest_tile,left,right):
                print("Can't make this move, this piece can't move there.")
                return False
        elif not piece.validate_move(start_tile,dest_tile):
            print("Can't make this move, this piece can't move there.")
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
        if(dest_tile is None):
            return False
        #Get the piece we are moving
        piece=start_tile.piece
        if piece == None:
            return False
        # if(piece.color != self.user_color):
        #     return False
        if isinstance(piece,Pawn):
            left=self.get_tile(start_tile.row,start_tile.col-1)
            right=self.get_tile(start_tile.row,start_tile.col+1)
            if not piece.validate_move(start_tile,dest_tile,left,right):
                return False
        elif not piece.validate_move(start_tile,dest_tile):
            return False
        
        if self.path_obstructed(piece.get_piece_path(start_tile,dest_tile)):
            return False
        if dest_tile.piece!=None:
            if dest_tile.piece.color==piece.color:
                return False
        return True
    
    #Returns none when it is invalid row and col
    def get_tile(self,row,col):
        if(not(row<8 and row>=0 and col<8 and col>=0)):
            return None
        return self.board[row][col]
        
    #Currently just brute force checks, candidate to optimize later
    def is_any_move_possible(self,color):
        for row in range(8):
            for col in range(8):
                start_tile = self.get_tile(row,col)
                #Check valid tile
                if start_tile is None:
                    continue
                #Check there is a piece to move
                if start_tile.piece is None:
                    continue
                #Check the color is of the same as the desired color to test
                if start_tile.piece.color !=color:
                    continue
                #Test all destination squares
                for dest_row in range(8):
                    for dest_col in range(8):
                        dest_tile = self.get_tile(dest_row,dest_col)
                        # if dest_tile.piece is None:
                        #     continue
                        # if (start_tile.col==5 and start_tile.row==5 and dest_tile.piece.symbol=="Q" ):
                        #     x=5
                        if self.full_move_validation_for_checks(start_tile, dest_tile):
                            # Try making the move and see if it puts the king out of check
                            self.make_move(start_tile, dest_tile)
                            #Are we in check now?
                            in_check=self.is_in_check(color)
                            #Restore board state
                            self.undo_move()
                            #Return true if we aren't in check
                            if in_check==False:
                                return True
        return False
    
    def is_checkmate_or_stalemate(self,color):
        #Check if we are in check right now
        is_in_check=self.is_in_check(color)

        #Check if we can move
        can_move=self.is_any_move_possible(color)

        #If we can move its not checkmate or stalemate
        if(can_move==True):
            return None
        #Reaching here means we cant move, so check if we are in check, if so it is mate
        if is_in_check ==True:
            return "CM"
        #If its not mate and we can't move then it must be a draw
        if is_in_check==False:
            return "SM"

    #Castling requires more complex than just moving need to check if king would be in check in any move of castle
    def move_is_castle(self,move_str):
        if move_str=="O-O":
            return "KC"
        elif move_str=="O-O-O":
            return "QC"
        return None
    
    def validate_castle(self,king:Tile,rook:Tile,type,color):
        king_start={"row":king.row,"col":king.col}
        if king.piece is None or rook.piece is None:
            return False
        #Check our pieces are actually king and rooks
        if not (isinstance(rook.piece,Rook) and isinstance(king.piece,King)):
            return False
        if rook.piece.has_moved or king.piece.has_moved:
            return False
        iterate_over=None
        if type=="QC":
            iterate_over=range(1,king.col).__reversed__()
        elif type=="KC":
            iterate_over=range(king.col+1,7)
            pass
        failed_castle=False
        move_from=king
        move_to=None
        #Check if king is safe in the intermediate squares and they arent occupied
        for i in iterate_over:
            move_to=self.get_tile(king.row,i)
            if(move_to.occupied()):
                failed_castle=True
                break
            self.make_move(move_from,move_to)
            move_from=move_to
            if(self.is_in_check(color)):
                failed_castle=True
                break
        
        #Reset king to its true spot instead of its intermediary check spots
        self.undo_move()

        return not failed_castle
    
    """If it is en passant, grab that pawn. NOTE: This does not perform any move validation itself."""
    def handle_en_passant(self,start_tile:Tile,dest_tile:Tile):
        left=self.get_tile(start_tile.row,start_tile.col-1)
        right=self.get_tile(start_tile.row,start_tile.col+1)
        if(Pawn.move_is_en_passant(start_tile,dest_tile,left,right)):
            # Calculate the direction of movement based on pawn color
            direction = start_tile.piece.get_direction()
            captured_tile=self.get_tile(dest_tile.row - direction,dest_tile.col)
            self.move_buffer.append(deepcopy(captured_tile))
            captured_tile.piece=None#Capture the piece
    #Never used
    # def undo_en_passant(self,start_tile,dest_tile):
    #     captured_color=ChessBoard.BLACK if dest_tile.color==ChessBoard.WHITE else ChessBoard.WHITE
    #     # Calculate the direction of movement based on pawn color
    #     direction = -1 if start_tile.color == ChessBoard.WHITE else 1

    #     captured_tile=self.get_tile(dest_tile.row - direction,dest_tile.col)
    #     restored_pawn=Pawn(captured_color)
    #     restored_pawn.en_passantable=True
    #     captured_tile.piece=restored_pawn
    #     self.make_move(start_tile,dest_tile)

    def handle_castle(self,castle_type,receiving:bool):
        color=self.user_color
        if receiving:
            if color==ChessBoard.WHITE:
                color=ChessBoard.BLACK
            else:
                color=ChessBoard.WHITE
        row=0
        if color==ChessBoard.WHITE:
            row=7
        king_tile=self.get_tile(row,ord("e")-ord("a"))
        king_dest_col=None
        if(castle_type=="QC"):
            rook_tile=self.get_tile(row,0)
            king_dest_col=1
            rook_dest_col=king_tile.col-1
        elif castle_type=="KC":
            rook_tile=self.get_tile(row,7)
            king_dest_col=6
            rook_dest_col=king_tile.col+1
        king_dest_tile=self.get_tile(row,king_dest_col)
        rook_dest_tile=self.get_tile(row,rook_dest_col)
        if(receiving==True):
            self.move_piece(king_tile,king_dest_tile)
            self.move_piece(rook_tile,rook_dest_tile)
            return True
        #Check if castle move is valid
        if self.validate_castle(king_tile,rook_tile,castle_type,color):
            self.move_piece(king_tile,king_dest_tile)
            self.move_piece(rook_tile,rook_dest_tile)
            return True
        
        print("Can't castle right now!")
        return False
    
    def move_piece(self,from_tile:Tile,to_tile:Tile):
        to_tile.piece=from_tile.piece
        from_tile.piece=None
    
    def make_move(self,start_tile:Tile, dest_tile:Tile):
        #Copy initial tile states before move
        self.move_buffer.append(deepcopy(start_tile))
        self.move_buffer.append(deepcopy(dest_tile))
        
        #Check for special pawn moves
        if (isinstance(start_tile.piece,Pawn)):
            #If it is en passant, grab that pawn
            self.handle_en_passant(start_tile,dest_tile)
            
            #Handle setting en passant flag
            if(abs(dest_tile.row-start_tile.row)==2):
                start_tile.piece.en_passantable=True

            #Promotion
        #Handle king moves
        #Actually update the board
        self.move_piece(start_tile,dest_tile)

        #Update king if piece is king
        self.update_king_position(self.user_color,dest_tile.row,dest_tile.col)

    def undo_move(self):
        #Iterate through moves from last to first, this is necessary to properly undo a castle move
        for restore_tile in self.move_buffer.__reversed__():
            if isinstance(restore_tile,Tile):
                #Retrieve current tile from board
                board_tile=self.get_tile(restore_tile.row,restore_tile.col)
                #Restore it to the buffered piece
                board_tile.piece=restore_tile.piece
                #Update king if piece is king
                self.update_king_position(self.user_color,board_tile.row,board_tile.col)
            else:
                raise TypeError("Move buffer received an invalid type")
        #Empty buffer
        self.move_buffer.clear()
    
    def clean_up_move(self):
        #Clear en passants
        if(self.user_color==ChessBoard.WHITE):
            for pawn in self.black_pawns:
                pawn.en_passantable=False
        elif(self.user_color==ChessBoard.BLACK):
            for pawn in self.white_pawns:
                pawn.en_passantable=False
        self.move_buffer.clear()
    
    """Accepts a users input and translates it into a move on the board if it is a legal move"""
    def move(self, move_str,receiving_move=False):#Eg of a move is Ne4
        castle_res=self.move_is_castle(move_str)

        if castle_res is not None:
            success= self.handle_castle(castle_res,receiving_move)
            self.clean_up_move()
            return success
        
        #Load starting tiles
        start_tile,dest_tile = self.move_decoder.decode_move(move_str)

        #Null checks
        if(start_tile is None or dest_tile is None):
            return False
        
        #Assume move is validated and make the move if receiving
        if receiving_move:
            self.make_move(start_tile,dest_tile)
            self.move_buffer.clear()
            return True
        
        #Validate the move
        if(self.full_move_validation(start_tile,dest_tile)==False):
            return False
        
        #Move piece
        self.make_move(start_tile,dest_tile)
        
        #Check if we are in check after move
        if self.is_in_check(self.user_color):
            #Undo move if it puts yourself in check
            self.undo_move()
            print("Can't move yourself into check!")
            return False
        
        # Check if the move puts the opponent's king in check
        opponent_color = 1 - self.user_color
        if self.is_in_check(opponent_color):
            print("Check!")
        if isinstance(dest_tile.piece,King) or isinstance(dest_tile.piece,Rook):
            dest_tile.piece.has_moved=True

        self.clean_up_move()
        return True
    
    def update_king_position(self, color, row, col):
        if self.board[row][col].piece is None:
            return
        # Update the position of the king for the specified color
        if self.board[row][col].piece.symbol == 'K':
            self.king_positions[color] = (row, col)

    #Currently can't move king out of check properly
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

#Needs the promotion implemented
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'P'
        self.en_passantable=False
    def get_direction(self):
        return -1 if self.color == ChessBoard.WHITE else 1
        
    def move_is_en_passant(current:Tile,new:Tile,left:Tile,right:Tile):
        color=current.piece.color
        if not isinstance(current.piece,Pawn):
            return False
        # Calculate the direction of movement based on pawn color
        direction = -1 if current.piece.color == ChessBoard.WHITE else 1
        # Pawn capture (diagonal)
        if (new.row == current.row + direction):
            if (new.col == current.col - 1):
                if isinstance(left.piece,Pawn):
                    if left.piece.en_passantable and left.piece.color != color:
                        return True
            elif (new.col == current.col + 1):
                if isinstance(right.piece,Pawn):
                    if right.piece.en_passantable and right.piece.color != color:
                        return True
            #This means it is normal capture
            return False
    def validate_move(self,current:Tile,new:Tile,left:Tile,right:Tile):
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
        if (new.row == current.row + direction):
            if (new.col == current.col - 1):
                if isinstance(left.piece,Pawn):
                    if left.piece.en_passantable and left.piece.color != self.color:
                        return not new.occupied()
                else:
                    return new.occupied()
            elif (new.col == current.col + 1):
                if isinstance(right.piece,Pawn):
                    if right.piece.en_passantable and right.piece.color != self.color:
                        return not new.occupied()
                else:
                    return new.occupied()

        
        # Invalid move
        return False

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'R'
        self.has_moved=False
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
        self.has_moved=False
    def validate_move(self, start:Tile,dest:Tile):
        row_diff = abs(dest.row - start.row)
        col_diff = abs(dest.col - start.col)
        if row_diff<=1 and col_diff<=1:
            return True
        return False
    