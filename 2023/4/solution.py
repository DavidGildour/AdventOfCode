"""https://adventofcode.com/2023/day/4"""
import argparse


class CountdownStack(list):
    def expand(self, length: int, times: int):
        diff = max(length - len(self), 0)
        self.extend([0] * diff)

        for i in range(length):
            self[i] += times

    def smart_shift(self) -> int:
        if not self:
            return 1
        return self.pop(0) + 1


def get_winning_numbers(card: str) -> set[int]:
    _card_no, numbers = card.split(": ")
    winning_numbers, numbers_you_have = map(
        lambda x: {int(n) for n in x.split()}, numbers.split(" | ")
    )
    return winning_numbers & numbers_you_have


def get_score(card: str) -> int:
    matching_numbers = get_winning_numbers(card)

    return 2 ** (len(matching_numbers) - 1) if matching_numbers else 0


def part_one(data: list[str]) -> int:
    return sum(get_score(card) for card in data)


def part_two(data: list[str]) -> int:
    countdown_stack = CountdownStack()
    total = 0
    for numbers in map(get_winning_numbers, data):
        current_multiplier = countdown_stack.smart_shift()
        total += current_multiplier
        countdown_stack.expand(len(numbers), current_multiplier)

    return total


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
