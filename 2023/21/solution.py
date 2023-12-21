"""https://adventofcode.com/2023/day/21"""
import argparse
from functools import reduce

type Position = tuple[int, int]


class Garden:
    def __init__(self, rows: list[str]):
        self.symbols = "".join(rows)
        self.width = len(rows)
        self.height = len(rows[0])
        self._start_index = self.symbols.index("S")

    @property
    def start_pos(self) -> Position:
        return self._to_position(self._start_index)

    def _to_symbol_index(self, x: int, y: int) -> int:
        return y * self.height + x

    def _to_position(self, i: int) -> Position:
        y, x = divmod(i, self.height)
        return x, y

    def get_plot_symbol(self, x: int, y: int) -> str | None:
        if self.position_is_valid(x, y):
            return self.symbols[self._to_symbol_index(x, y)]

    def position_is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _filter_criterion(self, pos: Position, visited_plots: set[Position]) -> bool:
        return pos not in visited_plots and self.get_plot_symbol(*pos) not in {
            None,
            "#",
        }

    def get_neighbours(
        self, position: Position, visited_plots: set[Position]
    ) -> set[Position]:
        x, y = position
        return set(
            filter(
                lambda pos: self._filter_criterion(pos, visited_plots),
                ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)),
            )
        )

    def reachable_plots(self, steps: int) -> int:
        step_oddness = self.oddness(steps)
        visited_plots = {self.start_pos}
        plot_steps = [(self.start_pos, 0)]

        last_visited = {self.start_pos}
        for step in range(1, steps + 1):
            if not last_visited:
                break
            last_visited = reduce(
                set.union,
                map(lambda x: self.get_neighbours(x, visited_plots), last_visited),
                set(),
            )

            plot_steps.extend((pos, step) for pos in last_visited)
            visited_plots |= last_visited

        print(f"Took {step} iteration.")

        reachable_plots = [
            pos for pos, step in plot_steps if self.oddness(step) == step_oddness
        ]
        print(self.debug_visited(reachable_plots))

        return len(reachable_plots)

    def debug_visited(self, plots: set[Position]):
        builder = []
        row = []
        for i, symbol in enumerate(self.symbols):
            if i > 0 and i % self.height == 0:
                builder.append("".join(row))
                row = []

            row.append("O" if self._to_position(i) in plots else symbol)

        return "\n".join([*builder, "".join(row)])

    @staticmethod
    def oddness(x: int) -> bool:
        return x % 2 == 0


def part_one(data: list[str]):
    garden = Garden(data)
    return garden.reachable_plots(64)


def part_two(data: list[str]):
    ...


parser = argparse.ArgumentParser(description="Solution for Advent of Code 21/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
