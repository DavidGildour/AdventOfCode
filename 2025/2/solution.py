"""https://adventofcode.com/2025/day/2"""

import argparse
import logging
from typing import Callable, Generator
import timeit

#####################  <UTILS> #####################

parser = argparse.ArgumentParser(description="Solution for Advent of Code 2/2025.")
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


class RangeLimit(str):
    def as_int(self):
        return int(self)

    def len(self):
        return len(self)


def is_even(num: int) -> bool:
    return num % 2 == 0


def parse_range(range_data: str) -> tuple[RangeLimit, RangeLimit]:
    start, end = range_data.split("-")
    return RangeLimit(start), RangeLimit(end)


def find_complex_invalid_ids_in_range(
    range_data: str,
) -> Generator[int, None, None]: ...


def find_invalid_ids_in_range(range_data: str) -> Generator[int, None, None]:
    logging.debug(f"Parsing range data: {range_data}")
    start, end = parse_range(range_data)
    logging.debug(f"Range values: {end.as_int() - start.as_int()}")

    min_repeat = (
        start[: start.len() // 2]
        if is_even(start.len())
        else "1" + "0" * (start.len() // 2)
    )
    max_repeat = end[: end.len() // 2] if is_even(end.len()) else "9" * (end.len() // 2)
    logging.debug(f"{min_repeat=}, {max_repeat=}")

    include_min = int(min_repeat * 2) >= start.as_int()
    include_max = int(max_repeat * 2) <= start.as_int()

    final_range = range(
        int(min_repeat) + int(not include_min), int(max_repeat) + int(include_max)
    )
    return (int(str(x) * 2) for x in final_range)


@timed
def part_one(data: list[str]):
    return sum(sum(find_invalid_ids_in_range(range_data)) for range_data in data)


@timed
def part_two(data: list[str]): ...


if __name__ == "__main__":
    args = parser.parse_args()
    filename: str
    if args.test:
        logging.basicConfig(level=logging.DEBUG)
        filename = "./input_test.txt"
        print("Running 2025/2 solution on test input.")
    else:
        filename = "./input.txt"
        print("Running 2025/2 solution on full input.")

    with open(filename) as f:
        raw_data = f.read().strip().split(",")

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
