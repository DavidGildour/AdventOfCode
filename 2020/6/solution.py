"""https://adventofcode.com/2020/day/6"""
import argparse
from functools import reduce
from typing import Callable


def set_it_up(group: list[str], op: Callable[[set, set], set]) -> int:
    return len(reduce(op, map(set, group)))


def part_one(data: list[list[str]]) -> int:
    return sum(map(lambda x: set_it_up(x, set.union), data))


def part_two(data: list[list[str]]) -> int:
    return sum(map(lambda x: set_it_up(x, set.intersection), data))


parser = argparse.ArgumentParser(description="Solution for Advent of Code 6/2020.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        group_data = f.read().split("\n\n")
        groups = [x.split("\n") for x in group_data]

    first_answer = part_one(groups)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(groups)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
