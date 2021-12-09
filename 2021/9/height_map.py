from dataclasses import dataclass
from functools import reduce
from typing import Optional, Iterator


@dataclass
class Point:
    x: int
    y: int
    height: int

    @property
    def coor(self) -> tuple[int, int]:
        return self.x, self.y


class HeightMap:
    def __init__(self, raw_data: list[str]):
        self.area = list(tuple(map(int, col)) for col in zip(*raw_data))
        self.width = len(self.area)
        self.height = len(self.area[0])

    @property
    def iter_area(self) -> Iterator[Point]:
        return iter(Point(x, y, height) for x, row in enumerate(self.area) for y, height in enumerate(row))

    def get_cell_height(self, x: int, y: int) -> Optional[int]:
        if not self.valid_coordinates(x, y):
            return None
        return self.area[x][y]

    def get_neighbours(self, x: int, y: int) -> tuple[Point, ...]:
        return tuple(filter(lambda point: point.height is not None, (
            Point(x-1, y, self.get_cell_height(x - 1, y)),
            Point(x, y-1, self.get_cell_height(x, y - 1)),
            Point(x+1, y, self.get_cell_height(x + 1, y)),
            Point(x, y+1, self.get_cell_height(x, y + 1)),
        )))

    def get_basin(self, x: int, y: int, basin_buffer: set[tuple[int, int]] = None) -> set[tuple[int, int]]:
        if basin_buffer is None:
            basin_buffer = set()
        filtered_neighbours = tuple(
            filter(
                lambda p: p.height < 9 and p.coor not in basin_buffer,
                self.get_neighbours(x, y)
            )
        )
        basin_buffer |= {(x, y), *(p.coor for p in filtered_neighbours)}
        return reduce(
            lambda s1, s2: s1 | s2,
            [{(x, y)}, *[self.get_basin(p.x, p.y, basin_buffer) for p in filtered_neighbours]]
        )

    def valid_coordinates(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_low_points(self) -> list[Point]:
        return [
            point for point in self.iter_area
            if not tuple(filter(lambda p: p.height <= point.height, self.get_neighbours(point.x, point.y)))
        ]

    def __str__(self):
        return "\n".join("".join(row) for row in zip(*self.area))
