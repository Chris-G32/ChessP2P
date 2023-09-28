from chessboard import ChessBoard,Piece,Pawn,Knight,King,Queen,Rook,Bishop

import unittest

#Make a utility for making board states to test, pysimplegui maybe
#Test castling out of check, test various castling things
#En passant, identify edge cases if possible.


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.board = ChessBoard(ChessBoard.WHITE)
    def tearDown(self):
        pass


    def test_initial_board_setup(self):
        # Test if the initial board setup is correct
        self.assertEqual(len(self.board.white_pawns), 8)
        self.assertEqual(len(self.board.black_pawns), 8)
        # Add more assertions for other initial piece positions

    def test_valid_piece_move(self):
        # Test a valid piece move
        self.assertTrue(self.board.move("e2e4"))
        # Add more assertions for other piece movements

    def test_invalid_piece_move(self):
        # Test an invalid piece move
        self.assertFalse(self.board.move("e2e5"))  # Invalid pawn move
        # Add more assertions for other invalid moves

    def test_check_condition(self):
        # Test check condition
        # You should set up a specific board state to test this condition
        # Make a move that puts the opponent's king in check and then check if it's in check
        self.board.move("e2e4")
        self.board.move("f7f5",True)
        self.board.move("d1h5")  # Queen threatens the black king
        self.board.display_board()
        self.assertTrue(self.board.is_in_check(ChessBoard.BLACK))
 
    def test_checkmate_condition(self):
        print("\nTesting Checkmate\n")
        # Test checkmate condition
        # You should set up a specific board state to test this condition
        # Make a series of moves that lead to checkmate
        self.assertTrue(self.board.move("f2f3"))
        self.assertTrue(self.board.move("e7e5",True))
        self.assertTrue( self.board.move("g2g4"))
        self.assertTrue (self.board.move("d8h4",True))  # Queen threatens the white king
        # self.board.display_board()
        self.assertEqual(self.board.is_checkmate_or_stalemate(ChessBoard.WHITE), "CM")

    def runTest(self):
        print("RUNTEST")
        pass

if __name__ == '__main__':
    unittest.main()
