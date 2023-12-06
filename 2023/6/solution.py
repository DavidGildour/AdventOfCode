"""https://adventofcode.com/2023/day/6"""
import argparse
import re
from functools import reduce
from itertools import starmap
from math import sqrt, floor, ceil

NUMBER_RE = f"\d+"


def get_numbers(s: str) -> list[int]:
    return [int(x) for x in re.findall(NUMBER_RE, s)]


def get_single_number(s: str) -> int:
    return int("".join(re.findall(NUMBER_RE, s)))


def delta(a: int, b: int, c: int) -> tuple[int, int]:
    return (-b - sqrt(b**2 - 4 * a * c)) / 2 * a, (
        -b + sqrt(b**2 - 4 * a * c)
    ) / 2 * a


def get_margin(t: int, d: int) -> int:
    x1, x2 = delta(-1, t, -d)
    return ceil(x1 - 1) - floor(x2)


def part_one(data: list[str]) -> int:
    return reduce(
        lambda a, b: a * b,
        starmap(get_margin, zip(*map(get_numbers, data))),
    )


def part_two(data: list[str]):
    return get_margin(*map(get_single_number, data))


parser = argparse.ArgumentParser(description="Solution for Advent of Code 6/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
