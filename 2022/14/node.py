from dataclasses import dataclass


class IntTuple(tuple):
    def __add__(self, other: tuple) -> "IntTuple":
        return IntTuple(int(s + o) for s, o in zip(self, other))

    def __sub__(self, other: tuple) -> "IntTuple":
        return IntTuple(int(s - o) for s, o in zip(self, other))


@dataclass
class Node:
    x: int
    y: int

    @property
    def position(self) -> IntTuple[int, int]:
        return IntTuple((self.x, self.y))

    @position.setter
    def position(self, value: tuple[int, int]):
        x, y = value
        self.x = x
        self.y = y

    @classmethod
    def from_string(cls, node_info: str) -> "Node":
        return cls(*map(int, node_info.split(",")))

    def __hash__(self):
        return hash(self.position)
