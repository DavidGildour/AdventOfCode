"""https://adventofcode.com/2023/day/15"""
import argparse
from functools import reduce


def ascii_hash(s: str) -> int:
    return reduce(lambda x, y: ((x + ord(y)) * 17) % 256, s, 0)


def part_one(data: list[str]):
    return sum(map(ascii_hash, data))


def part_two(data: list[str]):
    ...


parser = argparse.ArgumentParser(description="Solution for Advent of Code 15/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = f.read().strip().split(",")

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
