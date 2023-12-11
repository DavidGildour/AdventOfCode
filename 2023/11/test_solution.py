import unittest

from solution import expand_universe, find_galaxies, part_one


class TestPartOne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("input_test.txt") as f:
            cls._input = [x.strip() for x in f.readlines()]

    def test_universe_expansion(self):
        actual = expand_universe(self._input)
        expected = [
            "....#........",
            ".........#...",
            "#............",
            ".............",
            ".............",
            "........#....",
            ".#...........",
            "............#",
            ".............",
            ".............",
            ".........#...",
            "#....#.......",
        ]
        self.assertEqual(actual, expected)

    def test_find_galaxies(self):
        actual = find_galaxies(self._input)
        expected = {
            (3, 0),
            (7, 1),
            (0, 2),
            (6, 4),
            (1, 5),
            (9, 6),
            (7, 8),
            (0, 9),
            (4, 9),
        }

        self.assertEqual(actual, expected)

    def test_result(self):
        actual = part_one(self._input)
        self.assertEqual(actual, 374)


if __name__ == "__main__":
    unittest.main()
