"""https://adventofcode.com/2023/day/4"""
import argparse


def get_score(card: str) -> int:
    _card_no, numbers = card.split(": ")
    winning_numbers, numbers_you_have = map(
        lambda x: {int(n) for n in x.split()}, numbers.split(" | ")
    )
    matching_numbers = winning_numbers & numbers_you_have

    return 2 ** (len(matching_numbers) - 1) if matching_numbers else 0


def part_one(data: list[str]):
    return sum(get_score(card) for card in data)


def part_two(data: list[str]):
    ...


parser = argparse.ArgumentParser(description="Solution for Advent of Code 4/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
