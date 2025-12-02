"""https://adventofcode.com/2022/day/12"""

from grid import Grid


def part_one(grid: Grid) -> int:
    return len(grid.find_best_path(from_=grid.start_area)) - 1


def part_two(grid: Grid) -> int:
    return min(
        len(route) - 1
        for candidate in filter(lambda a: a.height == 0, grid.height_map.values())
        if (route := grid.find_best_path(from_=candidate))
    )


def part_two_alternative(grid: Grid) -> int:
    return len(grid.find_first_a()) - 1


if __name__ == "__main__":
    with open("./input.txt") as f:
        raw_data = [x.strip() for x in f.readlines()]

    input_grid = Grid(raw_data)

    first_answer = part_one(input_grid)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two_alternative(input_grid)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
