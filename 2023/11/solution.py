"""https://adventofcode.com/2023/day/11"""
import argparse
from itertools import combinations

EMPTY_VOID = "."
GALAXY = "#"


def find_manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def find_galaxies_in_an_ancient_universe(
    universe: list[str], expansion_rate: int
) -> set[tuple[int, int]]:
    col_expansions, row_expansions = [], []
    galaxies = set()
    for y, row in enumerate(universe):
        if set(row) == {EMPTY_VOID}:
            row_expansions.append(y)
        else:
            for x, spot in enumerate(row):
                if y == 0 and set(row[x] for row in universe) == {EMPTY_VOID}:
                    col_expansions.append(x)
                if spot == GALAXY:
                    col_offset = len(
                        [
                            expansion_index
                            for expansion_index in col_expansions
                            if expansion_index < x
                        ]
                    )
                    row_offset = len(
                        [
                            expansion_index
                            for expansion_index in row_expansions
                            if expansion_index < y
                        ]
                    )
                    galaxies.add(
                        (
                            x + (col_offset * (expansion_rate - 1)),
                            y + (row_offset * (expansion_rate - 1)),
                        )
                    )

    return galaxies


def part_one(data: list[str]) -> int:
    galaxies = find_galaxies_in_an_ancient_universe(data, 2)

    return sum(find_manhattan(a, b) for a, b in combinations(galaxies, 2))


def part_two(data: list[str]):
    galaxies = find_galaxies_in_an_ancient_universe(data, 1_000_000)

    return sum(find_manhattan(a, b) for a, b in combinations(galaxies, 2))


parser = argparse.ArgumentParser(description="Solution for Advent of Code 11/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
