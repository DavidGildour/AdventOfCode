from enum import Enum


class RPS(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


beats = {RPS.ROCK: RPS.PAPER, RPS.PAPER: RPS.SCISSORS, RPS.SCISSORS: RPS.ROCK}
loses_to = {v: k for k, v in beats.items()}


def get_score(p1: RPS, p2: RPS) -> int:
    if p1 == beats[p2]:
        return Outcome.WIN.value + p1.value
    if p2 == beats[p1]:
        return Outcome.LOSE.value + p1.value
    return Outcome.DRAW.value + p1.value


def parse_outcome(code: str) -> Outcome:
    return {"X": Outcome.LOSE, "Y": Outcome.DRAW, "Z": Outcome.WIN}[code]


def parse_move(code: str) -> RPS:
    if code in "AX":
        return RPS.ROCK
    if code in "BY":
        return RPS.PAPER
    if code in "CZ":
        return RPS.SCISSORS


def get_right_move(enemy: RPS, outcome: Outcome) -> RPS:
    if outcome == Outcome.LOSE:
        return loses_to[enemy]
    if outcome == Outcome.WIN:
        return beats[enemy]
    return enemy


def part_one(data: list[str]) -> int:
    """The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage,
    a giant Rock Paper Scissors tournament is already in progress.

    Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each
    simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected:
    Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape,
    the round instead ends in a draw.

    Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say
    will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper,
    and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

    The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for
    Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

    The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores
    for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper,
    and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw,
    and 6 if you won).

    Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get
    if you were to follow the strategy guide.

    For example, suppose you were given the following strategy guide:

    A Y
    B X
    C Z

    This strategy guide predicts and recommends the following:

        In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for
        you with a score of 8 (2 because you chose Paper + 6 because you won). In the second round, your opponent will
        choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0). The
        third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.

    In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

    What would your total score be if everything goes exactly according to your strategy guide?"""
    return sum(
        get_score(myself, enemy)
        for enemy, myself in map(
            lambda x: (parse_move(x[0]), parse_move(x[1])), map(str.split, data)
        )
    )


def part_two(data: list[str]) -> int:
    """The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the
    round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need
    to win. Good luck!"

    The total score is still calculated in the same way, but now you need to figure out what shape to choose so the
    round ends as indicated. The example above now goes like this:

        In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also
        choose Rock. This gives you a score of 1 + 3 = 4. In the second round, your opponent will choose Paper (B),
        and you choose Rock, so you lose (X) with a score of 1 + 0 = 1. In the third round, you will defeat your
        opponent's Scissors with Rock for a score of 1 + 6 = 7.

    Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

    Following the Elf's instructions for the second column, what would your total score be if everything goes exactly
    according to your strategy guide?"""
    return sum(
        get_score(get_right_move(enemy, outcome), enemy)
        for enemy, outcome in map(
            lambda x: (parse_move(x[0]), parse_outcome(x[1])), map(str.split, data)
        )
    )


if __name__ == "__main__":
    with open("./input.txt") as f:
        raw_data = [x.strip() for x in f.readlines()]

    first_answer = part_one(raw_data)
    print(f"PART ONE: The answer to part one is equal to {first_answer}.")
    second_answer = part_two(raw_data)
    print(f"PART ONE: The answer to part two is equal to {second_answer}.")
