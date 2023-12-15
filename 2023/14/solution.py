"""https://adventofcode.com/2023/day/14"""
import argparse
import re
from copy import copy
from typing import Generator

SPHERE = "O"
CUBE = "#"


def cycle(grid: list[str]) -> list[str]:
    return exhaust(rotator(grid, 4))


def rotator(grid: list[str], times: int) -> Generator:
    previous = copy(grid)
    for i in range(times):
        previous = tilt_and_rotate(previous)
        yield previous


def exhaust(gen: Generator):
    result = None
    while True:
        try:
            result = next(gen)
        except StopIteration:
            return result


def tilt_and_rotate(grid: list[str]) -> list[str]:
    return [
        re.sub(
            r"[O.]+",
            lambda m: "".join(sorted(m.group(), key=lambda ch: ch == ".")),
            row,
        )
        for row in rotate(grid)
    ]


def rotate(grid: list[str]):
    return ["".join(col) for col in zip(*grid[::-1])]


def calculate_load(row: str) -> int:
    row_length = len(row)
    return sum(row_length - i for i, ch in enumerate(row) if ch == SPHERE)


def calculate_total_load(grid: list[str]) -> int:
    return sum(calculate_load(row) for row in grid)


def hash_grid(grid: list[str]) -> str:
    return "".join(grid)


def get_loop_length(hash_map: dict, start: str) -> int:
    current = start
    loop_length = 0
    while not loop_length or current != start:
        _next = hash_map[current]
        loop_length += 1
        current = _next

    return loop_length


def part_one(data: list[str]) -> int:
    return calculate_total_load(tilt_and_rotate(rotate(rotate(data))))


def part_two(data: list[str]) -> int:
    initial = rotate(rotate(data))
    total_cycles = 1_000_000_000
    cycle_map = dict()
    current = initial
    for i in range(total_cycles):
        grid_hash = hash_grid(current)
        if grid_hash in cycle_map:
            loop_length = get_loop_length(cycle_map, grid_hash)
            loop_start = len(cycle_map) - loop_length
            odd_cycles = (total_cycles - loop_start) % loop_length
            final_cycle = current
            for j in range(odd_cycles):
                final_cycle = cycle(final_cycle)
            return calculate_total_load(rotate(final_cycle))
        next_cycle = cycle(current)
        cycle_map[grid_hash] = hash_grid(next_cycle)
        current = next_cycle


parser = argparse.ArgumentParser(description="Solution for Advent of Code 14/2023.")
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
