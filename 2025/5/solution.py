"""https://adventofcode.com/2025/day/5"""

import argparse
import logging
from typing import Callable
import timeit

#####################  <UTILS> #####################

parser = argparse.ArgumentParser(description="Solution for Advent of Code 5/2025.")
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


def parse_range(range_str: str) -> range:
    a, b = map(int, range_str.split("-"))
    return range(a, b + 1)


def validate(x: int, ranges_to_check: list[str]) -> bool:
    if len(ranges_to_check) == 0:
        return False

    range_str, *rest = ranges_to_check
    return x in parse_range(range_str) or validate(x, rest)


def build_condition_pipeline(conditions: list[str]):
    return lambda x: validate(x, conditions)


@timed
def part_one(ranges: list[str], id_list: list[str]) -> int:
    validator = build_condition_pipeline(ranges)
    return sum(validator(int_id) for int_id in map(int, id_list))


@timed
def part_two(ranges: list[str]) -> int: ...


if __name__ == "__main__":
    cli_args = parser.parse_args()
    filename: str
    if cli_args.test:
        logging.basicConfig(level=logging.DEBUG)
        filename = "./input_test.txt"
        print("Running 2025/5 solution on test input.")
    else:
        filename = "./input.txt"
        print("Running 2025/5 solution on full input.")

    with open(filename) as file:
        contents = file.read()
        ranges_str, id_str = contents.split("\n\n")

        ranges_data = ranges_str.split("\n")
        id_data = id_str.split("\n")

    first_answer = part_one(ranges_data, id_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(ranges_data, id_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
