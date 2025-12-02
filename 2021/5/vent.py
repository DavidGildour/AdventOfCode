import re
from typing import Generator

RANGE_REGEX = r"(\d+),(\d+) -> (\d+),(\d+)"


class Vent:
    def __init__(self, raw_coordinates: str):
        a, b, c, d = map(int, re.match(RANGE_REGEX, raw_coordinates).groups())
        self.range_start = a, b
        self.range_end = c, d

    @property
    def is_vertical(self) -> bool:
        return self.range_start[0] == self.range_end[0]

    @property
    def is_horizontal(self) -> bool:
        return self.range_start[1] == self.range_end[1]

    def get_full_range(self) -> Generator[tuple[int, int], None, None]:
        if self.is_horizontal:
            return self._get_horizontal_range()
        if self.is_vertical:
            return self._get_vertical_range()
        else:
            return self._get_diagonal_range()

    def _get_horizontal_range(self) -> Generator[tuple[int, int], None, None]:
        y = self.range_start[1]
        x1, x2 = self.range_start[0], self.range_end[0]
        start, end = sorted([x1, x2])

        for x in range(start, end + 1):
            yield x, y

    def _get_vertical_range(self) -> Generator[tuple[int, int], None, None]:
        x = self.range_start[0]
        y1, y2 = self.range_start[1], self.range_end[1]
        start, end = sorted([y1, y2])

        for y in range(start, end + 1):
            yield x, y

    def _get_diagonal_range(self) -> Generator[tuple[int, int], None, None]:
        x1, y1 = self.range_start
        x2, y2 = self.range_end
        direction_horizontal = (-1) ** (x1 > x2)
        direction_vertical = (-1) ** (y1 > y2)

        full_range = zip(
            range(x1, x2 + direction_horizontal, direction_horizontal),
            range(y1, y2 + direction_vertical, direction_vertical),
        )
        yield from full_range
