"""https://adventofcode.com/2024/day/3"""
import argparse
import re
from typing import Callable
import timeit


def timed(f: Callable) -> Callable:
    """Decorator to time the execution of a function."""
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = f(*args, **kwargs)
        end_time = timeit.default_timer()
        print(f"Function {f.__name__} took {end_time - start_time:.6f} seconds")
        return result
    return wrapper


@timed
def part_one(data: str) -> int:
    r = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    return sum(int(m.group(1)) * int(m.group(2)) for m in r.finditer(data))


@timed
def part_two(data: list[str]):
    r = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")
    res = 0
    enabled = True

    for m in r.finditer(data):
        match m.group(0):
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _ if enabled:
                res += int(m.group(1)) * int(m.group(2))

    return res


parser = argparse.ArgumentParser(description="Solution for Advent of Code 3/2024.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename: str
    if args.test:
        filename = "./input_test.txt"
        print("Running 2024/3 solution on test input.")
    else:
        filename = "./input.txt"
        print("Running 2024/3 solution on full input.")

    with open(filename) as f:
        raw_data = f.read()

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
