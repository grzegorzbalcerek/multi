import unittest

from color import Color
from figure import Figure, FigureType


class TestFigure(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Figure(FigureType.King, Color.White)), "k")
        self.assertEqual(str(Figure(FigureType.Queen, Color.White)), "q")
        self.assertEqual(str(Figure(FigureType.Rook, Color.White)), "r")
        self.assertEqual(str(Figure(FigureType.Bishop, Color.White)), "b")
        self.assertEqual(str(Figure(FigureType.Knight, Color.White)), "n")
        self.assertEqual(str(Figure(FigureType.Pawn, Color.White)), "p")
        self.assertEqual(str(Figure(FigureType.King, Color.Black)), "K")
        self.assertEqual(str(Figure(FigureType.Queen, Color.Black)), "Q")
        self.assertEqual(str(Figure(FigureType.Rook, Color.Black)), "R")
        self.assertEqual(str(Figure(FigureType.Bishop, Color.Black)), "B")
        self.assertEqual(str(Figure(FigureType.Knight, Color.Black)), "N")
        self.assertEqual(str(Figure(FigureType.Pawn, Color.Black)), "P")

    def test_figure_symbol(self):
        self.assertEqual(Figure(FigureType.King, Color.White).figure_symbol(), "\u2654")
        self.assertEqual(
            Figure(FigureType.Queen, Color.White).figure_symbol(), "\u2655"
        )
        self.assertEqual(Figure(FigureType.Rook, Color.White).figure_symbol(), "\u2656")
        self.assertEqual(
            Figure(FigureType.Bishop, Color.White).figure_symbol(), "\u2657"
        )
        self.assertEqual(
            Figure(FigureType.Knight, Color.White).figure_symbol(), "\u2658"
        )
        self.assertEqual(Figure(FigureType.Pawn, Color.White).figure_symbol(), "\u2659")
        self.assertEqual(Figure(FigureType.King, Color.Black).figure_symbol(), "\u265a")
        self.assertEqual(
            Figure(FigureType.Queen, Color.Black).figure_symbol(), "\u265b"
        )
        self.assertEqual(Figure(FigureType.Rook, Color.Black).figure_symbol(), "\u265c")
        self.assertEqual(
            Figure(FigureType.Bishop, Color.Black).figure_symbol(), "\u265d"
        )
        self.assertEqual(
            Figure(FigureType.Knight, Color.Black).figure_symbol(), "\u265e"
        )
        self.assertEqual(Figure(FigureType.Pawn, Color.Black).figure_symbol(), "\u265f")
