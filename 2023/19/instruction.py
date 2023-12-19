import re
from collections import defaultdict
from dataclasses import dataclass
from operator import gt, lt

from part import PartRange, Part

INSTRUCTION_REGEX = re.compile(r"(\w)([<>])(\d+):(\w+)")
OP_DICT = {">": gt, "<": lt}


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
