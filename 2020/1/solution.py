from itertools import combinations


def part_one(values: list[int]) -> tuple[int, int]:
    """
    Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently,
    something isn't quite adding up.

    Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

    For example, suppose your expense report contained the following:

    1721
    979
    366
    299
    675
    1456

    In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces
    1721 * 299 = 514579, so the correct answer is 514579.

    Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you
    multiply them together?
    """
    value_set = set(sorted(values))

    for value in value_set:
        rest = 2020 - value
        if rest in value_set:
            return value, rest


def part_two(values: list[int]) -> tuple[int, int, int]:
    """
    The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over
    from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the
    same criteria.

    Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together
    produces the answer, 241861950.

    In your expense report, what is the product of the three entries that sum to 2020?
    """
    for _v1, _v2, _v3 in combinations(values, 3):
        if _v1 + _v2 + _v3 == 2020:
            return _v1, _v2, _v3


if __name__ == "__main__":
    with open("./input.txt") as f:
        values_list = [int(x.strip()) for x in f.readlines()]

    v1, v2 = part_one(values_list)
    print(f"PART ONE: {v1} * {v2} = {v1*v2}")

    v1, v2, v3 = part_two(values_list)
    print(f"PART TWO: {v1} * {v2} * {v3} = {v1*v2*v3}")
