"""https://adventofcode.com/2023/day/8"""

import argparse
import re
import timeit
from itertools import cycle
from math import lcm
from typing import Iterator

LOCATION_REGEX = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")
START_LOC = "AAA"
DESTINATION = "ZZZ"
LocationMap = dict[str, dict[str, str]]


def parse_location(location_string: str) -> tuple[str, str, str]:
    name, left, right = LOCATION_REGEX.match(location_string).groups()

    return name, left, right


def parse_input(
    pattern: str, location_data: list[str]
) -> tuple[Iterator[tuple[int, str]], LocationMap]:
    return enumerate(cycle(pattern)), {
        name: {"R": right, "L": left}
        for name, left, right in map(parse_location, location_data)
    }


def part_one(pattern: str, location_data: list[str]) -> int:
    stepper, location_map = parse_input(pattern, location_data)

    current_loc = START_LOC
    step = 0
    while current_loc != DESTINATION:
        step, next_move = next(stepper)
        current_loc = location_map[current_loc][next_move]

    return step


def part_two(pattern: str, location_data: list[str]) -> int:
    stepper, location_map = parse_input(pattern, location_data)

    current_nodes = [name for name in location_map if name.endswith("A")]
    steps = []
    while current_nodes:
        step, next_move = next(stepper)
        finished_nodes = [node for node in current_nodes if node.endswith("Z")]
        if finished_nodes:
            steps.append(step)
        current_nodes = [
            location_map[node][next_move]
            for node in current_nodes
            if node not in finished_nodes
        ]

    return lcm(*steps)


parser = argparse.ArgumentParser(description="Solution for Advent of Code 8/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        move_pattern, rest = f.read().split("\n\n")
        locations = [x.strip() for x in rest.split("\n")]

    start = timeit.default_timer()
    first_answer = part_one(move_pattern, locations)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(move_pattern, locations)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
