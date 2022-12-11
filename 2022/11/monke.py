from dataclasses import dataclass
from typing import Callable


@dataclass
class Monke:
    items: list[int]
    operation: Callable[[int], int]
    divisor: int
    monkey_targets: tuple[int, int]
    inspection_count: int = 0

    def inspect_next_item(self):
        self.inspection_count += 1
        return self.items.pop(0)
