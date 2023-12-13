"""https://adventofcode.com/2023/day/13"""
import argparse


def difference(top_grid: list[str], bottom_grid: list[str]) -> int:
    return sum(
        ch1 != ch2
        for ch1, ch2 in zip("".join(top_grid), "".join(reversed(bottom_grid)))
    )


def find_difference_index(
    grid: list[str], difference_to_find: int, vertical: bool = False
) -> int:
    working_grid = transposed(grid) if vertical else grid
    grid_len = len(working_grid)
    for i in range(1, grid_len):
        sub_grid_len = min(grid_len - i, i)
        top, bottom = working_grid[i - sub_grid_len : i], working_grid[i : 2 * i]
        if difference(top, bottom) == difference_to_find:
            return i

    return 0


def find_proper_reflection(grid: list[str], difference_to_find: int) -> int:
    return (
        horizontal_reflection
        if (
            horizontal_reflection := find_difference_index(grid, difference_to_find)
            * 100
        )
        else find_difference_index(grid, difference_to_find, vertical=True)
    )


def transposed(grid: list[str]) -> list[str]:
    return ["".join(col) for col in zip(*grid)]


def part_one(grids: list[list[str]]) -> int:
    return sum(find_proper_reflection(grid, 0) for grid in grids)


def part_two(grids: list[list[str]]) -> int:
    return sum(find_proper_reflection(grid, 1) for grid in grids)


parser = argparse.ArgumentParser(description="Solution for Advent of Code 13/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [x.split("\n") for x in f.read().split("\n\n")]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
