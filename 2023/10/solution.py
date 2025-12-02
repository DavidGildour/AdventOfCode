"""https://adventofcode.com/2023/day/10"""

import argparse
from typing import Type

from position import Position
from cell import Cell, Start, Ground


class Maze:
    def __init__(self, row_data: list[str]):
        self.grid: dict[Position, Type[Cell]] = dict()
        self.starting_pos = Position((0, 0))
        for x, y, ch in (
            (x, y, ch) for y, row in enumerate(row_data) for x, ch in enumerate(row)
        ):
            cell = Cell.from_symbol(ch, x, y)
            self.grid[Position((x, y))] = cell
            if isinstance(cell, Start):
                self.starting_pos = cell.position

    def get_cell(self, position: Position) -> Type[Cell]:
        return self.grid.get(position, Ground(position))

    def get_loop_from_start(self) -> list[Type[Cell]]:
        current = self.get_cell(self.starting_pos)
        loop_found = False
        visited_set = set()
        visited_list = []

        while not loop_found:
            visited_set.add(current.position)
            visited_list.append(current)

            next_possible_positions = filter(
                lambda p: p not in visited_set,
                current.get_positions_of_connected_cells(),
            )
            next_possible_cells = map(self.get_cell, next_possible_positions)
            next_viable_cells = filter(
                lambda c: current.position in c.get_positions_of_connected_cells(),
                next_possible_cells,
            )

            try:
                next_cell = next(next_viable_cells)
            except StopIteration:
                loop_found = True
            else:
                current = next_cell

        return visited_list

    def calculate_loop_area(self, loop_cells: list[Type[Cell]]) -> int:
        return len(self.grid) - len(loop_cells)


def part_one(data: list[str]) -> int:
    return len(Maze(data).get_loop_from_start()) // 2


def part_two(data: list[str]) -> int:
    maze = Maze(data)
    loop = maze.get_loop_from_start()
    return maze.calculate_loop_area(loop)


parser = argparse.ArgumentParser(description="Solution for Advent of Code 10/2023.")
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
