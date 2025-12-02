"""https://adventofcode.com/2024/day/2"""

import argparse

INCREASING_SET = {1, 2, 3}
DECREASING_SET = {-1, -2, -3}


def get_diffs(levels: list[int]) -> list[int]:
    return [b - a for a, b in zip(levels, levels[1:])]


def is_safe(levels: list[int]) -> bool:
    diffs = get_diffs(levels)
    return not (set(diffs) - INCREASING_SET and set(diffs) - DECREASING_SET)


def is_safe_with_BRUTE_FORCE(levels: list[int]) -> bool:
    return any(is_safe(levels[: i - 1] + levels[i:]) for i in range(1, len(levels) + 1))


def part_one(data: list[list[int]]) -> int:
    return sum(map(is_safe, data))


def part_two(data: list[list[int]]) -> int:
    return len(
        [
            levels
            for levels in data
            if is_safe(levels) or is_safe_with_BRUTE_FORCE(levels)
        ]
    )


parser = argparse.ArgumentParser(description="Solution for Advent of Code 2/2024.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [list(map(int, x.strip().split())) for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
