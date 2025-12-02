"""This is a small script for creating the boilerplate for the new AoC day for this repository."""

import argparse
import os
from pathlib import Path


parser = argparse.ArgumentParser(
    description="Create a boilerplate code and directory structure (in a current directory!) for a challenge on"
    "a specific day of a specific year of Advent of Code event."
)
parser.add_argument("year", type=int, help="a day on the AoC")
parser.add_argument("day", type=int, help="a year of the AoC")
parser.add_argument(
    "-l",
    "--lang",
    type=str,
    default="py",
    choices=["py", "go"],
    help="a programming language to generate a template for",
)


def create_boilerplate(year: int, day: int, language: str) -> str:
    base = Path() / str(year) / str(day)
    os.makedirs(base, exist_ok=True)

    solution = base / f"solution.{language}"
    input_test = base / "input_test.txt"
    input_proper = base / "input.txt"

    if os.path.exists(solution):
        return f"Boilerplate ({language}) for AoC {year}/{day} already exists."
    solution.touch(exist_ok=True)
    input_test.touch(exist_ok=True)
    input_proper.touch(exist_ok=True)

    with (
        open(solution, "w") as output_file,
        open(f"templates/{language}.template") as template_file,
    ):
        template_str = template_file.read()
        output_file.write(template_str.format(year=year, day=day))

    return f"Created ({language}) boilerplate for AoC {year}/{day}."


if __name__ == "__main__":
    args = parser.parse_args()
    message = create_boilerplate(args.year, args.day, args.lang)
    print(message)
