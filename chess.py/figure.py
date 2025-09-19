from dataclasses import dataclass
from enum import Enum, auto

from color import Color


class FigureType(Enum):
    """
    Represents chess figure types.
    """

    King = auto()
    Queen = auto()
    Rook = auto()
    Bishop = auto()
    Knight = auto()
    Pawn = auto()


@dataclass
class Figure:
    """
    Represents a figure, which has a type and a color.
    """

    figure_type: FigureType
    figure_color: Color

    def __str__(self):
        """
        Returns a one-character string representing the figure.

        >>> print(Figure(FigureType.King, Color.White))
        k

        >>> print(Figure(FigureType.King, Color.Black))
        K
        """
        match self:
            case Figure(FigureType.King, Color.White):
                return "k"
            case Figure(FigureType.Queen, Color.White):
                return "q"
            case Figure(FigureType.Rook, Color.White):
                return "r"
            case Figure(FigureType.Bishop, Color.White):
                return "b"
            case Figure(FigureType.Knight, Color.White):
                return "n"
            case Figure(FigureType.Pawn, Color.White):
                return "p"
            case Figure(FigureType.King, Color.Black):
                return "K"
            case Figure(FigureType.Queen, Color.Black):
                return "Q"
            case Figure(FigureType.Rook, Color.Black):
                return "R"
            case Figure(FigureType.Bishop, Color.Black):
                return "B"
            case Figure(FigureType.Knight, Color.Black):
                return "N"
            case Figure(FigureType.Pawn, Color.Black):
                return "P"

    def figure_symbol(self):
        """
        Returns a unicode symbol representing the figure.
        """
        match self:
            case Figure(FigureType.King, Color.White):
                return "\u2654"
            case Figure(FigureType.Queen, Color.White):
                return "\u2655"
            case Figure(FigureType.Rook, Color.White):
                return "\u2656"
            case Figure(FigureType.Bishop, Color.White):
                return "\u2657"
            case Figure(FigureType.Knight, Color.White):
                return "\u2658"
            case Figure(FigureType.Pawn, Color.White):
                return "\u2659"
            case Figure(FigureType.King, Color.Black):
                return "\u265a"
            case Figure(FigureType.Queen, Color.Black):
                return "\u265b"
            case Figure(FigureType.Rook, Color.Black):
                return "\u265c"
            case Figure(FigureType.Bishop, Color.Black):
                return "\u265d"
            case Figure(FigureType.Knight, Color.Black):
                return "\u265e"
            case Figure(FigureType.Pawn, Color.Black):
                return "\u265f"
