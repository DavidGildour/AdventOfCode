from dataclasses import dataclass, field


@dataclass
class Cave:
    name: str
    exits: list[str] = field(default_factory=list)

    @property
    def is_start(self) -> bool:
        return self.name == "start"

    @property
    def is_end(self) -> bool:
        return self.name == "end"

    @property
    def is_big(self) -> bool:
        return self.name.isupper()


@dataclass
class Route:
    caves: list[Cave] = field(default_factory=list)

    @property
    def bonus_traversal_available(self) -> bool:
        return all(self.caves.count(cave) == 1 for cave in self.caves if not cave.is_big)

    @property
    def length(self) -> int:
        return len(self.caves)

    @property
    def as_str(self):
        return ">".join(c.name for c in self.caves)

    @property
    def finished(self):
        return self.length > 0 and self.caves[-1].is_end

    def copy(self):
        return Route(caves=self.caves.copy())

    def add_cave(self, cave: Cave):
        self.caves.append(cave)
