"""https://adventofcode.com/2023/day/2"""
import argparse
import re
from dataclasses import dataclass


class REGEX:
    RED = re.compile(r"(\d+) red")
    GREEN = re.compile(r"(\d+) green")
    BLUE = re.compile(r"(\d+) blue")


@dataclass
class Draw:
    r: int
    g: int
    b: int


class Bag(Draw):
    def draw_is_possible(self, draw: Draw) -> bool:
        return draw.r <= self.r and draw.g <= self.g and draw.b <= self.b

    @property
    def power(self):
        return self.r * self.g * self.b


@dataclass
class Game:
    id: int
    draws: list[Draw]

    def is_possible(self, bag: Bag) -> bool:
        return all(bag.draw_is_possible(draw) for draw in self.draws)

    def find_minimal_bag(self) -> Bag:
        return Bag(
            r=max(draw.r for draw in self.draws),
            g=max(draw.g for draw in self.draws),
            b=max(draw.b for draw in self.draws),
        )


def part_one(lines: list[str]) -> int:
    bag = Bag(12, 13, 14)
    return sum(game.id for game in map(parse_game, lines) if game.is_possible(bag))


def part_two(lines: list[str]) -> int:
    return sum(
        bag.power
        for bag in map(lambda line: parse_game(line).find_minimal_bag(), lines)
    )


def parse_draw(draw_data: str) -> Draw:
    return Draw(
        r=int(match.group(1)) if (match := REGEX.RED.search(draw_data)) else 0,
        g=int(match.group(1)) if (match := REGEX.GREEN.search(draw_data)) else 0,
        b=int(match.group(1)) if (match := REGEX.BLUE.search(draw_data)) else 0,
    )


def parse_game(line: str) -> Game:
    header, draw_data = line.split(": ")
    game_id = int(header[5:])
    draw_list = [parse_draw(raw_draw) for raw_draw in draw_data.split(";")]

    return Game(game_id, draw_list)


parser = argparse.ArgumentParser(description="Solution for Advent of Code 2/2023.")
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
