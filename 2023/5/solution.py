"""https://adventofcode.com/2023/day/5"""
import argparse
from functools import reduce
from itertools import batched
from timeit import default_timer
from typing import Iterable, Callable

NumMapper = Callable[[int], int]
Range = tuple[int, int]
RangeMapper = Callable[[list[Range]], list[Range]]


def make_map_function1(map_ranges: list[tuple[int, ...]]) -> NumMapper:
    def _mapper(num: int) -> int:
        for dest_start, source_start, length in map_ranges:
            if 0 <= (diff := num - source_start) < length:
                return dest_start + diff

        return num

    return _mapper


def is_overlapping(seed_range: Range, map_range: Range) -> bool:
    seed_start, seed_length = seed_range
    map_start, map_length = map_range

    if seed_start < map_start:
        return map_start - seed_start < seed_length
    else:
        return seed_start - map_start < map_length


def make_map_function2(map_ranges: list[tuple[int, ...]]) -> RangeMapper:
    def _mapper(num_ranges: list[Range]) -> list[Range]:
        new_ranges = []
        remaining = [*num_ranges]
        leftovers = []

        for dest_start, *map_range in map_ranges:
            leftovers = []
            for seed_range in remaining:
                seed_start, seed_length = seed_range
                if is_overlapping(seed_range, map_range):
                    source_start, map_length = map_range
                    source_end = source_start + map_length - 1
                    seed_end = seed_start + seed_length - 1

                    overlap_start = max(seed_start, source_start)
                    overlap_end = min(seed_end, source_end)
                    overlap_offset = overlap_start - source_start
                    overlap_length = (overlap_end - overlap_start) + 1

                    if seed_start < source_start:
                        leftovers.append((seed_start, source_start - seed_start))

                    if seed_end > source_end:
                        leftovers.append((source_end + 1, seed_end - source_end))

                    new_ranges.append((dest_start + overlap_offset, overlap_length))
                else:
                    leftovers.append(seed_range)

            remaining = leftovers

        return new_ranges + leftovers

    return _mapper


def get_ints_from_string(s: str) -> Iterable[int]:
    return map(int, s.split())


def get_ranges_from_string(s: str) -> list[Range]:
    return list(batched(get_ints_from_string(s), 2))


def map_seed_to_location(maps: list[NumMapper], seed_num: int) -> int:
    return reduce(lambda c, fun: fun(c), maps, seed_num)


def map_seed_ranges_to_location(
    maps: list[RangeMapper], seed_ranges: list[Range]
) -> list[Range]:
    return reduce(lambda c, fun: fun(c), maps, seed_ranges)


def parse_map(map_data: str, variant: int = 0) -> NumMapper | RangeMapper:
    _name, *map_ranges = map_data.split("\n")
    map_numbers = [tuple(get_ints_from_string(s)) for s in map_ranges]

    return (
        make_map_function2(map_numbers) if variant else make_map_function1(map_numbers)
    )


def part_one(seed_data: str, *map_data: str) -> int:
    maps = [parse_map(raw_map) for raw_map in map_data]

    return min(
        map_seed_to_location(maps, seed_num)
        for seed_num in get_ints_from_string(seed_data.lstrip("seeds: "))
    )


def part_two(seed_data: str, *map_data: str):
    seed_ranges = get_ranges_from_string(seed_data.lstrip("seeds: "))
    maps = [parse_map(raw_map, variant=1) for raw_map in map_data]

    return sorted(map(lambda x: x[0], map_seed_ranges_to_location(maps, seed_ranges))).pop(0)


parser = argparse.ArgumentParser(description="Solution for Advent of Code 5/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_seeds, *raw_maps = f.read().split("\n\n")

    _start = default_timer()
    first_answer = part_one(raw_seeds, *raw_maps)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_seeds, *raw_maps)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
    print(f"Took {default_timer() - _start} s.")
