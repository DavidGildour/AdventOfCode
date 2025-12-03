"""https://adventofcode.com/2025/day/3"""

import argparse
import logging
from typing import Callable
import timeit

#####################  <UTILS> #####################

parser = argparse.ArgumentParser(description="Solution for Advent of Code 3/2025.")
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


def find_joltage_output(battery_bank: str, batteries_left: int) -> str:
    if batteries_left == 0:
        return ""

    bank_subset = (
        battery_bank[: -batteries_left + 1] if batteries_left > 1 else battery_bank
    )
    logging.debug(f"{battery_bank=}, {batteries_left=}, {bank_subset=}")
    max_joltage = max(bank_subset)
    joltage_index = bank_subset.index(max_joltage)

    logging.debug(f"{max_joltage=}, {joltage_index=}")

    return max_joltage + find_joltage_output(
        battery_bank[joltage_index + 1 :], batteries_left - 1
    )


@timed
def part_one(data: list[str]):
    return sum(
        logging.debug(res := find_joltage_output(battery_bank, batteries_left=2))
        or int(res)
        for battery_bank in data
    )


@timed
def part_two(data: list[str]):
    return sum(
        logging.debug(res := find_joltage_output(battery_bank, batteries_left=12))
        or int(res)
        for battery_bank in data
    )


if __name__ == "__main__":
    args = parser.parse_args()
    filename: str
    if args.test:
        logging.basicConfig(level=logging.DEBUG)
        filename = "./input_test.txt"
        print("Running 2025/3 solution on test input.")
    else:
        filename = "./input.txt"
        print("Running 2025/3 solution on full input.")

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
