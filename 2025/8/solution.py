"""https://adventofcode.com/2025/day/8"""

import argparse
import logging
from functools import cache, reduce
from operator import mul

from typing import Callable
import timeit

from point import Point
from circuit_tracker import CircuitTracker


#####################  <UTILS> #####################

parser = argparse.ArgumentParser(description="Solution for Advent of Code 8/2025.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")


def timed(f: Callable) -> Callable:
    """Decorator to time the execution of a function."""

    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = f(*args, **kwargs)
        end_time = timeit.default_timer()
        print(f"Function {f.__name__} took {end_time - start_time:.6f} seconds")
        return result

    return wrapper


##################### </UTILS> #####################


@cache
def parse_boxes(data: tuple[str]) -> list[Point]:
    return [Point(*map(int, row.split(","))) for row in data]


def sorted_pair[Comparable](
    a: Comparable, b: Comparable
) -> tuple[Comparable, Comparable]:
    return (a, b) if a >= b else (b, a)


type DistanceDict = dict[tuple[Point, Point], float]


def initialize_circuits_and_calculate_distances(
    boxes: list[Point],
) -> tuple[CircuitTracker, DistanceDict]:
    circuits = CircuitTracker()
    distances: DistanceDict = dict()

    for i, box in enumerate(boxes, 1):
        circuits.add_circuit(box)
        for another_box in boxes[i:]:
            dict_key = sorted_pair(another_box, box)
            if dict_key not in distances:
                dist = box.distance_to(another_box)
                distances[dict_key] = dist

    return circuits, distances


@timed
def part_one(data: tuple[str], connection_limit: int) -> int:
    boxes = parse_boxes(data)

    circuits, distances = initialize_circuits_and_calculate_distances(boxes)

    sorted_pair_points = sorted(
        ((a, b, dist) for (a, b), dist in distances.items()), key=lambda x: x[2]
    )
    for a, b, _ in sorted_pair_points[:connection_limit]:
        circuits.merge_circuits(a.circuit_id, b.circuit_id)

    return reduce(mul, map(len, circuits.sorted()[-3:]))


@timed
def part_two(data: tuple[str]) -> int:
    boxes = parse_boxes(data)

    circuits, distances = initialize_circuits_and_calculate_distances(boxes)

    sorted_pair_points = sorted(
        ((a, b, dist) for (a, b), dist in distances.items()), key=lambda x: x[2]
    )
    last_connected_pair: tuple[Point, Point] | None = None
    for a, b, _ in sorted_pair_points:
        if a.circuit_id != b.circuit_id:
            circuits.merge_circuits(a.circuit_id, b.circuit_id)
            last_connected_pair = (a, b)

        if circuits.circuit_count() == 1:
            break

    a, b = last_connected_pair
    logging.debug(f"{a=}, {b=}")
    return a.x * b.x


if __name__ == "__main__":
    cli_args = parser.parse_args()
    filename: str
    if cli_args.test:
        logging.basicConfig(level=logging.DEBUG)
        limit = 10
        filename = "./input_test.txt"
        print("Running 2025/8 solution on test input.")
    else:
        limit = 1000
        filename = "./input.txt"
        print("Running 2025/8 solution on full input.")

    with open(filename) as file:
        raw_data = tuple(x.strip() for x in file.readlines())

    first_answer = part_one(raw_data, limit)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
