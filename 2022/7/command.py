from dataclasses import dataclass, field


class CmdType:
    LS = "ls"
    CD = "cd"


@dataclass
class Command:
    type_: str
    argument: str | None
    output: list[str] = field(default_factory=list)
