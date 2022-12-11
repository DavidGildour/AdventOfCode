"""https://adventofcode.com/2022/day/11"""
from functools import reduce
from operator import mul

from parser import Parser


def part_one(data: list[str]) -> int:
    monkes = Parser.parse_input(data)
    for _ in range(20):
        for monke in monkes:
            while monke.items:
                current_item = monke.inspect_next_item()
                current_item = monke.operation(current_item) // 3
                monkes[
                    monke.monkey_targets[current_item % monke.divisor == 0]
                ].items.append(current_item)

    return reduce(mul, sorted(m.inspection_count for m in monkes)[-2:])


def part_two(data: list[str]):
    monkes = Parser.parse_input(data)
    product = reduce(mul, (monke.divisor for monke in monkes))
    for i in range(10000):
        for monke in monkes:
            while monke.items:
                current_item = monke.inspect_next_item()
                current_item = monke.operation(current_item) % product
                monkes[
                    monke.monkey_targets[current_item % monke.divisor == 0]
                ].items.append(current_item)

    return reduce(mul, sorted(m.inspection_count for m in monkes)[-2:])


if __name__ == "__main__":
    with open("./input.txt") as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
