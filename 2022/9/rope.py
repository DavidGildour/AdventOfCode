class Direction:
    RIGHT = "R"
    UP = "U"
    LEFT = "L"
    DOWN = "D"


class IntTuple(tuple):
    def __add__(self, other: tuple) -> "IntTuple":
        return IntTuple(int(s + o) for s, o in zip(self, other))

    def __sub__(self, other: tuple) -> "IntTuple":
        return IntTuple(int(s - o) for s, o in zip(self, other))


class Knot:
    def __init__(self, position: tuple[int, int]):
        self.position = IntTuple(position)
        self.move_history = {position}

    def move(self, direction: str):
        position_offset = {
            Direction.UP: (0, 1),
            Direction.RIGHT: (1, 0),
            Direction.DOWN: (0, -1),
            Direction.LEFT: (-1, 0),
        }[direction]

        self._move_by_offset(position_offset)

    def _move_by_offset(self, position_offset: tuple[int, int]):
        self.position += position_offset
        self.move_history.add(self.position)

    def follow(self, other: "Knot"):
        source, target = self.position, other.position
        position_offset = target - source
        match position_offset:
            case (x, 0):
                if abs(x) <= 1:
                    return
                self.move(Direction.RIGHT if x > 0 else Direction.LEFT)
            case (0, y):
                if abs(y) <= 1:
                    return
                self.move(Direction.UP if y > 0 else Direction.DOWN)
            case (x, y):
                if abs(x) <= 1 and abs(y) <= 1:
                    return
                position_offset = (x / abs(x), y / abs(y))
                self._move_by_offset(position_offset)