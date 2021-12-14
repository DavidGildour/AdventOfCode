from collections import Counter, defaultdict


def apply_insertions(polymer: str, rules: dict[str, str]):
    buffer = list(polymer)
    offset = 0
    for i in range(len(polymer) - 1):
        pair = polymer[i: i+2]
        insertion = rules.get(pair)
        if not insertion:
            continue

        buffer.insert(i + 1 + offset, insertion)
        offset += 1
    return "".join(buffer)


def count_pairs(polymer: str) -> tuple[defaultdict[str, int], defaultdict[str, int]]:
    p = defaultdict(int)
    e = defaultdict(int)
    for pair in zip(polymer, polymer[1:]):
        p["".join(pair)] += 1
        e[pair[0]] += 1
    e[polymer[-1]] += 1
    return p, e


def count_insertions(pair_count: defaultdict[str, int], element_count: defaultdict[str, int], rules: dict[str, str]):
    for pair, count in list(pair_count.items()):
        insertion = rules.get(pair)
        if not insertion:
            continue

        pair_count[pair[0] + insertion] += count
        pair_count[insertion + pair[1]] += count
        pair_count[pair] -= count
        element_count[insertion] += count


def part_one(initial_state: str, rules: list[str]) -> int:
    """The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has
    polymerization equipment that would produce suitable materials to reinforce the submarine, and the nearby
    volcanically-active caves should even have the necessary input elements in sufficient quantities.

    The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer
    template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result
    after repeating the pair insertion process a few times.

    For example:

    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C

    The first line is the polymer template - this is the starting point of the process.

    The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are
    immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.

    So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

        The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
        The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
        The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.

    Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all
    pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.

    After the first step of this process, the polymer becomes NCNBCHB.

    Here are the results of a few steps using the above rules:

    Template:     NNCB
    After step 1: NCNBCHB
    After step 2: NBCCNBBBCBHCB
    After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
    After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

    This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B occurs
    1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times; taking the quantity of the most common
    element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.

    Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. What
    do you get if you take the quantity of the most common element and subtract the quantity of the least common element?
    """
    parsed_rules = dict(map(lambda s: tuple(s.split(" -> ")), rules))
    polymer = initial_state
    for i in range(10):
        polymer = apply_insertions(polymer, parsed_rules)
    counts = list(c[1] for c in Counter(polymer).most_common())
    return counts[0] - counts[-1]


def part_two(initial_state: str, rules: list[str]) -> int:
    """The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more steps of the
    pair insertion process; a total of 40 steps should do it.

    In the above example, the most common element is B (occurring 2192039569602 times) and the least common element is H
    (occurring 3849876073 times); subtracting these produces 2188189693529.

    Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result.
    What do you get if you take the quantity of the most common element and subtract the quantity of the least common
    element?
    """
    parsed_rules = dict(map(lambda s: tuple(s.split(" -> ")), rules))
    pair_count, element_count = count_pairs(initial_state)
    for i in range(40):
        count_insertions(pair_count, element_count, parsed_rules)
    counts = sorted(element_count.values())
    return counts[-1] - counts[0]


if __name__ == '__main__':
    with open("./input.txt") as f:
        initial_polymer, _, *pair_insertions = [x.strip() for x in f.readlines()]

    difference = part_one(initial_polymer, pair_insertions)
    print(f"PART ONE: The difference between the most and least common "
          f"elements after 10 iterations is equal to {difference}.")
    difference = part_two(initial_polymer, pair_insertions)
    print(f"PART ONE: The difference between the most and least common "
          f"elements after 40 iterations is equal to {difference}.")
