from dataclasses import dataclass
from typing import Generator

from node import Node, IntTuple


class CavePath:
    def __init__(self, node_info: str):
        self.nodes = set()
        nodes = list(map(Node.from_string, node_info.split(" -> ")))
        for node1, node2 in zip(nodes, nodes[1:]):
            self.nodes.update(self.build_path(node1, node2))

    @staticmethod
    def build_path(n1: Node, n2: Node) -> set[Node]:
        if n1.x == n2.x:
            y_start, y_end = sorted([n1.y, n2.y])
            return {Node(n1.x, y) for y in range(y_start, y_end + 1)}
        elif n1.y == n2.y:
            x_start, x_end = sorted([n1.x, n2.x])
            return {Node(x, n1.y) for x in range(x_start, x_end + 1)}


class Cave:
    def __init__(self, path_info: list[str]):
        self.blocked_nodes = set()
        self.x_span = [500, 500]
        self.y_depth = 0
        for path in map(CavePath, path_info):
            self.blocked_nodes.update(path.nodes)
            self.widen(path)

    def widen(self, path: CavePath):
        path_x_span = [n.x for n in path.nodes]
        if (new_min_x := min(path_x_span)) < self.x_span[0]:
            self.x_span[0] = new_min_x
        if (new_max_x := max(path_x_span)) > self.x_span[1]:
            self.x_span[1] = new_max_x
        if (new_max_y := max(n.y for n in path.nodes)) > self.y_depth:
            self.y_depth = new_max_y

    def simulate_sand_dropping(self) -> Generator["Sand", None, None]:
        more_sand_to_go = True
        while more_sand_to_go:
            sand = Sand(500, 1)
            sand.simulate_dropping(self)
            if sand.is_resting:
                self.blocked_nodes.add(sand.to_node())
                yield sand
            else:
                more_sand_to_go = False

    def node_is_unblocked(self, node: Node | tuple[int, int]) -> bool:
        if not isinstance(node, Node):
            node = Node(*node)
        return node not in self.blocked_nodes

    def node_is_bound_for_endless_void(self, p: Node) -> bool:
        return p.x < self.x_span[0] or p.x > self.x_span[1] or p.y > self.y_depth

    def __str__(self) -> str:
        builder = []
        for y in range(self.y_depth + 1):
            row = ""
            for x in range(self.x_span[0], self.x_span[1] + 1):
                row += "#" if Node(x, y) in self.blocked_nodes else "."
            builder.append(row)
        return "\n".join(builder)


class CaveWithBottom(Cave):
    def __init__(self, path_info: list[str]):
        super().__init__(path_info)
        self.y_depth += 2

    def simulate_sand_dropping(self) -> Generator["Sand", None, None]:
        more_sand_to_go = True
        start_pos = IntTuple((500, 0))
        while more_sand_to_go:
            if Node(*start_pos) in self.blocked_nodes:
                more_sand_to_go = False
            else:
                sand = Sand(*start_pos)
                sand.simulate_dropping(self)
                self.add_sand(sand)
                yield sand

    def add_sand(self, sand: "Sand"):
        if sand.x < self.x_span[0]:
            self.x_span[0] = sand.x
        elif sand.x > self.x_span[1]:
            self.x_span[1] = sand.x
        self.blocked_nodes.add(sand.to_node())

    def node_is_unblocked(self, node: Node | tuple[int, int]) -> bool:
        if not isinstance(node, Node):
            node = Node(*node)
        return node not in self.blocked_nodes and node.y != self.y_depth

    def node_is_bound_for_endless_void(self, p: Node) -> bool:
        return False

    def __str__(self) -> str:
        builder = []
        for y in range(self.y_depth + 1):
            if y == self.y_depth:
                builder.append("#" * (self.x_span[1] - self.x_span[0]))
                continue
            row = ""
            for x in range(self.x_span[0], self.x_span[1] + 1):
                row += "#" if Node(x, y) in self.blocked_nodes else "."
            builder.append(row)
        return "\n".join(builder)


@dataclass
class Sand(Node):
    is_resting: bool = False

    def simulate_dropping(self, cave: Cave):
        while not self.is_resting:
            next_possible_positions = filter(
                cave.node_is_unblocked,
                [
                    self.position + (0, 1),
                    self.position + (-1, 1),
                    self.position + (1, 1),
                ],
            )
            try:
                next_position = next(next_possible_positions)
                if cave.node_is_bound_for_endless_void(Node(*next_position)):
                    break
                self.position = next_position
            except StopIteration:
                self.is_resting = True

    def to_node(self) -> Node:
        return Node(self.x, self.y)
