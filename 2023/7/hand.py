from collections import Counter

from hand_value import HandValue


class Hand:
    CARD_VALUE_ORDER = "23456789TJQKA"

    def __init__(self, data: str):
        cards, bid = data.split(" ")
        self.cards = cards
        self.bid = int(bid)
        self.value = self.determine_hand_value(cards)

    @staticmethod
    def determine_hand_value(cards: str) -> HandValue:
        c = Counter(cards)
        match sorted(c.values(), reverse=True):
            case (5,):
                return HandValue.FIVE
            case (4, 1):
                return HandValue.FOUR
            case (3, 2):
                return HandValue.FHOUSE
            case (3, 1, 1):
                return HandValue.THREE
            case (2, 2, 1):
                return HandValue.TPAIR
            case (2, 1, 1, 1):
                return HandValue.PAIR
            case _:
                return HandValue.HCARD

    @classmethod
    def get_card_value(cls, c: str) -> int:
        return cls.CARD_VALUE_ORDER.index(c)

    def __str__(self):
        return f"{self.cards=} :: {self.bid=} :: {self.value=}"


class JokerHand(Hand):
    CARD_VALUE_ORDER = "J23456789TQKA"

    @classmethod
    def determine_hand_value(cls, cards: str) -> HandValue:
        if cards == "J" * 5:
            return HandValue.FIVE

        c = Counter(cards.replace("J", ""))
        card, _ = c.most_common(1).pop()

        return super().determine_hand_value(cards.replace("J", card))
