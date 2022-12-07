import re
from dataclasses import dataclass, field
from typing import Optional, Union

FILE_RE = re.compile(r"^(\d+) (.+)$")


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    parent: Optional["Directory"] = None
    children: dict[str, Union["Directory", File]] = field(default_factory=dict)
    _size: int | None = None

    def add_children(self, ls: list[str]):
        for line in ls:
            if m := re.match(FILE_RE, line):
                size, name = m.groups()
                self.children[name] = File(name, int(size))
            else:
                _, name = line.split()
                self.children[name] = Directory(name, self)

    @property
    def size(self) -> int:
        if self._size is None:
            size = 0
            for child in self.children.values():
                size += child.size
            self._size = size
        return self._size
