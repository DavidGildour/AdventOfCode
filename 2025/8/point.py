from dataclasses import dataclass, field

import math


@dataclass
class Point:
    x: int
    y: int
    z: int
    circuit_id: int | None = None
    _distance_cache: dict[Point, float] = field(default_factory=dict, repr=False)

    @property
    def xyz(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z

    def distance_to(self, other: Point) -> float:
        if other in self._distance_cache:
            return self._distance_cache[other]

        dist = math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )
        self._distance_cache[other] = dist
        other._distance_cache[self] = dist
        return dist

    def __hash__(self):
        return hash(self.xyz)

    def __ge__(self, other: Point) -> bool:
        return self.xyz >= other.xyz

    def __gt__(self, other: Point) -> bool:
        return self.xyz > other.xyz

    def __lt__(self, other: Point) -> bool:
        return self.xyz < other.xyz
