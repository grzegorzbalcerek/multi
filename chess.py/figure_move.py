from itertools import takewhile

from color import Color
from field import Field
from figure import Figure, FigureType


def rook_movess() -> list[list[(int, int)]]:
    """
    Sequences of relative figure positions for rook moves.
    """
    return [
        [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)],
        [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)],
        [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)],
        [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],
    ]


def bishop_movess() -> list[list[(int, int)]]:
    """
    Sequences of relative figure positions for bishop moves.
    """
    return [
        [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)],
        [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)],
        [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)],
        [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)],
    ]


def queen_movess() -> list[list[(int, int)]]:
    """
    Sequences of relative figure positions for queen moves.
    """
    return rook_movess() + bishop_movess()


def knight_movess() -> list[list[(int, int)]]:
    """
    Sequences of relative figure positions for knight moves.
    """
    return [
        [(1, 2)],
        [(2, 1)],
        [(-1, 2)],
        [(2, -1)],
        [(-1, -2)],
        [(-2, -1)],
        [(1, -2)],
        [(-2, 1)],
    ]


def king_movess() -> list[list[(int, int)]]:
    """
    Sequences of relative figure positions for king moves.
    """
    return list(map(lambda seq: seq[0:1], queen_movess()))


def figure_movess(figure, field, capture):
    """
    Choose the sequences of relative figure positions
    based on the figure position, type, color,
    and whether the move is a capture move or not.
    """
    match figure:
        case Figure(FigureType.Rook, _):
            return rook_movess()
        case Figure(FigureType.Bishop, _):
            return bishop_movess()
        case Figure(FigureType.Queen, _):
            return queen_movess()
        case Figure(FigureType.King, _):
            return king_movess()
        case Figure(FigureType.Knight, _):
            return knight_movess()
        case Figure(FigureType.Pawn, Color.White) if capture:
            return [[(1, 1)], [(-1, 1)]]
        case Figure(FigureType.Pawn, Color.White) if field.row == 2:
            return [[(0, 1), (0, 2)]]
        case Figure(FigureType.Pawn, Color.White):
            return [[(0, 1)]]
        case Figure(FigureType.Pawn, Color.Black) if capture:
            return [[(1, -1)], [(-1, -1)]]
        case Figure(FigureType.Pawn, Color.Black) if field.row == 7:
            return [[(0, -1), (0, -2)]]
        case Figure(FigureType.Pawn, Color.Black):
            return [[(0, -1)]]
        case x:
            raise TypeError(f"Unexpected argument {figure=}")


def figure_targetss(figure: Figure, field: Field, capture: bool) -> [[Field]]:
    return list(
        map(
            lambda moves: list(
                filter(lambda target: target.is_valid(), field.relative_fields(moves))
            ),
            figure_movess(figure, field, capture),
        )
    )


def show_fieldss(fieldss: [[Field]]) -> [[str]]:
    return list(
        map(lambda targets: list(map(lambda target: str(target), targets)), fieldss)
    )
