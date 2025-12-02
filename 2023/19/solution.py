"""https://adventofcode.com/2023/day/19"""

import argparse
from collections import defaultdict

from part import Part, PartRange
from workflow import Workflow


def parse_parts(part_strings: list[str]) -> list[Part]:
    return [Part.from_str(p) for p in part_strings]


def parse_workflows(workflow_strings: list[str]) -> dict[str, Workflow]:
    return {w.name: w for w in map(Workflow.from_str, workflow_strings)}


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
            workflow = workflows[workflow_name]

            intermediate_state = workflow.consider_ranges(ranges)
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
