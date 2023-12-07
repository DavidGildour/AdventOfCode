"""https://adventofcode.com/2023/day/7"""
import argparse
from typing import Type

from hand import Hand, JokerHand


def count_winnings(hand_data: list[str], hand_class: Type[Hand]) -> int:
    hands = sorted(
        [hand_class(line) for line in hand_data],
        key=lambda x: (x.value, [hand_class.get_card_value(c) for c in x.cards]),
    )

    return sum(i * hand.bid for i, hand in enumerate(hands, 1))


def part_one(data: list[str]):
    return count_winnings(data, Hand)


def part_two(data: list[str]):
    return count_winnings(data, JokerHand)


parser = argparse.ArgumentParser(description="Solution for Advent of Code 7/2023.")
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
