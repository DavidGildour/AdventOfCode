"""https://adventofcode.com/2024/day/4"""
import argparse
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
def part_one(data: list[str]):
    ...


@timed
def part_two(data: list[str]):
    ...


parser = argparse.ArgumentParser(description="Solution for Advent of Code 4/2024.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename: str
    if args.test:
        filename = "./input_test.txt"
        print("Running 2024/4 solution on test input.")
    else:
        filename = "./input.txt"
        print("Running 2024/4 solution on full input.")

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
