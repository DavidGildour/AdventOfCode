"""https://adventofcode.com/2022/day/15"""
import re
from itertools import permutations


def manhattan(x1, y1, x2, y2) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def part_one(data: list[str], target_depth: int):
    s = set()
    for line in data:
        sx, sy, bx, by = map(int, re.findall(r"\d+", line))
        radius = manhattan(sx, sy, bx, by)
        if target_depth in range(sy - radius, sy + radius + 1):
            diff = radius - abs(sy - target_depth)
            s |= set(range(sx - diff, sx + diff + 1))
            if by == target_depth:
                s -= {bx}

    return len(s)


def part_two(data: list[str], space: int):
    for s1, s2 in permutations(data, r=2):
        sx1, sy1, bx1, by1 = map(int, re.findall(r"\d+", s1))
        sx2, sy2, bx2, by2 = map(int, re.findall(r"\d+", s2))
        radius1 = manhattan(sx1, sy1, bx1, by1)
        radius2 = manhattan(sx2, sy2, bx2, by2)
        distance = manhattan(sx1, sy1, sx2, sy2)
        if distance == radius1 + radius2 + 2:
            a, c = 1, sy1 - sx1 - radius1 - 1
            b, d = -1, sy2 + sx2 + radius1 + 1
            x = (d - c) * (a - b)
            y = a * x + c
            if x in range(0, space + 1) and y in range(0, space + 1):
                print(x, y)


if __name__ == "__main__":
    file = "./input_test.txt"
    with open(file) as f:
        raw_data = [x.strip() for x in f.readlines()]

    if file == "./input.txt":
        depth = 2_000_000
        limit = 4_000_000
    else:
        depth = 10
        limit = 20
    first_answer = part_one(raw_data, depth)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data, limit)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
