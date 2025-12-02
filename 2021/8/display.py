from dataclasses import dataclass


@dataclass
class Display:
    unique_signals: set[str]
    output: list[str]

    @classmethod
    def from_raw_input(cls, inpt: str) -> "Display":
        unique, output = inpt.split("|")
        return cls(unique_signals=set(unique.split()), output=list(output.split()))
