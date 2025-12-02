from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Type

from position import Position


@dataclass
class Cell(ABC):
    position: Position

    @classmethod
    def from_symbol(cls, symbol: str, x: int, y: int) -> Type["Cell"]:
        return {
            "S": Start,
            ".": Ground,
            "|": PipeNS,
            "-": PipeWE,
            "L": PipeNE,
            "J": PipeNW,
            "7": PipeSW,
            "F": PipeSE,
        }[symbol](Position((x, y)))

    @abstractmethod
    def get_positions_of_connected_cells(self) -> tuple[Position, ...]: ...


class Start(Cell):
    def get_positions_of_connected_cells(self) -> tuple[Position, ...]:
        return (
            self.position + Position((-1, 0)),  # WEST
            self.position + Position((1, 0)),  # EAST
            self.position + Position((0, -1)),  # NORTH
            self.position + Position((0, 1)),  # SOUTH
        )


class Ground(Cell):
    def get_positions_of_connected_cells(self) -> tuple[Position, ...]:
        return tuple()


class PipeNS(Cell):
    def get_positions_of_connected_cells(self) -> tuple[Position, ...]:
        return (
            self.position + Position((0, -1)),  # NORTH
            self.position + Position((0, 1)),  # SOUTH
        )


class PipeWE(Cell):
    def get_positions_of_connected_cells(self) -> tuple[Position, ...]:
        return (
            self.position + Position((-1, 0)),  # WEST
            self.position + Position((1, 0)),  # EAST
        )


class PipeNE(Cell):
    def get_positions_of_connected_cells(self) -> tuple[Position, ...]:
        return (
            self.position + Position((1, 0)),  # EAST
            self.position + Position((0, -1)),  # NORTH
        )


class PipeNW(Cell):
    def get_positions_of_connected_cells(self) -> tuple[Position, ...]:
        return (
            self.position + Position((-1, 0)),  # WEST
            self.position + Position((0, -1)),  # NORTH
        )


class PipeSW(Cell):
    def get_positions_of_connected_cells(self) -> tuple[Position, ...]:
        return (
            self.position + Position((-1, 0)),  # WEST
            self.position + Position((0, 1)),  # SOUTH
        )


class PipeSE(Cell):
    def get_positions_of_connected_cells(self) -> tuple[Position, ...]:
        return (
            self.position + Position((1, 0)),  # EAST
            self.position + Position((0, 1)),  # SOUTH
        )
