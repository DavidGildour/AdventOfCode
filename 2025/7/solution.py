"""https://adventofcode.com/2025/day/7"""

import argparse
import logging
import re
from collections import defaultdict
from functools import reduce
from typing import Callable
import timeit

#####################  <UTILS> #####################

parser = argparse.ArgumentParser(description="Solution for Advent of Code 7/2025.")
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


@timed
def part_one(data: list[str]):
    start_row, *rest = data
    beam_indexes = {start_row.index("S")}
    split_count = 0

    for row in rest[1::2]:
        splitter_indexes = {m.start() for m in re.finditer(r"\^", row)}
        intersections = beam_indexes & splitter_indexes

        split_count += len(intersections)

        beam_indexes -= intersections
        beam_indexes = reduce(
            lambda acc, point: acc | {point - 1, point + 1}, intersections, beam_indexes
        )

    return split_count


@timed
def part_two(data: list[str]):
    start_row, *rest = data
    timeline_counter = {start_row.index("S"): 1}

    for row in rest[1::2]:
        splitter_indexes = {m.start() for m in re.finditer(r"\^", row)}
        intersections = set(timeline_counter) & splitter_indexes

        for point in intersections:
            timeline_counter[point - 1] = timeline_counter.get(
                point - 1, 0
            ) + timeline_counter.get(point)
            timeline_counter[point + 1] = timeline_counter.get(
                point + 1, 0
            ) + timeline_counter.get(point)
            del timeline_counter[point]

    return sum(timeline_counter.values())


if __name__ == "__main__":
    cli_args = parser.parse_args()
    filename: str
    if cli_args.test:
        logging.basicConfig(level=logging.DEBUG)
        filename = "./input_test.txt"
        print("Running 2025/7 solution on test input.")
    else:
        filename = "./input.txt"
        print("Running 2025/7 solution on full input.")

    with open(filename) as file:
        raw_data = [x.strip() for x in file.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
