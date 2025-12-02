"""https://adventofcode.com/2022/day/13"""

from functools import cmp_to_key, reduce
from itertools import chain
from operator import mul


def pair_is_valid(left: list | int, right: list | int) -> int | None:
    match [left, right]:
        case [int(), int()]:
            if left != right:
                return 1 if left < right else -1
        case [list(), list()]:
            for left_in, right_in in zip(left, right):
                if (result := pair_is_valid(left_in, right_in)) is not None:
                    return result
            if len(left) != len(right):
                return 1 if len(left) < len(right) else -1
        case [list(), int()]:
            if (result := pair_is_valid(left, [right])) is not None:
                return result
        case [int(), list()]:
            if (result := pair_is_valid([left], right)) is not None:
                return result


def part_one(pairs: list[tuple]) -> int:
    return sum(
        i for i, (left, right) in enumerate(pairs, 1) if pair_is_valid(left, right) > 0
    )


def part_two(pairs: list[tuple]) -> int:
    divider_packets = [[[2]], [[6]]]
    packets_unordered = list(chain.from_iterable(pairs)) + divider_packets
    sorted_packets = sorted(
        packets_unordered, key=cmp_to_key(pair_is_valid), reverse=True
    )

    divider_strings = set(map(str, divider_packets))
    return reduce(
        mul,
        (
            i
            for i, packet in enumerate(sorted_packets, 1)
            if str(packet) in divider_strings
        ),
    )


def parse_data(file: str) -> list[tuple]:
    with open(file) as f:
        return [
            tuple(eval(p) for p in raw_pair.split())
            for raw_pair in f.read().split("\n\n")
        ]


if __name__ == "__main__":
    packet_pairs = parse_data("input.txt")

    first_answer = part_one(packet_pairs)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(packet_pairs)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
