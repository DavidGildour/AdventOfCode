import re
from dataclasses import dataclass
from functools import reduce

PART_REGEX = re.compile(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")
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
