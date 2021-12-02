from dataclasses import dataclass


@dataclass
class Position:
    horizontal: int = 0
    depth: int = 0


@dataclass
class AimedPosition(Position):
    aim: int = 0


@dataclass
class Movement:
    direction: str
    value: int


Course = list[Movement]
