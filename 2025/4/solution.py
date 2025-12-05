"""https://adventofcode.com/2025/day/4"""

import argparse
import logging
from typing import Callable, Literal
import timeit

#####################  <UTILS> #####################

parser = argparse.ArgumentParser(description="Solution for Advent of Code 4/2025.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")


def timed(f: Callable) -> Callable:
    """Decorator to time the execution of a function."""

    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = f(*args, **kwargs)
        end_time = timeit.default_timer()
        print(f"Function {f.__name__} took {end_time - start_time:.6f} seconds")
        return result

    return wrapper


##################### </UTILS> #####################

CELL_EMPTY = "."
CELL_PAPER = "@"
NEIGHBOUR_LIMIT = 4


class GridIterator:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.current_pos = (0, 0)

    def __next__(self):
        current_x, current_y = self.current_pos
        if current_x == self.grid.width:
            current_y += 1
            current_x = 0
        if current_y >= self.grid.height:
            raise StopIteration

        next_value = (current_x, current_y), self.grid.get_cell(current_x, current_y)
        current_x += 1
        self.current_pos = (current_x, current_y)

        return next_value


class Grid:
    def __init__(self, data: list[str]):
        self.data = data
        self.width = len(data[0])
        self.height = len(data)

    def get_cell(self, x: int, y: int) -> str | None:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.data[y][x]

    def get_neighbours(self, x: int, y: int) -> str:
        return "".join(
            value
            for pos in (
                (x - 1, y - 1),
                (x, y - 1),
                (x + 1, y - 1),
                (x - 1, y),
                (x + 1, y),
                (x - 1, y + 1),
                (x, y + 1),
                (x + 1, y + 1),
            )
            if (value := self.get_cell(*pos)) is not None
        )

    def cell_is_accessible(self, x: int, y: int) -> bool:
        return (
            self.get_cell(x, y) == CELL_PAPER
            and self.get_neighbours(x, y).count(CELL_PAPER) < NEIGHBOUR_LIMIT
        )

    def get_accessible_cells(self) -> list[tuple[int, int]]:
        return [(x, y) for (x, y), _ in self if self.cell_is_accessible(x, y)]

    def __iter__(self):
        return GridIterator(self)

    def __str__(self) -> str:
        return "\n".join(self.data)


@timed
def part_one(data: list[str]):
    grid = Grid(data)

    return len(grid.get_accessible_cells())


@timed
def part_two(data: list[str]):
    grid = Grid(data)
    total_removed_paper = 0

    while True:
        grid_rows = []
        removed_paper = 0
        for y, row in enumerate(grid.data):
            row_builder = []
            for x, cell in enumerate(row):
                if grid.cell_is_accessible(x, y):
                    row_builder.append(CELL_EMPTY)
                    removed_paper += 1
                else:
                    row_builder.append(cell)
            grid_rows.append("".join(row_builder))

        if removed_paper == 0:
            break
        total_removed_paper += removed_paper
        grid = Grid(grid_rows)

    return total_removed_paper


if __name__ == "__main__":
    cli_args = parser.parse_args()
    filename: str
    if cli_args.test:
        logging.basicConfig(level=logging.DEBUG)
        filename = "./input_test.txt"
        print("Running 2025/4 solution on test input.")
    else:
        filename = "./input.txt"
        print("Running 2025/4 solution on full input.")

    with open(filename) as file:
        raw_data = [x.strip() for x in file.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
