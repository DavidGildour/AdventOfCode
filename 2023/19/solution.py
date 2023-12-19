"""https://adventofcode.com/2023/day/19"""
import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import gt, lt
from pprint import pprint
from typing import Mapping

PART_REGEX = re.compile(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")
WORKFLOW_REGEX = re.compile(r"(\w+){(.+),(\w+)}")
INSTRUCTION_REGEX = re.compile(r"(\w)([<>])(\d+):(\w+)")

OP_DICT = {">": gt, "<": lt}

type ValueRange = tuple[int, int]


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def sum_up(self) -> int:
        return self.x + self.m + self.a + self.s

    @classmethod
    def from_str(cls, part_str: str) -> "Part":
        return cls(*map(int, PART_REGEX.match(part_str).groups()))


@dataclass
class PartRange:
    x: ValueRange
    m: ValueRange
    a: ValueRange
    s: ValueRange

    def with_updates(self, attribute: str, value_range: ValueRange) -> "PartRange":
        return PartRange(**{**self.__dict__, attribute: value_range})

    def get_range_spans(self) -> tuple[int, int, int, int]:
        return (
            max(0, self.x[1] - self.x[0]),
            max(0, self.m[1] - self.m[0]),
            max(0, self.a[1] - self.a[0]),
            max(0, self.s[1] - self.s[0]),
        )

    def get_possible_parts(self) -> int:
        return reduce(lambda x, y: x * y, self.get_range_spans(), 1)

    @classmethod
    def from_str(cls, part_str: str) -> "PartRange":
        return cls(*map(int, PART_REGEX.match(part_str).groups()))


@dataclass
class Workflow:
    name: str
    instructions: list["Instruction"]
    fallback: str

    def consider(self, part: Part) -> str:
        for instruction in self.instructions:
            passes_test, result_label = instruction(part)
            if passes_test:
                return result_label

        return self.fallback

    def consider_ranges(self, part_ranges: list[PartRange]) -> dict[str, PartRange]:
        output_ranges = defaultdict(list)
        considered_ranges = part_ranges
        for instruction in self.instructions:
            passing_ranges, rest = instruction.consider_ranges(considered_ranges)
            considered_ranges = rest
            for result_name, result_ranges in passing_ranges.items():
                output_ranges[result_name] += result_ranges

        output_ranges[self.fallback] += considered_ranges

        return output_ranges

    @classmethod
    def from_str(cls, workflow_str: str) -> "Workflow":
        name, instruction_strs, fallback = WORKFLOW_REGEX.match(workflow_str).groups()
        instructions = list(map(Instruction.from_str, instruction_strs.split(",")))
        return cls(name, instructions, fallback)


@dataclass
class Instruction:
    attribute: str
    op_symbol: str
    value: int
    result: str

    def consider_ranges(
        self, part_ranges: list[PartRange]
    ) -> tuple[dict[str, list[PartRange]], list[PartRange]]:
        output_passed = defaultdict(list)
        output_rest = []

        for part_range in part_ranges:
            input_range = part_range.__getattribute__(self.attribute)
            if self.op_symbol == ">":
                passing_range = start, end = (self.value + 1, input_range[1])
                rest = (input_range[0], self.value + 1)
            else:
                passing_range = start, end = (input_range[0], self.value)
                rest = (self.value, input_range[1])

            if start < end:
                output_passed[self.result].append(
                    part_range.with_updates(self.attribute, passing_range)
                )
                output_rest.append(part_range.with_updates(self.attribute, rest))
            else:
                output_rest.append(part_range)

        return output_passed, output_rest

    @classmethod
    def from_str(cls, instruction_str: str) -> "Instruction":
        attribute, op, value, result = INSTRUCTION_REGEX.match(instruction_str).groups()

        return cls(attribute, op, int(value), result)

    def __call__(self, p: Part) -> tuple[bool, str]:
        test_attr = p.__getattribute__(self.attribute)
        return OP_DICT[self.op_symbol](test_attr, self.value), self.result


def parse_parts(part_strings: list[str]) -> list[Part]:
    return [Part.from_str(p) for p in part_strings]


def parse_workflows(workflow_strings: list[str]) -> dict[str, Workflow]:
    return {w.name: w for w in map(Workflow.from_str, workflow_strings)}


def parse_instruction(instruction_string: str) -> Instruction:
    attribute, op, value, result = INSTRUCTION_REGEX.match(instruction_string).groups()

    def _instruction(p: Part) -> tuple[bool, str]:
        test_attr = p.__getattribute__(attribute)
        return OP_DICT[op](test_attr, int(value)), result

    return _instruction


def is_accepted(part: Part, workflows: dict[str, Workflow]) -> bool:
    result = "in"
    while result not in {"A", "R"}:
        workflow = workflows[result]
        result = workflow.consider(part)

    return result == "A"


def process_parts(
    parts: list[Part], workflows: dict[str, Workflow]
) -> tuple[list[Part], list[Part]]:
    accepted, rejected = [], []
    for part in parts:
        if is_accepted(part, workflows):
            accepted.append(part)
        else:
            rejected.append(part)

    return accepted, rejected


def join_states(
    state1: dict[str, list[PartRange]], state2: dict[str, list[PartRange]]
) -> dict[str, list[PartRange]]:
    return defaultdict(
        list, {k: state1[k] + state2[k] for k in set(state1) | set(state2)}
    )


def part_one(workflow_data: list[str], part_data: list[str]) -> int:
    parts = parse_parts(part_data)
    workflows = parse_workflows(workflow_data)

    accepted, rejected = process_parts(parts, workflows)
    return sum(map(Part.sum_up, accepted))


def part_two(workflow_data: list[str]) -> int:
    workflows = parse_workflows(workflow_data)
    state = {"in": [PartRange((1, 4001), (1, 4001), (1, 4001), (1, 4001))]}
    accepted, rejected = [], []
    while state:
        new_state = defaultdict(list)
        for workflow_name in state:
            ranges = state[workflow_name]
            # print(f"{workflow_name}: {sum(pr.get_possible_parts() for pr in ranges):,}")
            # print(ranges)
            workflow = workflows[workflow_name]

            intermediate_state = workflow.consider_ranges(ranges)
            # pprint(dict(**intermediate_state))
            new_state = join_states(new_state, intermediate_state)

        accepted += new_state["A"]
        rejected += new_state["R"]
        del new_state["A"], new_state["R"]
        state = new_state

    return sum(pr.get_possible_parts() for pr in accepted)


parser = argparse.ArgumentParser(description="Solution for Advent of Code 19/2023.")
parser.add_argument("-t", "--test", action="store_true", help="use test input")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = "./input_test.txt" if args.test else "./input.txt"

    with open(filename) as f:
        raw_data = f.read().split("\n\n")
        raw_workflows, raw_parts = map(lambda x: x.strip().split("\n"), raw_data)

    first_answer = part_one(raw_workflows, raw_parts)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_workflows)
    print(f"PART TWO: The answer to part two is equal to {second_answer}.")
