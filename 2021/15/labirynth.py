from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int
    risk: int

    @property
    def coor(self):
        return self.x, self.y

    def distance_to(self, c: "Cell") -> int:
        return abs(self.x - c.x) + abs(self.y - c.y)

    def __hash__(self):
        return hash(self.coor)


class Labirynth:
    def __init__(self, risk_levels: list[list[Cell]]):
        self.grid = risk_levels
        self.width = len(risk_levels[0])
        self.height = len(risk_levels)
        self.exit = self.get(self.width - 1, self.height - 1)

    def get(self, x: int, y: int) -> Cell | None:
        if self.are_valid_coordinates(x, y):
            return self.grid[y][x]

    def __str__(self):
        return "\n".join("".join(str(cell.risk) for cell in row) for row in self.grid)

    def are_valid_coordinates(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbours(self, cell: Cell) -> list[Cell]:
        return list(filter(None, [
            self.get(cell.x,     cell.y - 1),
            self.get(cell.x - 1, cell.y),
            self.get(cell.x + 1, cell.y),
            self.get(cell.x,     cell.y + 1),
        ]))

    def heuristic(self, cell: Cell) -> int:
        return cell.risk + cell.distance_to(self.exit)

    def find_best_path(self):
        start_cell = self.get(0, 0)
        end_cell = self.exit

        g_score = defaultdict(lambda: float("inf"))
        g_score[start_cell] = 0

        f_score = defaultdict(lambda: float("inf"))
        f_score[start_cell] = self.heuristic(start_cell)

        came_from = dict()
        open_set = {start_cell}

        while open_set:
            current = sorted(open_set, key=f_score.get)[0]
            if current == end_cell:
                return self.reconstruct_path(came_from, current)
            open_set.remove(current)

            for neighbour in self.get_neighbours(current):
                tentative_g_score = g_score[current] + neighbour.risk
                if tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_g_score + current.distance_to(neighbour)
                    open_set.add(neighbour)

        return

    @staticmethod
    def reconstruct_path(came_from: dict[Cell, Cell], current: Cell) -> list[Cell]:
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path


def expand_grid(grid: list[str]) -> list[list[Cell]]:
    def wrap(r: int) -> int:
        return r - 9 if r > 9 else r

    result = []
    size = len(grid)
    for j in range(5):
        for y, row in enumerate(grid):
            cell_row = []
            for i in range(5):
                for x, risk in enumerate(row):
                    cell = Cell(x+(i*size), y+(j*size), wrap(int(risk) + i + j))
                    cell_row.append(cell)
            result.append(cell_row)

    return result
