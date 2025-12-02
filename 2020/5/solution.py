"""https://adventofcode.com/2020/day/5"""

import argparse
from math import ceil
from typing import Iterator


def binary_search(start: int, end: int, direction_iter: Iterator[bool]) -> int:
    if start == end:
        return start
    left = next(direction_iter)
    new_start = start if left else ceil((start + end) / 2)
    new_end = (start + end) // 2 if left else end
    return binary_search(new_start, new_end, direction_iter)


def get_seat_id(b_pass: str) -> int:
    row_search, col_search = b_pass[:7], b_pass[7:]
    row = binary_search(0, 127, iter(c == "F" for c in row_search))
    col = binary_search(0, 7, iter(c == "L" for c in col_search))

    return row * 8 + col


def part_one(data: list[str]) -> int:
    return max(map(get_seat_id, data))


def part_two(data: list[str]):
    ids = {get_seat_id(s) for s in data}
    first_id, last_id = min(ids), max(ids)
    missing_ids = set(range(first_id, last_id + 1)) - ids

    return [*missing_ids].pop()


parser = argparse.ArgumentParser(description="Solution for Advent of Code 5/2020.")
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
