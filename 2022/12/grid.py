from collections import defaultdict
from dataclasses import dataclass


class IntTuple(tuple):
    def __add__(self, other: tuple) -> "IntTuple":
        return IntTuple(int(s + o) for s, o in zip(self, other))

    def __sub__(self, other: tuple) -> "IntTuple":
        return IntTuple(int(s - o) for s, o in zip(self, other))


@dataclass
class Area:
    x: int
    y: int
    height: int

    @property
    def position(self) -> IntTuple[int, int]:
        return IntTuple((self.x, self.y))

    def __hash__(self):
        return hash(self.position)


class Grid:
    def __init__(self, rows: list[str]):
        self.height_map: dict[tuple, Area] = dict()
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                if char == "S":
                    self.start = (x, y)
                    height_char = "a"
                elif char == "E":
                    self.end = (x, y)
                    height_char = "z"
                else:
                    height_char = char
                self.height_map[IntTuple((x, y))] = Area(
                    x, y, self.get_height_from_char(height_char)
                )

    @staticmethod
    def get_height_from_char(ch: str) -> int:
        return ord(ch) - 97

    @property
    def start_area(self) -> Area:
        return self.height_map[self.start]

    @property
    def end_area(self) -> Area:
        return self.height_map[self.end]

    def heuristic(self, a: Area) -> int:
        s = self.start_area
        return abs(a.x - s.x) + abs(a.y - s.y)

    def get_accessible_neighbours(self, area: Area) -> list[Area]:
        pos = area.position
        h = area.height
        return list(
            filter(
                lambda a: a is not None and a.height <= h + 1,
                (
                    self.height_map.get(pos + (0, -1)),
                    self.height_map.get(pos + (1, 0)),
                    self.height_map.get(pos + (0, 1)),
                    self.height_map.get(pos + (-1, 0)),
                ),
            )
        )

    def find_best_path(self, from_: Area) -> list[Area]:
        start_area = from_
        end_area = self.end_area

        g_score = defaultdict(lambda: float("inf"))
        g_score[start_area] = 0

        f_score = defaultdict(lambda: float("inf"))
        f_score[start_area] = self.heuristic(start_area)

        came_from: dict[Area, Area] = dict()
        open_set = {start_area}

        while open_set:
            current = sorted(open_set, key=f_score.get)[0]
            if current == end_area:
                return self.reconstruct_path(came_from, current)
            open_set.remove(current)

            for neighbour in self.get_accessible_neighbours(current):
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + self.heuristic(current)
                    open_set.add(neighbour)

        return []

    @staticmethod
    def reconstruct_path(came_from: dict[Area, Area], current: Area) -> list[Area]:
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path
