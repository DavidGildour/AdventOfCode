from dataclasses import dataclass
from functools import reduce
from itertools import chain
from operator import mul
from typing import Sequence


class IntTuple(tuple):
    def __add__(self, other: "IntTuple") -> "IntTuple":
        return IntTuple(s + o for s, o in zip(self, other))


@dataclass
class Tree:
    height: int
    position: IntTuple[int, int]

    def __hash__(self):
        return hash(self.position)


Trees = Sequence[Sequence[Tree]]


class Forest:
    def __init__(self, trees: Trees):
        self.trees = trees
        self.tree_dict = {t.position: t for t in chain(*trees)}

    @classmethod
    def from_strings(cls, tree_lines: list[str]) -> "Forest":
        return cls(
            [
                [Tree(int(h), IntTuple((x, y))) for x, h in enumerate(line)]
                for y, line in enumerate(tree_lines)
            ]
        )

    def get_next_tree(self, tree: Tree, direction: str) -> Tree | None:
        return {
            "n": self.tree_dict.get(tree.position + IntTuple((0, -1))),
            "e": self.tree_dict.get(tree.position + IntTuple((1, 0))),
            "w": self.tree_dict.get(tree.position + IntTuple((-1, 0))),
            "s": self.tree_dict.get(tree.position + IntTuple((0, 1))),
        }[direction]

    def get_score_in_direction(self, tree: Tree, direction: str) -> int:
        sub_score = 0
        current_tree = tree
        while current_tree:
            next_tree = self.get_next_tree(current_tree, direction)
            if next_tree is not None:
                sub_score += 1
                if next_tree.height >= tree.height:
                    break
            current_tree = next_tree
        return sub_score

    def get_scenic_score(self, tree: Tree) -> int:
        return reduce(mul, (self.get_score_in_direction(tree, d) for d in "news"))

    def from_west(self) -> Trees:
        return self.trees

    def from_north(self):
        return zip(*self.trees)

    def from_east(self):
        return map(reversed, self.trees)

    def from_south(self):
        return map(reversed, self.from_north())
