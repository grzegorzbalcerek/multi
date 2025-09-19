import unittest

from color import Color, color_row, other_color


class TestColor(unittest.TestCase):
    def test_other_color(self):
        self.assertEqual(other_color(Color.White), Color.Black)
        self.assertEqual(other_color(Color.Black), Color.White)

    def test_color_row(self):
        self.assertEqual(color_row(Color.White, 1), 1)
        self.assertEqual(color_row(Color.Black, 1), 8)
