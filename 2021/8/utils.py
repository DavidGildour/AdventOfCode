from functools import reduce

LENGTH_TO_DIGIT = {2: 1, 3: 7, 4: 4, 7: 8}
DIGIT_TO_LENGTH = {1: 2, 4: 4, 7: 3, 8: 7}
DIGIT_MAP = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9",
}


def get_digits_with_unique_lengths(uniques: set[str]) -> list[str]:
    return [
        [x for x in uniques if len(x) == DIGIT_TO_LENGTH[i]].pop()
        if i in DIGIT_TO_LENGTH
        else ""
        for i in range(10)
    ]


def get_common_segments(*raw_digits: str) -> str:
    return "".join(reduce(set.intersection, map(set, raw_digits)))


def get_segment_difference(raw_digit1: str, raw_digit2: str) -> str:
    return "".join(set(raw_digit1) - set(raw_digit2))


def deduce_digit_two(
    uniques: set[str], digit_four: str, top_segment: str
) -> tuple[str, str, str]:
    candidates = [x for x in uniques if len(x) == 5]
    diffs = [
        get_segment_difference(candidate_235, digit_four)
        for candidate_235 in candidates
    ]
    bottom_segment = "".join(reduce(set.intersection, map(set, diffs)) - {top_segment})
    diffs = ["".join(diff - set(bottom_segment)) for diff in map(set, diffs)]
    bottom_left_segment = [
        "".join(set(diff) - {top_segment}) for diff in diffs if len(diff) == 2
    ].pop()
    number_two = [c for c in candidates if bottom_left_segment in c].pop()
    return number_two, bottom_segment, bottom_left_segment


def deduce_digit_three_and_five(
    uniques: set[str], digit_two: str, right_segments: str
) -> tuple[str, str, str, str]:
    candidates = [x for x in uniques if len(x) == 5 and x != digit_two]
    five, three = sorted(candidates, key=lambda x: len(set(x) & set(right_segments)))
    bottom_right_segment = get_common_segments(five, right_segments)
    top_right_segment = get_segment_difference(right_segments, bottom_right_segment)
    return three, five, top_right_segment, bottom_right_segment


def get_middle_segment(two: str, three: str, five: str, top: str, bottom: str) -> str:
    common = get_common_segments(two, three, five)
    return get_segment_difference(common, top + bottom)


def get_top_left_segment(wire_candidates: list[str]) -> str:
    return list(set("abcdefg") - set(wire_candidates)).pop()


def get_wire_mapping(uniques: set[str]) -> dict[str, str]:
    wire_candidates = [""] * 7
    decoded_digits = get_digits_with_unique_lengths(uniques)

    # get candidates for top right and top left segments
    right_segments = get_common_segments(decoded_digits[1], decoded_digits[7])
    wire_candidates[2] += right_segments
    wire_candidates[5] += right_segments

    # get the top segment
    wire_candidates[0] = get_segment_difference(decoded_digits[7], decoded_digits[1])

    # get digit 2, bottom segment and bottom left segment
    decoded_digits[2], wire_candidates[6], wire_candidates[4] = deduce_digit_two(
        uniques, decoded_digits[4], wire_candidates[0]
    )

    # get digits 3 and 5, top and bottom right segments
    decoded_digits[3], decoded_digits[5], wire_candidates[2], wire_candidates[5] = (
        deduce_digit_three_and_five(uniques, decoded_digits[2], wire_candidates[2])
    )

    wire_candidates[3] = get_middle_segment(
        decoded_digits[2],
        decoded_digits[3],
        decoded_digits[5],
        wire_candidates[0],
        wire_candidates[6],
    )

    wire_candidates[1] = get_top_left_segment(wire_candidates)

    return dict(zip(wire_candidates, "abcdefg"))


def parse_number(number: list[str], wire_mapping: dict[str, str]) -> int:
    builder = ""
    for digit in number:
        mapped_wires = "".join(wire_mapping[wire] for wire in digit)
        builder += DIGIT_MAP["".join(sorted(mapped_wires))]
    return int(builder)
