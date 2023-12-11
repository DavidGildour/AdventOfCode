class Position(tuple):
    def __add__(self, other: "Position") -> "Position":
        return Position(s + o for s, o in zip(self, other))
