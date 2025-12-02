"""https://adventofcode.com/2022/day/14"""

from cave import Cave, CaveWithBottom


def part_one(data: list[str]):
    cave = Cave(data)
    return len(list(cave.simulate_sand_dropping()))


def part_two(data: list[str]):
    cave = CaveWithBottom(data)
    return len(list(cave.simulate_sand_dropping()))


if __name__ == "__main__":
    with open("./input.txt") as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
