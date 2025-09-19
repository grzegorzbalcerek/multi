import unittest

from color import Color
from field import Field
from figure import Figure, FigureType
from figure_move import *


class TestFigureMove(unittest.TestCase):
    def test_king_movess(self):
        self.assertEqual(
            king_movess(),
            [
                [(1, 0)],
                [(-1, 0)],
                [(0, 1)],
                [(0, -1)],
                [(1, 1)],
                [(1, -1)],
                [(-1, 1)],
                [(-1, -1)],
            ],
        )

    def test_figure_movess(self):
        self.assertEqual(
            figure_movess(Figure(FigureType.King, Color.Black), Field(4, 4), False),
            [
                [(1, 0)],
                [(-1, 0)],
                [(0, 1)],
                [(0, -1)],
                [(1, 1)],
                [(1, -1)],
                [(-1, 1)],
                [(-1, -1)],
            ],
        )

    def _test_figure_targetss(self, figure, field, capture, expected):
        self.assertEqual(
            show_fieldss(figure_targetss(figure, field, capture)), expected
        )

    def test_figure_targetss(self):
        self._test_figure_targetss(
            Figure(FigureType.Rook, Color.White),
            Field(3, 4),
            False,
            [
                ["d4", "e4", "f4", "g4", "h4"],
                ["b4", "a4"],
                ["c5", "c6", "c7", "c8"],
                ["c3", "c2", "c1"],
            ],
        )

        self._test_figure_targetss(
            Figure(FigureType.Bishop, Color.White),
            Field(2, 2),
            False,
            [["c3", "d4", "e5", "f6", "g7", "h8"], ["c1"], ["a3"], ["a1"]],
        )

        self._test_figure_targetss(
            Figure(FigureType.Queen, Color.Black),
            Field(2, 2),
            False,
            [
                ["c2", "d2", "e2", "f2", "g2", "h2"],
                ["a2"],
                ["b3", "b4", "b5", "b6", "b7", "b8"],
                ["b1"],
                ["c3", "d4", "e5", "f6", "g7", "h8"],
                ["c1"],
                ["a3"],
                ["a1"],
            ],
        )

        self._test_figure_targetss(
            Figure(FigureType.King, Color.Black),
            Field(2, 1),
            False,
            [["c1"], ["a1"], ["b2"], [], ["c2"], [], ["a2"], []],
        )

        self._test_figure_targetss(
            Figure(FigureType.Knight, Color.Black),
            Field(2, 1),
            False,
            [["c3"], ["d2"], ["a3"], [], [], [], [], []],
        )

        self._test_figure_targetss(
            Figure(FigureType.Pawn, Color.White), Field(2, 2), False, [["b3", "b4"]]
        )

        self._test_figure_targetss(
            Figure(FigureType.Pawn, Color.White), Field(2, 3), False, [["b4"]]
        )

        self._test_figure_targetss(
            Figure(FigureType.Pawn, Color.White), Field(2, 2), True, [["c3"], ["a3"]]
        )

        self._test_figure_targetss(
            Figure(FigureType.Pawn, Color.Black), Field(2, 7), False, [["b6", "b5"]]
        )

        self._test_figure_targetss(
            Figure(FigureType.Pawn, Color.Black), Field(2, 6), False, [["b5"]]
        )

        self._test_figure_targetss(
            Figure(FigureType.Pawn, Color.Black), Field(2, 7), True, [["c6"], ["a6"]]
        )
