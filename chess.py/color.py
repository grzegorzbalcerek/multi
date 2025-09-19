from enum import Enum


class Color(Enum):
    """
    The `Color` class represents one of the two colors (`Black` or `White`)
    used in the game of Chess.
    """

    White = 1
    Black = 8


def other_color(color: Color) -> Color:
    """
    Returns the opposite color.

    >>> other_color(Color.White)
    <Color.Black: 8>
    >>> other_color(Color.Black)
    <Color.White: 1>
    """
    match color:
        case Color.White:
            return Color.Black
        case Color.Black:
            return Color.White


def color_row(color: Color, n: int) -> int:
    """
    Returns the coordinate of the nth row
    from the point of view of a player who plays the given color.

    >>> color_row(Color.White, 1)
    1
    >>> color_row(Color.Black, 1)
    8
    """
    match color:
        case Color.White:
            return n
        case Color.Black:
            return 9 - n
