from chessboard import ChessBoard,Piece,Pawn,Knight,King,Queen,Rook,Bishop
from test_categories import TESTS,TEST_VALID_MOVE,TEST_CHECK,TEST_GAME_OVER
import unittest

#Make a utility for making board states to test, pysimplegui maybe
#Test castling out of check, test various castling things
#En passant, identify edge cases if possible.
class TestCase:
    def __init__(self,board,expected_result,board_move=None):
        self.board=board
        self.expected_result=expected_result
        self.move=None if board_move=='' else board_move

class TestChessBoard(unittest.TestCase):
    # Show boards when loading them to verify loaded properly if desired
    PREVIEW_BOARDS=True
    def setUp(self):
        self.board = ChessBoard(ChessBoard.WHITE)
        self.boards=[]
        self.tests={}
        for category in TESTS:
            self.tests[category]=[]
        self.load_boards_from_file()
    def tearDown(self):
        pass
    def load_boards_from_file(self):
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
                
            # for row_str in rows:
            #     row_data = row_str[1:-1].split(", ")
            #     row_data = [int(row_data[0]), int(row_data[1]), row_data[2], int(row_data[3])]
            #     chessboard_array.append(row_data)
            
            return chessboard_array
        with open("boards.json","r") as f:
            boards=f.readlines()

        for i in boards:
            #Load category
            category_end_index=i.find(",")
            category=i[:category_end_index]
            #Load color
            end_color_index=i.find(",",category_end_index+1)
            color_str=i[category_end_index+1:end_color_index]
            color=ChessBoard.WHITE if color_str=="white" else ChessBoard.BLACK
            #Load expected value
            end_expected_index=i.find(",",end_color_index+1)
            expected=i[end_color_index+1:end_expected_index]
            #Check if looking for return of none
            if expected.lower()=="none":
                expected=None
            elif expected.lower()=="true":
                expected=True
            elif expected.lower()=="false":
                expected=False
            #Load move
            move_end_index=i.find(",",end_expected_index+1)
            move=i[end_expected_index+1:move_end_index]

            #Create board
            board_array=parse_chessboard_string(i[move_end_index+1:])
            board=ChessBoard(color)
            board.load_board_from_array(board_array)
            if TestChessBoard.PREVIEW_BOARDS:
                board.display_board()
            
            #Construct test case
            test=TestCase(board,expected,move)
            self.tests[category].append(test)

    def test_initial_board_setup(self):
        # Test if the initial board setup is correct
        self.assertEqual(len(self.board.white_pawns), 8)
        self.assertEqual(len(self.board.black_pawns), 8)
        # Add more assertions for other initial piece positions

    def test_piece_move(self):
        for test_case in self.tests[TEST_VALID_MOVE]:
            # test_case.board.display_board()
            self.assertEqual(test_case.board.move(test_case.move),test_case.expected_result)

    #Checks if the player to play is in check
    def test_check(self):
        #When true it will attempt a move then see if in check.
        TRY_MOVE_FLAG=False
        for test_case in self.tests[TEST_CHECK]:
            if TRY_MOVE_FLAG and test_case.move !=None:
                test_case.board.move(test_case.move)
            self.assertEqual(test_case.board.is_in_check(test_case.board.user_color),test_case.expected_result)
        
 
    def test_game_over(self):
        #When true it will attempt a move before test
        TRY_MOVE_FLAG=False
        for test_case in self.tests[TEST_GAME_OVER]:
            if TRY_MOVE_FLAG and test_case.move !=None:
                test_case.board.move(test_case.move)
            self.assertEqual(test_case.board.is_checkmate_or_stalemate(test_case.board.user_color),test_case.expected_result)
    

if __name__ == '__main__':
    unittest.main()
