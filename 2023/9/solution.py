"""https://adventofcode.com/2023/day/9"""
import argparse


def get_sequence(s: str) -> list[int]:
    return [int(x) for x in s.split()]


def get_derivative(sequence: list[int]) -> list[int]:
    return [x - y for x, y in zip(sequence[1:], sequence)]


def is_constant(sequence: list[int]) -> bool:
    return len(set(sequence)) == 1


def get_arithmetic_difference_or_none(sequence: list[int]) -> int | None:
    if is_constant(derivative := get_derivative(sequence)):
        return derivative.pop()


def extrapolate(sequence: list[int]) -> int:
    if (diff := get_arithmetic_difference_or_none(sequence)) is not None:
        return sequence[-1] + diff
    return sequence[-1] + extrapolate(get_derivative(sequence))


def extrapolate_backwards(sequence: list[int]) -> int:
    if (diff := get_arithmetic_difference_or_none(sequence)) is not None:
        result = sequence[0] - diff
        return result
    return sequence[0] - extrapolate_backwards(get_derivative(sequence))


def part_one(data: list[str]) -> int:
    return sum(map(extrapolate, map(get_sequence, data)))


def part_two(data: list[str]) -> int:
    return sum(map(extrapolate_backwards, map(get_sequence, data)))


parser = argparse.ArgumentParser(description="Solution for Advent of Code 9/2023.")
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
