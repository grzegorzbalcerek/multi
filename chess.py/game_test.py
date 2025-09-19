import unittest

from board import starting_board, update_board
from color import Color
from field import Field
from figure import Figure, FigureType
from game import (GameStart, OngoingGame, game_message, game_moves,
                  is_en_passant_capture, next_games_after_figure_moves,
                  next_games_after_pawn_en_passant_moves,
                  next_games_after_pawn_regular_and_promotion_moves,
                  show_game_hist, update_game)
from move import RegularMove

game1 = GameStart()
board2 = update_board(starting_board(), RegularMove(Field(2, 2), Field(2, 3)))
game2 = OngoingGame(Color.Black, board2, game1, RegularMove(Field(2, 2), Field(2, 3)))
board3 = update_board(board2, RegularMove(Field(2, 7), Field(2, 5)))
game3 = OngoingGame(Color.White, board3, game2, RegularMove(Field(2, 7), Field(2, 5)))
board4 = update_board(board3, RegularMove(Field(4, 2), Field(4, 2)))
game4 = OngoingGame(Color.Black, board4, game3, RegularMove(Field(4, 2), Field(4, 4)))


class GameTest(unittest.TestCase):
    def test_game_message(self):
        self.assertEqual(game_message(game1), "White to begin")
        self.assertEqual(game_message(game2), "Last move: White b2 to b3")

    def test_game_moves(self):
        self.assertEqual(game_moves(game1), [])
        self.assertEqual(game_moves(game2), ["White b2 to b3"])
        self.assertEqual(game_moves(game3), ["White b2 to b3", "Black b7 to b5"])

    def test_show_game_hist(self):
        self.assertEqual(
            show_game_hist(game4),
            "  1. White b2 to b3, Black b7 to b5\n  2. White d2 to d4",
        )

    def test_update_game(self):
        g2 = update_game(game1, RegularMove(Field(2, 2), Field(2, 4)))
        self.assertEqual(g2.color, Color.Black)
        self.assertIsNone(g2.board.get((2, 2)))
        self.assertEqual(g2.board[(2, 4)], Figure(FigureType.Pawn, Color.White))

    def test_is_en_passant_capture(self):
        self.assertFalse(is_en_passant_capture(game1, Field(2, 2), Field(2, 4)))
        g2 = update_game(game1, RegularMove(Field(2, 2), Field(2, 4)))
        g3 = update_game(g2, RegularMove(Field(7, 7), Field(7, 5)))
        g4 = update_game(g3, RegularMove(Field(2, 4), Field(2, 5)))
        g5 = update_game(g4, RegularMove(Field(7, 5), Field(7, 4)))
        g6 = update_game(g5, RegularMove(Field(6, 2), Field(6, 4)))
        g7 = update_game(g6, RegularMove(Field(7, 4), Field(6, 3)))
        self.assertTrue(is_en_passant_capture(g6, Field(7, 4), Field(6, 3)))
        self.assertFalse(is_en_passant_capture(g7, Field(2, 5), Field(3, 6)))

    def test_next_games_after_pawn_en_passant_moves(self):
        self.assertEqual(
            next_games_after_pawn_en_passant_moves(
                game1, Field(2, 2), Figure(FigureType.Pawn, Color.White)
            ),
            [],
        )
        g2 = update_game(game1, RegularMove(Field(2, 2), Field(2, 4)))
        g3 = update_game(g2, RegularMove(Field(7, 7), Field(7, 5)))
        g4 = update_game(g3, RegularMove(Field(2, 4), Field(2, 5)))
        g5 = update_game(g4, RegularMove(Field(7, 5), Field(7, 4)))
        g6 = update_game(g5, RegularMove(Field(6, 2), Field(6, 4)))
        g7 = update_game(g6, RegularMove(Field(7, 4), Field(6, 3)))
        self.assertEqual(
            len(
                next_games_after_pawn_en_passant_moves(
                    g6, Field(7, 4), Figure(FigureType.Pawn, Color.White)
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                next_games_after_pawn_en_passant_moves(
                    g6, Field(7, 4), Figure(FigureType.Pawn, Color.Black)
                )
            ),
            1,
        )
        self.assertEqual(
            len(
                next_games_after_pawn_en_passant_moves(
                    g7, Field(2, 5), Figure(FigureType.Pawn, Color.White)
                )
            ),
            0,
        )

    def test_next_games_after_pawn_regular_and_promotion_moves(self):
        self.assertEqual(
            len(
                next_games_after_pawn_regular_and_promotion_moves(
                    game1, Field(2, 2), Figure(FigureType.Pawn, Color.White)
                )
            ),
            2,
        )

    def test_next_games_after_figure_moves(self):
        self.assertEqual(
            len(
                next_games_after_figure_moves(
                    game1, Field(2, 1), Figure(FigureType.Knight, Color.White)
                )
            ),
            2,
        )
        self.assertEqual(
            len(
                next_games_after_figure_moves(
                    game1, Field(2, 1), Figure(FigureType.Rook, Color.White)
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                next_games_after_figure_moves(
                    game1, Field(2, 2), Figure(FigureType.Queen, Color.White)
                )
            ),
            11,
        )
        self.assertEqual(
            len(
                next_games_after_figure_moves(
                    game1, Field(2, 2), Figure(FigureType.King, Color.White)
                )
            ),
            3,
        )

    def test_next_games_after_moves(self):
        self.assertEqual(
            len(
                next_games_after_figure_moves(
                    game1, Field(2, 1), Figure(FigureType.Knight, Color.White)
                )
            ),
            2,
        )
        
