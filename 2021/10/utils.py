from functools import reduce

OPEN_BRACES = ["(", "[", "{", "<"]
CLOSE_BRACES = [")", "]", "}", ">"]
ERROR_SCORES = [0, 3, 57, 1197, 25137]


def validate_braces(brace_line: str) -> int:
    stack = []
    for brace in brace_line:
        if brace in OPEN_BRACES:
            stack.append(brace)
        else:
            corresponding_brace = stack.pop()
            if OPEN_BRACES.index(corresponding_brace) != CLOSE_BRACES.index(brace):
                return CLOSE_BRACES.index(brace) + 1
    return 0


def complete_braces(incomplete_braces: str) -> str:
    stack = []
    for brace in incomplete_braces:
        if brace in OPEN_BRACES:
            stack.append(brace)
        else:
            stack.pop()

    return "".join(CLOSE_BRACES[OPEN_BRACES.index(brace)] for brace in reversed(stack))


def get_completion_score(completion_braces: str) -> int:
    return reduce(lambda a, b: a * 5 + CLOSE_BRACES.index(b) + 1, completion_braces, 0)


def get_middle_element(lst: list[int]) -> int:
    return sorted(lst)[len(lst) // 2]
