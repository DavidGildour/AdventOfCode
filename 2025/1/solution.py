"""https://adventofcode.com/2025/day/1"""
import argparse
import logging
from dataclasses import dataclass
from typing import Callable, Generator
import timeit

#####################  <UTILS> #####################

parser = argparse.ArgumentParser(description="Solution for Advent of Code 1/2025.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")


def timed(func: Callable) -> Callable:
    """Decorator to time the execution of a function."""
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds")
        return result
    return wrapper

##################### </UTILS> #####################


DIAL_RANGE = 100
DIAL_START_VALUE = 50
DIAL_ZERO_VALUE = 0


@dataclass
class Rotation:
    raw_str: str
    direction: int
    value: int
    previous_position: int

    @property
    def total_rotation(self) -> int:
        return self.direction * self.value

    @property
    def relative_rotation(self) -> int:
        return self.previous_position + self.total_rotation

    @property
    def resulting_position(self) -> int:
        return self.relative_rotation % DIAL_RANGE

    def ends_on_zero(self) -> bool:
        return self.resulting_position == DIAL_ZERO_VALUE

    def count_zero_ticks(self) -> int:
        rotations = abs(self.relative_rotation // DIAL_RANGE)
        if self.direction == -1:
            rotations -= int(self.previous_position == DIAL_ZERO_VALUE)
            rotations += int(self.ends_on_zero())

        return rotations

    def __str__(self):
        base_str = super().__str__()[:-1]
        base_str += f", relative_rotation={self.relative_rotation}"
        base_str += f", resulting_position={self.resulting_position}"
        base_str += f", ends_on_zero={int(self.ends_on_zero())}"
        return base_str + ")"

    @classmethod
    def from_string(cls, input_string: str, previous_position: int) -> "Rotation":
        direction, value = input_string[0], int(input_string[1:])
        sign = 1 if direction == "R" else -1
        return cls(raw_str=input_string, direction=sign, value=value, previous_position=previous_position)


def rotation_generator(data: list[str]) -> Generator[Rotation, None, None]:
    current_position = DIAL_START_VALUE
    for rotation_str in data:
        new_rotation = Rotation.from_string(rotation_str, current_position)
        yield new_rotation
        current_position = new_rotation.resulting_position


@timed
def part_one(data: list[str]) -> int:
    return sum(rot.ends_on_zero() for rot in rotation_generator(data))


@timed
def part_two(data: list[str]):
    return sum(rot.count_zero_ticks() for rot in rotation_generator(data))


if __name__ == "__main__":
    args = parser.parse_args()
    filename: str
    if args.test:
        logging.basicConfig(level=logging.DEBUG)
        filename = "./input_test.txt"
        print("Running 2025/1 solution on test input.")
    else:
        filename = "./input.txt"
        print("Running 2025/1 solution on full input.")

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
