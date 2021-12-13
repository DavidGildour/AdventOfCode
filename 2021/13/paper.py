import re


class Paper:
    def __init__(self, dot_data: list[str]):
        self.dots = set(self.parse_dot(dot) for dot in dot_data)

    @property
    def width(self) -> int:
        return max(dot[0] for dot in self.dots) + 1

    @property
    def height(self) -> int:
        return max(dot[1] for dot in self.dots) + 1

    @property
    def surface(self):
        return [
            "".join("#" if (x, y) in self.dots else "." for x in range(self.width))
            for y in range(self.height)
        ]

    @property
    def dot_number(self) -> int:
        return len(self.dots)

    @staticmethod
    def parse_dot(dot: str) -> tuple[int, int]:
        x, y = map(int, dot.split(","))
        return x, y

    def fold(self, instruction: str):
        axis, line = re.match(r"^fold along ([xy])=(\d+)$", instruction).groups()
        line = int(line)
        if axis == "x":
            self.fold_left(line)
        elif axis == "y":
            self.fold_up(line)

    def fold_left(self, col: int):
        left = {dot for dot in self.dots if dot[0] < col}
        right = {(x - (x - col)*2, y) for x, y in self.dots if x > col}
        self.dots = left | right

    def fold_up(self, row: int):
        up = {dot for dot in self.dots if dot[1] < row}
        down = {(x, y - (y - row)*2) for x, y in self.dots if y > row}
        self.dots = up | down

    def __str__(self) -> str:
        return "\n".join(self.surface)
