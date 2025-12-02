"""https://adventofcode.com/2023/day/16"""

import argparse
from dataclasses import dataclass
from enum import Enum, auto


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


@dataclass
class RayEvent:
    position: tuple[int, int]
    did_split: bool
    new_ray: "Ray" = None


@dataclass
class Ray:
    x: int
    y: int
    direction: Direction

    @property
    def current_pos(self) -> tuple[int, int]:
        return self.x, self.y

    def move(self):
        d = self.direction
        if d == Direction.NORTH:
            self.y -= 1
        elif d == Direction.EAST:
            self.x += 1
        elif d == Direction.SOUTH:
            self.y += 1
        elif d == Direction.WEST:
            self.x -= 1

    def split_ray(self, vertical: bool = True) -> "Ray":
        return Ray(
            self.x + (not vertical),
            self.y + vertical,
            Direction.SOUTH if vertical else Direction.EAST,
        )

    def react(self, symbol: str) -> RayEvent:
        new_ray = None
        match (symbol, self.direction):
            case "-", (Direction.NORTH | Direction.SOUTH):
                self.direction = Direction.WEST
                new_ray = self.split_ray(False)
            case "|", (Direction.WEST | Direction.EAST):
                self.direction = Direction.NORTH
                new_ray = self.split_ray(True)
            case "\\", _:
                self.right_angle_turn(0)
            case "/", _:
                self.right_angle_turn(1)

        self.move()
        return RayEvent(self.current_pos, new_ray is not None, new_ray)

    def right_angle_turn(self, variant: int):
        reflection_maps = (
            {
                Direction.NORTH: Direction.WEST,
                Direction.EAST: Direction.SOUTH,
                Direction.SOUTH: Direction.EAST,
                Direction.WEST: Direction.NORTH,
            },
            {
                Direction.NORTH: Direction.EAST,
                Direction.EAST: Direction.NORTH,
                Direction.SOUTH: Direction.WEST,
                Direction.WEST: Direction.SOUTH,
            },
        )
        self.direction = reflection_maps[variant][self.direction]


class Grid:
    def __init__(self, rows: list[str]):
        self.width = len(rows[0])
        self.height = len(rows)
        self.symbols = "".join(rows)

    def _to_symbol_index(self, x: int, y: int) -> int:
        return y * self.height + x

    def get_symbol(self, x: int, y: int) -> str | None:
        if self.position_is_valid(x, y):
            return self.symbols[self._to_symbol_index(x, y)]

    def position_is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    @staticmethod
    def was_already_considered(
        ray: Ray, positions: set[tuple[int, int], Direction]
    ) -> bool:
        return (ray.current_pos, ray.direction) in positions

    def progress_ray(self, ray: Ray) -> RayEvent:
        symbol = self.get_symbol(*ray.current_pos)
        return ray.react(symbol)

    def shine_light(self, starting_ray: Ray) -> int:
        bouncing_rays = [starting_ray]
        considered_positions: set[tuple[int, int], Direction] = set()

        while bouncing_rays:
            considered_rays = [
                ray
                for ray in bouncing_rays
                if self.position_is_valid(*ray.current_pos)
                and not self.was_already_considered(ray, considered_positions)
            ]
            next_positions = {
                (ray.current_pos, ray.direction) for ray in considered_rays
            }
            considered_positions |= next_positions

            events = [self.progress_ray(ray) for ray in considered_rays]
            split_rays = [event.new_ray for event in events if event.did_split]
            bouncing_rays = [
                *considered_rays,
                *split_rays,
            ]

        return len({p[0] for p in considered_positions})

    def debug_energized(self, positions: set[tuple[int, int]]):
        energized_indexes = {self._to_symbol_index(*p) for p in positions}
        for i, ch in enumerate(self.symbols):
            if not i % self.width:
                print()
            print(ch if i not in energized_indexes else "#", end="")
        print()


def part_one(data: list[str]) -> int:
    grid = Grid(data)
    return grid.shine_light(Ray(0, 0, Direction.EAST))


def part_two(data: list[str]):
    grid = Grid(data)
    possible_starts = [
        *(Ray(x, 0, Direction.SOUTH) for x in range(grid.width)),
        *(Ray(x, grid.height - 1, Direction.NORTH) for x in range(grid.width)),
        *(Ray(0, y, Direction.EAST) for y in range(grid.height)),
        *(Ray(grid.width - 1, y, Direction.WEST) for y in range(grid.height)),
    ]

    return max(map(grid.shine_light, possible_starts))


parser = argparse.ArgumentParser(description="Solution for Advent of Code 16/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
