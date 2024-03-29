"""This is a small script for creating the boilerplate for the new AoC day for this repository."""
import argparse
import os
from pathlib import Path

TEMPLATE = """\"\"\"https://adventofcode.com/{year}/day/{day}\"\"\"
import argparse


def part_one(data: list[str]):
    ...


def part_two(data: list[str]):
    ...


parser = argparse.ArgumentParser(description="Solution for Advent of Code {day}/{year}.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {{first_answer}}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {{second_answer}}.")
"""

parser = argparse.ArgumentParser(
    description="Create a boilerplate code and directory structure (in a current directory!) for a challenge on"
    "a specific day of a specific year of Advent of Code event."
)
parser.add_argument("year", type=int, help="a day on the AoC")
parser.add_argument("day", type=int, help="a year of the AoC")


def create_boilerplate(year: int, day: int):
    base = Path() / str(year) / str(day)
    os.makedirs(base, exist_ok=True)

    solution = base / "solution.py"
    input_test = base / "input_test.txt"
    input_proper = base / "input.txt"
    try:
        solution.touch(exist_ok=False)
        input_test.touch(exist_ok=False)
        input_proper.touch(exist_ok=False)
    except FileExistsError as e:
        return (
            f"Failed to create boilerplate, are you sure you typed the new day instead of an existing one?\n"
            f"ERROR: {e}"
        )

    with open(solution, "w") as f:
        f.write(TEMPLATE.format(year=year, day=day))

    return f"Created boilerplate for AoC {year}/{day}."


if __name__ == "__main__":
    args = parser.parse_args()
    message = create_boilerplate(args.year, args.day)
    print(message)
