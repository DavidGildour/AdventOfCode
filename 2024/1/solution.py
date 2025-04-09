"""https://adventofcode.com/2024/day/1"""
import argparse
import timeit
from collections import Counter
from typing import Callable


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
def part_one(left_list: list[int], right_list: list[int]) -> int:
    return sum(abs(a - b) for a, b in zip(sorted(left_list), sorted(right_list)))


@timed
def part_two(left_list: list[int], right_list: list[int]) -> int:
    c = Counter(right_list)

    return sum(x * c[x] for x in left_list)


parser = argparse.ArgumentParser(description="Solution for Advent of Code 1/2024.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")


def parse_lists(data_str: list[str]) -> tuple[list[int], list[int]]:
    nums = [map(int, row.split()) for row in data_str]

    return tuple(zip(*nums))


if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    left, right = parse_lists(raw_data)

    first_answer = part_one(left, right)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(left, right)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
