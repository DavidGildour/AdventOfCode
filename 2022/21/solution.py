"""https://adventofcode.com/2022/day/21"""

from dataclasses import dataclass
from operator import add, sub, mul, floordiv
from typing import Union

op_dict = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": floordiv,
}
opposite_op = {"+": "-", "-": "+", "*": "/", "/": "*"}


class FlatValueMonkey:
    def __init__(self, value: str):
        if value.isnumeric():
            self.value = int(value)
        else:
            self.value = None
            m1, op, m2 = value.split()
            self.m1 = m1
            self.op = op_dict[op]
            self.m2 = m2


@dataclass
class ExpressionMonkey:
    left_hand: Union["ExpressionMonkey", str, int]
    operator_symbol: str
    right_hand: Union["ExpressionMonkey", str, int]

    def __str__(self) -> str:
        return f"({str(self.left_hand)} {self.operator_symbol} {str(self.right_hand)})"


def has_x(exp: ExpressionMonkey | int | str) -> bool:
    match exp:
        case str():
            return True
        case int():
            return False
        case _:
            return has_x(exp.left_hand) or has_x(exp.right_hand)


def evaluate(value: ExpressionMonkey | int) -> int:
    if isinstance(value, int):
        return value
    return op_dict[value.operator_symbol](
        evaluate(value.left_hand), evaluate(value.right_hand)
    )


def get_monkey_value(monkey_dict: dict[str, FlatValueMonkey], monkey_id: str) -> int:
    monkey = monkey_dict[monkey_id]
    if monkey.value is not None:
        return monkey.value
    return monkey.op(
        get_monkey_value(monkey_dict, monkey.m1),
        get_monkey_value(monkey_dict, monkey.m2),
    )


def monkey_expression(
    monkey_dict: dict[str, str], monkey_id: str
) -> ExpressionMonkey | int | str:
    if monkey_id == "humn":
        return "x"
    exp_str = monkey_dict[monkey_id]
    if exp_str.isnumeric():
        return int(exp_str)
    m1, op, m2 = exp_str.split()
    if monkey_id == "root":
        op = "="
    return ExpressionMonkey(
        monkey_expression(monkey_dict, m1), op, monkey_expression(monkey_dict, m2)
    )


def part_one(data: list[str]):
    monkey_dict = dict()
    for monkey_id, value in map(lambda m: m.split(": "), data):
        monkey_dict[monkey_id] = FlatValueMonkey(value)

    return get_monkey_value(monkey_dict, "root")


def part_two(data: list[str]):
    monkey_dict = dict()
    for monkey_id, value in map(lambda m: m.split(": "), data):
        monkey_dict[monkey_id] = value

    expression = monkey_expression(monkey_dict, "root")

    while not isinstance(expression.left_hand, str):
        left_hand = expression.left_hand
        right_hand = expression.right_hand
        operator = left_hand.operator_symbol
        opposite = opposite_op[operator]
        if has_x(left_hand.left_hand):
            expression.right_hand = ExpressionMonkey(
                right_hand, opposite, left_hand.right_hand
            )
            expression.left_hand = left_hand.left_hand
        else:
            if operator == "-":
                expression.right_hand = ExpressionMonkey(
                    left_hand.left_hand, "-", right_hand
                )
            elif operator == "/":
                expression.right_hand = ExpressionMonkey(
                    right_hand, "/", left_hand.left_hand
                )
            else:
                expression.right_hand = ExpressionMonkey(
                    right_hand, opposite, left_hand.left_hand
                )
            expression.left_hand = left_hand.right_hand
    return evaluate(expression.right_hand)


if __name__ == "__main__":
    with open("./input.txt") as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
