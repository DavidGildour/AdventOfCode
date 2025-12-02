import re
from operator import mul, add
from typing import Callable

from monke import Monke


class Parser:
    OP_DICT = {
        "*": mul,
        "+": add,
    }

    @staticmethod
    def parse_starting_items(s: str) -> list[int]:
        return [int(x) for x in re.findall(r"\d+", s)]

    @staticmethod
    def parse_operation(s: str) -> Callable[[int], int]:
        op_symbol, second_arg = re.match(
            r"Operation: new = old (.) (.+)", s.strip()
        ).groups()
        operator = Parser.OP_DICT[op_symbol]
        if second_arg.isnumeric():
            return lambda x: operator(x, int(second_arg))
        return lambda x: operator(x, x)

    @staticmethod
    def parse_test(test_description: list[str]) -> tuple[int, ...]:
        return tuple(int(x.split()[-1]) for x in test_description)

    @classmethod
    def parse_monke(cls, monke_description: list[str]) -> Monke:
        starting_items = cls.parse_starting_items(monke_description[0])
        operation = cls.parse_operation(monke_description[1])
        divisor, *monke_targets = cls.parse_test(monke_description[2:])

        return Monke(starting_items, operation, divisor, monke_targets[::-1])

    @classmethod
    def parse_input(cls, raw_input: list[str]) -> list[Monke]:
        return [
            cls.parse_monke(raw_input[i * 7 + 1 : (i + 1) * 7 - 1])
            for i in range(0, len(raw_input) // 7 + 1)
        ]
