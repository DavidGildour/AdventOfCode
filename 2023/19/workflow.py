import re
from collections import defaultdict
from dataclasses import dataclass

from part import Part, PartRange
from instruction import Instruction


WORKFLOW_REGEX = re.compile(r"(\w+){(.+),(\w+)}")


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
