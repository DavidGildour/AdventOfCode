from dataclasses import dataclass
from typing import Iterator


@dataclass
class Point:
    x: int
    y: int
    energy: int
    flashed: bool = False

    @property
    def coor(self) -> tuple[int, int]:
        return self.x, self.y

    def reset(self):
        self.flashed = False
        self.energy = 0

    def increment(self):
        self.energy += 1

    def __hash__(self):
        return hash(self.coor)


class OctopiSimulator:
    def __init__(self, light_data: list[str]):
        self.light_map = self.create_light_map(light_data)
        self.width = len(self.light_map)
        self.height = len(self.light_map[0])

    @staticmethod
    def create_light_map(light_data: list[str]) -> tuple[tuple[Point, ...], ...]:
        return tuple(
            tuple(map(lambda v: Point(x, v[0], int(v[1])), enumerate(col))) for x, col in enumerate(zip(*light_data))
        )

    @property
    def iter_area(self) -> Iterator[Point]:
        return iter(point for row in self.light_map for point in row)

    def get(self, x: int, y: int) -> Point | None:
        if not self.valid_coordinates(x, y):
            return
        return self.light_map[x][y]

    def get_neighbours(self, x: int, y: int) -> tuple[Point, ...]:
        return tuple(filter(lambda p: p and not p.flashed, (
            self.get(x - 1, y - 1),
            self.get(x,     y - 1),
            self.get(x + 1, y - 1),
            self.get(x - 1, y),
            self.get(x + 1, y),
            self.get(x - 1, y + 1),
            self.get(x,     y + 1),
            self.get(x + 1, y + 1),
        )))

    def valid_coordinates(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def process_step(self) -> int:
        flash_reset_buffer = set()
        flashes = set()
        for point in self.iter_area:
            point.increment()
            if point.energy > 9:
                point.flashed = True
                flashes.add(point)

        total_flashes = 0
        while len(flashes):
            flash_reset_buffer |= flashes
            total_flashes += len(flashes)
            additional_flashes = set()
            for point in flashes:
                neighbours = self.get_neighbours(*point.coor)
                for neighbour in neighbours:
                    neighbour.increment()
                    if neighbour.energy > 9:
                        neighbour.flashed = True
                        additional_flashes.add(neighbour)
            flashes = additional_flashes

        for point in flash_reset_buffer:
            point.reset()

        return total_flashes
