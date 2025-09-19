from dataclasses import dataclass

from color import Color, color_row, other_color


@dataclass
class Field:
    """
    Represents a field on the chess board.
    """

    col: int
    row: int

    def __str__(self):
        """
        Shows field coordinates as a pair of characters:
        a letter representing the column and a number representing the row.

        >>> print(Field(1,1))
        a1

        >>> print(Field(1,8))
        a8

        >>> print(Field(8,1))
        h1

        >>> print(Field(8,8))
        h8

        >>> print(Field(4,5))
        d5
        """
        return chr(self.col + ord("a") - 1) + str(self.row)

    def as_pair(self):
        """
        Return a tuple containing the column and the row.
        """
        return (self.col, self.row)

    def relative(self, move: (int, int)):
        """
        Returns a new field with coordinates moved
        by the given number of rows and columns relative to the original field.

        >>> Field(6,7).relative((-2,-4))
        Field(col=4, row=3)

        >>> Field(3,5).relative((9,10))
        Field(col=12, row=15)
        """
        return Field(self.col + move[0], self.row + move[1])

    def relative_fields(self, moves: [(int, int)]):
        """
        Returns fields with coordinates moved by the given moves.
        """
        return list(map(lambda move: self.relative(move), moves))

    def is_last_row(self, color: Color):
        """
        Returns a boolean value indicating
        whether the given field belongs to the last row from
        the point of view of a player.

        >>> Field(8,8).is_last_row(Color.White)
        True

        >>> Field(7,8).is_last_row(Color.White)
        True

        >>> Field(7,8).is_last_row(Color.Black)
        False

        >>> Field(7,1).is_last_row(Color.Black)
        True

        >>> Field(2,2).is_last_row(Color.White)
        False
        """
        return self.row == color_row(other_color(color), 1)

    def is_valid(self):
        """
        Returns a boolean value indicating
        whether the field has valid coordinates, that is
        whether it belongs to the board.
        Valid fields have coordinates in the range between 1 and 8.

        >>> Field(2,2).is_valid()
        True

        >>> Field(0,2).is_valid()
        False

        >>> Field(2,0).is_valid()
        False

        >>> Field(2,9).is_valid()
        False

        >>> Field(9,2).is_valid()
        False
        """
        return self.col >= 1 and self.col <= 8 and self.row >= 1 and self.row <= 8
