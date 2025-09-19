import unittest

from color import Color
from field import Field


class TestField(unittest.TestCase):
    def test_relative(self):
        self.assertEqual(Field(6, 7).relative((-2, -4)), Field(col=4, row=3))
        self.assertEqual(Field(3, 5).relative((9, 10)), Field(col=12, row=15))

    def test_relative_fields(self):
        self.assertEqual(
            Field(6, 7).relative_fields([(1, 0), (1, 1), (-2, -3), (9, 9)]),
            [
                Field(col=7, row=7),
                Field(col=7, row=8),
                Field(col=4, row=4),
                Field(col=15, row=16),
            ],
        )

    def test_is_last_row(self):
        self.assertEqual(Field(8, 8).is_last_row(Color.White), True)
        self.assertEqual(Field(7, 8).is_last_row(Color.White), True)
        self.assertEqual(Field(7, 8).is_last_row(Color.Black), False)
        self.assertEqual(Field(7, 1).is_last_row(Color.Black), True)
        self.assertEqual(Field(2, 2).is_last_row(Color.Black), False)

    def test_valid(self):
        self.assertEqual(Field(2, 2).is_valid(), True)
        self.assertEqual(Field(0, 2).is_valid(), False)
        self.assertEqual(Field(2, 0).is_valid(), False)
        self.assertEqual(Field(2, 9).is_valid(), False)
        self.assertEqual(Field(9, 2).is_valid(), False)
