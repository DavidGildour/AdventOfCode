"""https://adventofcode.com/2023/day/3"""
import argparse
import re
from dataclasses import dataclass, field
from functools import reduce

Point = tuple[int, int]
NUMBER_RE = re.compile(r"\d+")
SYMBOL_RE = re.compile(r"[^\w.]")


@dataclass
class Number:
    value: int
    span: list[Point]

    def __hash__(self):
        return sum(map(hash, self.span))


class GearError(Exception):
    pass


@dataclass
class Symbol:
    ch: str
    point: Point
    grid: "Schematic"
    _neighbouring_numbers: set[Number] = field(default_factory=set)

    def is_gear(self):
        return self.ch == "*" and len(self.neighboring_numbers) == 2

    @property
    def neighboring_numbers(self) -> set[Number]:
        if not self._neighbouring_numbers:
            self._neighbouring_numbers = self.grid.get_neighboring_numbers(*self.point)
        return self._neighbouring_numbers

    @property
    def ratio(self):
        if not self.is_gear():
            raise GearError("This symbol is not a gear.")
        one, two = self.neighboring_numbers
        return one.value * two.value


class Schematic:
    def __init__(self, lines: list[str]):
        self.number_grid: dict[Point, Number] = dict()
        self.symbol_list: list[Symbol] = []

        for y, line in enumerate(lines):
            self.find_numbers(line, y)
            self.find_symbols(line, y)

    def add_number_to_grid(self, part: Number):
        for point in part.span:
            self.number_grid[point] = part

    def find_numbers(self, line: str, y: int):
        for match in NUMBER_RE.finditer(line):
            value = int(match.group())
            number = Number(value, [(x, y) for x in range(*match.span())])
            self.add_number_to_grid(number)

    def find_symbols(self, line: str, y: int):
        for match in SYMBOL_RE.finditer(line):
            x = match.span()[0]
            self.symbol_list.append(Symbol(match.group(), (x, y), self))

    def get_position(self, x: int, y: int) -> Number | None:
        return self.number_grid.get((x, y))

    def get_neighboring_numbers(self, x: int, y: int) -> set[Number]:
        return set(
            filter(
                None,
                (
                    self.get_position(x - 1, y - 1),
                    self.get_position(x, y - 1),
                    self.get_position(x + 1, y - 1),
                    self.get_position(x - 1, y),
                    self.get_position(x + 1, y),
                    self.get_position(x - 1, y + 1),
                    self.get_position(x, y + 1),
                    self.get_position(x + 1, y + 1),
                ),
            )
        )

    def get_part_numbers(self) -> set[Number]:
        return reduce(
            lambda x, y: x | y,
            (symbol.neighboring_numbers for symbol in self.symbol_list),
            set(),
        )

    def get_gears(self) -> list[Symbol]:
        return [symbol for symbol in self.symbol_list if symbol.is_gear()]


def part_one(schematic: Schematic) -> int:
    return sum(part.value for part in schematic.get_part_numbers())


def part_two(schematic: Schematic):
    return sum(symbol.ratio for symbol in schematic.get_gears())


parser = argparse.ArgumentParser(description="Solution for Advent of Code 3/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    schema = Schematic(raw_data)
    first_answer = part_one(schema)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(schema)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
