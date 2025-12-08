"""https://adventofcode.com/2025/day/6"""

import argparse
import logging
import re
from functools import reduce
from operator import add, mul
from typing import Callable
import timeit

#####################  <UTILS> #####################

parser = argparse.ArgumentParser(description="Solution for Advent of Code 6/2025.")
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


ADD = "+"
MUL = "*"
NUL = " "

oper = {"+": add, "*": mul}


def naive_parsing(data: list[str]) -> tuple[list[tuple[int]], list[str]]:
    regex = r"\s+"
    *raw_numbers, operators = map(lambda s: re.split(regex, s.strip()), data)
    numbers = list(zip(*(list(map(int, row)) for row in raw_numbers)))

    return numbers, operators


def str_get(l: str, i: int) -> str:
    try:
        return l[i]
    except IndexError:
        return " "


def rtl_parsing(data: list[str]) -> tuple[list[tuple[int]], list[str]]:
    max_index = max(map(len, data)) - 1

    number_set = []
    numbers = []
    operators = []
    for i in range(max_index, -1, -1):
        *digits, operator = (str_get(row, i) for row in data)

        if set(digits) != {NUL}:
            number_set.append(int("".join(digits)))

        if operator != NUL:
            operators.append(operator)
            numbers.append(number_set)
            number_set = []

    return numbers, operators


def get_reducer(op: str) -> Callable:
    return lambda x, y: oper[op](x, y)


@timed
def part_one(data: list[str]) -> int:
    numbers, operators = naive_parsing(data)

    return sum(
        reduce(get_reducer(operator), number_set)
        for number_set, operator in zip(numbers, operators)
    )


@timed
def part_two(data: list[str]) -> int:
    numbers, operators = rtl_parsing(data)

    return sum(
        reduce(get_reducer(operator), number_set)
        for number_set, operator in zip(numbers, operators)
    )


if __name__ == "__main__":
    cli_args = parser.parse_args()
    filename: str
    if cli_args.test:
        logging.basicConfig(level=logging.DEBUG)
        filename = "./input_test.txt"
        print("Running 2025/6 solution on test input.")
    else:
        filename = "./input.txt"
        print("Running 2025/6 solution on full input.")

    with open(filename) as file:
        raw_data = [x.rstrip("\n") for x in file.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
