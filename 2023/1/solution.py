"""https://adventofcode.com/2023/day/1"""
import argparse
import re

DIGITS_WORDS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
WORD_TO_DIGIT: dict[str, str] = dict(
    zip(
        DIGITS_WORDS,
        map(str, range(1, 10)),
    )
)
DIGIT_REGEX = re.compile("|".join(DIGITS_WORDS))


def extract_first_and_last_digit(line: str) -> int:
    digits = [ch for ch in line if ch.isdigit()]
    return int(digits[0] + digits[-1])


def has_a_digit_word(string: str, parse_reversed: bool = False) -> str | None:
    match = DIGIT_REGEX.search(string[::-1] if parse_reversed else string)
    return match[0] if match else None


def consider_next_character(
        buffer: str, next_char: str, parse_reversed: bool = False
) -> tuple[str, bool]:
    if next_char.isdigit():
        return next_char, True
    elif digit_word := has_a_digit_word(
            next_buffer := buffer + next_char, parse_reversed
    ):
        return WORD_TO_DIGIT[digit_word], True
    else:
        return next_buffer, False


def extract_real_first_and_last_digit(line: str) -> int:
    front_digit, back_digit = "", ""
    front_done, back_done = False, False

    for f_ch, b_ch in zip(line, line[::-1]):
        if not front_done:
            front_digit, front_done = consider_next_character(front_digit, f_ch)

        if not back_done:
            back_digit, back_done = consider_next_character(
                back_digit, b_ch, parse_reversed=True
            )

        if front_done and back_done:
            return int(front_digit + back_digit)


def part_one(lines: list[str]):
    return sum(map(extract_first_and_last_digit, lines))


def part_two(lines: list[str]):
    return sum(map(extract_real_first_and_last_digit, lines))


parser = argparse.ArgumentParser(description="Solution for Advent of Code 1/2023.")
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
