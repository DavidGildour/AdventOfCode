"""https://adventofcode.com/2023/day/15"""
import argparse
import re
from functools import reduce, partial
from itertools import starmap
from typing import Mapping, Callable

INSTRUCTION_REGEX = re.compile(r"(\w+)([-=]\d*)")
type LensList = list[tuple[str, int]]
type BoxMap = Mapping[int, LensList]
type BoxOp = Callable[[BoxMap], BoxMap]


def ascii_hash(s: str) -> int:
    return reduce(lambda x, y: ((x + ord(y)) * 17) % 256, s, 0)


def remove_lens(lens_id: str, box_id: int, boxes: BoxMap) -> BoxMap:
    return {
        **boxes,
        box_id: list(filter(lambda l: l[0] != lens_id, boxes.get(box_id, list()))),
    }


def update_lens(lens: tuple[str, int], box_id: int, boxes: BoxMap) -> BoxMap:
    return {**boxes, box_id: put_lens_into_list(boxes.get(box_id, list()), lens)}


def put_lens_into_list(box: LensList, lens: tuple[str, int]) -> LensList:
    lens_id = lens[0]
    present_ids = [l[0] for l in box]
    if lens_id in present_ids:
        idx = present_ids.index(lens_id)
        return [*box[:idx], lens, *box[idx + 1 :]]
    return [*box, lens]


def get_operation(lens_id: str, op_str: str) -> BoxOp:
    box_id = ascii_hash(lens_id)
    if op_str.startswith("="):
        lens = (lens_id, int(op_str[1:]))
        return partial(update_lens, lens, box_id)
    return partial(remove_lens, lens_id, box_id)


def sum_fpowers(box_id: int, lenses: LensList) -> int:
    return sum((box_id + 1) * i * lens[1] for i, lens in enumerate(lenses, 1))


def part_one(data: str) -> int:
    return sum(map(ascii_hash, data.split(",")))


def part_two(data: str):
    boxes = reduce(
        lambda x, fn: fn(x),
        (get_operation(*m.groups()) for m in INSTRUCTION_REGEX.finditer(data)),
        dict(),
    )

    return sum(starmap(sum_fpowers, boxes.items()))


parser = argparse.ArgumentParser(description="Solution for Advent of Code 15/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = f.read().strip()

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
