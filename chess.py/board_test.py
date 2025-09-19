import unittest

from board import (find_color_figure_fields, free_destinations,
                   has_figure_of_color, is_field_empty, show_board,
                   starting_board, update_board)
from color import Color
from field import Field
from figure import Figure, FigureType
from figure_move import figure_movess
from move import CastlingMove, EnPassantMove, PromotionMove, RegularMove


class BoardFigure(unittest.TestCase):
    def test_show_board(self):
        self.assertEqual(
            str(show_board(starting_board())),
            """ abcdefgh
8RNBQKBNR8
7PPPPPPPP7
6........6
5........5
4........4
3........3
2pppppppp2
1rnbqkbnr1
 abcdefgh""",
        )

    def test_update_board(self):
        board = update_board(starting_board(), RegularMove(Field(2, 2), Field(2, 3)))
        self.assertEqual(board.get((2, 2)), None)
        self.assertEqual(board.get((2, 3)), Figure(FigureType.Pawn, Color.White))

        board = update_board(starting_board(), RegularMove(Field(3, 3), Field(2, 3)))
        self.assertEqual(board, starting_board())

        board = update_board(
            starting_board(),
            PromotionMove(
                Field(2, 2), Field(2, 8), Figure(FigureType.Queen, Color.White)
            ),
        )
        self.assertEqual(board.get((2, 2)), None)
        self.assertEqual(board.get((2, 8)), Figure(FigureType.Queen, Color.White))
        figure_types = [figure.figure_type for figure in board.values()]
        self.assertEqual(figure_types.count(FigureType.Pawn), 15)
        self.assertEqual(figure_types.count(FigureType.Queen), 3)

        board = update_board(
            starting_board(),
            EnPassantMove(Field(2, 2), Field(3, 3), captured=Field(3, 7)),
        )
        self.assertEqual(board.get((2, 2)), None)
        self.assertEqual(board.get((3, 3)), Figure(FigureType.Pawn, Color.White))
        self.assertEqual(board.get((3, 7)), None)
        figure_types = [figure.figure_type for figure in board.values()]
        self.assertEqual(figure_types.count(FigureType.Pawn), 15)

        board = update_board(
            starting_board(),
            CastlingMove(Field(5, 1), Field(3, 1), Field(1, 1), Field(4, 1)),
        )
        self.assertEqual(board.get((1, 1)), None)
        self.assertEqual(board.get((5, 1)), None)
        self.assertEqual(board.get((3, 1)), Figure(FigureType.King, Color.White))
        self.assertEqual(board.get((4, 1)), Figure(FigureType.Rook, Color.White))
        figure_types = [figure.figure_type for figure in board.values()]
        self.assertEqual(figure_types.count(FigureType.Pawn), 16)
        self.assertEqual(figure_types.count(FigureType.Rook), 4)
        self.assertEqual(figure_types.count(FigureType.Bishop), 3)

    def test_is_field_empty(self):
        self.assertEqual(is_field_empty(starting_board(), Field(1, 1)), False)
        self.assertEqual(is_field_empty(starting_board(), Field(3, 3)), True)

    def test_has_figure_of_color(self):
        self.assertEqual(
            has_figure_of_color(starting_board(), Field(4, 4), Color.White), False
        )
        self.assertEqual(
            has_figure_of_color(starting_board(), Field(2, 2), Color.White), True
        )
        self.assertEqual(
            has_figure_of_color(starting_board(), Field(7, 7), Color.White), False
        )
        self.assertEqual(
            has_figure_of_color(starting_board(), Field(8, 8), Color.White), False
        )
        self.assertEqual(
            has_figure_of_color(starting_board(), Field(4, 4), Color.Black), False
        )
        self.assertEqual(
            has_figure_of_color(starting_board(), Field(2, 2), Color.Black), False
        )
        self.assertEqual(
            has_figure_of_color(starting_board(), Field(7, 7), Color.Black), True
        )
        self.assertEqual(
            has_figure_of_color(starting_board(), Field(8, 8), Color.Black), True
        )

    def test_free_destinations(self):
        self.assertEqual(
            free_destinations(
                starting_board(),
                [[Field(4, 4), Field(3, 3), Field(2, 2), Field(1, 1)]],
            ),
            [Field(4, 4), Field(3, 3)],
        )

        self.assertEqual(
            free_destinations(
                starting_board(),
                [
                    [Field(4, 3), Field(4, 2)],
                    [Field(4, 4), Field(3, 3), Field(2, 2), Field(1, 1)],
                ],
            ),
            [Field(4, 3), Field(4, 4), Field(3, 3)],
        )

    def test_find_color_figure_fields(self):
        self.assertEqual(
            find_color_figure_fields(
                starting_board(),
                [[Field(4, 4), Field(3, 3), Field(2, 2), Field(1, 1)]],
                Color.Black,
            ),
            [],
        )

        self.assertEqual(
            find_color_figure_fields(
                starting_board(),
                [[Field(4, 4), Field(3, 3), Field(2, 2), Field(1, 1)]],
                Color.White,
            ),
            [Field(2, 2)],
        )

        self.assertEqual(
            find_color_figure_fields(
                starting_board(),
                [
                    [Field(4, 3), Field(4, 2)],
                    [Field(4, 4), Field(3, 3), Field(2, 2), Field(1, 1)],
                ],
                Color.White,
            ),
            [Field(4, 2), Field(2, 2)],
        )
