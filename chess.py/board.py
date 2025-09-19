from itertools import chain, dropwhile, takewhile

from color import Color
from field import Field
from figure import Figure, FigureType
from move import CastlingMove, EnPassantMove, PromotionMove, RegularMove


def starting_board():
    return {
        (1, 1): Figure(FigureType.Rook, Color.White),
        (2, 1): Figure(FigureType.Knight, Color.White),
        (3, 1): Figure(FigureType.Bishop, Color.White),
        (4, 1): Figure(FigureType.Queen, Color.White),
        (5, 1): Figure(FigureType.King, Color.White),
        (6, 1): Figure(FigureType.Bishop, Color.White),
        (7, 1): Figure(FigureType.Knight, Color.White),
        (8, 1): Figure(FigureType.Rook, Color.White),
        (1, 2): Figure(FigureType.Pawn, Color.White),
        (2, 2): Figure(FigureType.Pawn, Color.White),
        (3, 2): Figure(FigureType.Pawn, Color.White),
        (4, 2): Figure(FigureType.Pawn, Color.White),
        (5, 2): Figure(FigureType.Pawn, Color.White),
        (6, 2): Figure(FigureType.Pawn, Color.White),
        (7, 2): Figure(FigureType.Pawn, Color.White),
        (8, 2): Figure(FigureType.Pawn, Color.White),
        (1, 7): Figure(FigureType.Pawn, Color.Black),
        (2, 7): Figure(FigureType.Pawn, Color.Black),
        (3, 7): Figure(FigureType.Pawn, Color.Black),
        (4, 7): Figure(FigureType.Pawn, Color.Black),
        (5, 7): Figure(FigureType.Pawn, Color.Black),
        (6, 7): Figure(FigureType.Pawn, Color.Black),
        (7, 7): Figure(FigureType.Pawn, Color.Black),
        (8, 7): Figure(FigureType.Pawn, Color.Black),
        (1, 8): Figure(FigureType.Rook, Color.Black),
        (2, 8): Figure(FigureType.Knight, Color.Black),
        (3, 8): Figure(FigureType.Bishop, Color.Black),
        (4, 8): Figure(FigureType.Queen, Color.Black),
        (5, 8): Figure(FigureType.King, Color.Black),
        (6, 8): Figure(FigureType.Bishop, Color.Black),
        (7, 8): Figure(FigureType.Knight, Color.Black),
        (8, 8): Figure(FigureType.Rook, Color.Black),
    }


def show_board(board):
    """
    Shows the board.

    >>> print(show_board(starting_board()))
     abcdefgh
    8RNBQKBNR8
    7PPPPPPPP7
    6........6
    5........5
    4........4
    3........3
    2pppppppp2
    1rnbqkbnr1
     abcdefgh
    """

    def row_to_str(row):
        return "".join([str(board.get((col, row), ".")) for col in range(1, 9)])

    return (
        " abcdefgh\n"
        + "".join(
            [(str(row) + row_to_str(row) + str(row) + "\n") for row in range(8, 0, -1)]
        )
        + " abcdefgh"
    )


def update_board(board, move):
    """
    Returns a new board, updated with a move.
    """
    match move:
        case RegularMove(frm, to):
            if frm.as_pair() in board:
                new_board = board.copy()
                new_board[to.as_pair()] = new_board[frm.as_pair()]
                del new_board[frm.as_pair()]
                return new_board
            else:
                return board.copy()
        case PromotionMove(frm, to, figure):
            if frm.as_pair() in board:
                new_board = board.copy()
                new_board[to.as_pair()] = move.figure
                del new_board[frm.as_pair()]
                return new_board
            else:
                return board.copy()
        case EnPassantMove(frm, to, captured):
            if frm.as_pair() in board:
                new_board = board.copy()
                new_board[to.as_pair()] = new_board[frm.as_pair()]
                del new_board[frm.as_pair()]
                del new_board[captured.as_pair()]
                return new_board
            else:
                return board.copy()
        case CastlingMove(frm, to, rook_from, rook_to):
            if frm.as_pair() in board and rook_from.as_pair() in board:
                new_board = board.copy()
                new_board[to.as_pair()] = new_board[frm.as_pair()]
                new_board[rook_to.as_pair()] = new_board[rook_from.as_pair()]
                del new_board[frm.as_pair()]
                del new_board[rook_from.as_pair()]
                return new_board
            else:
                return board.copy()


def is_field_empty(board, field):
    """
    Verifies if the given field is empty.

    >>> is_field_empty(starting_board(), Field(2,2))
    False
    """
    return not (field.as_pair() in board)


def take_fields_while(board, fieldss, condition):
    """
    Take while condition holds from a list of field lists.
    """
    return list(
        chain(
            *[
                list(takewhile(lambda field: condition(board, field), fields))
                for fields in fieldss
            ]
        )
    )


def free_destinations(board, fieldss):
    """
    Returns free fields onto which the figure may be moved
    """
    return take_fields_while(board, fieldss, is_field_empty)


def has_figure_of_color(board, field, color):
    """
    Checks whether the field holds a figure with the given color
    """
    figure = board.get(field.as_pair())
    if figure:
        return figure.figure_color == color
    else:
        return False


def find_color_figure_fields(board, fieldss, color):
    """
    Returns fields occupied by the figures of a specific color that are first in each field sequence after an optional series of empty fields
    """
    return list(
        chain(
            *[
                list(
                    filter(
                        lambda f: has_figure_of_color(board, f, color),
                        list(
                            dropwhile(
                                lambda field: is_field_empty(board, field), fields
                            )
                        )[:1],
                    )
                )
                for fields in fieldss
            ]
        )
    )
