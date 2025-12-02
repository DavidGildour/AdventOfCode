class BingoBoard:
    def __init__(self, number_matrix: list[list[int]]):
        self.numbers = number_matrix
        self.index_dict = self.get_index_dict()
        self.mark_mask = self.get_empty_mask()

    def get_index_dict(self) -> dict[int, tuple[int, int]]:
        """Creates a dictionary with values of the numbers on the board as keys and their (x, y) indices as values to
        mitigate the need to iterate over the numbers array every time we want to check if the number is there."""
        return {
            cell: (x, y)
            for y, row in enumerate(self.numbers)
            for x, cell in enumerate(row)
        }

    @staticmethod
    def get_empty_mask() -> list[list[bool]]:
        return [
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
        ]

    def reset(self):
        self.mark_mask = self.get_empty_mask()

    def mark_number(self, number: int):
        if number in self.index_dict:
            x, y = self.index_dict[number]
            self.mark_mask[y][x] = True

    def get_score(self) -> int:
        score = 0
        for row in self.numbers:
            for num in row:
                x, y = self.index_dict[num]
                score += num * (not self.mark_mask[y][x])
        return score

    def is_winning(self) -> bool:
        return self.check_horizontal() or self.check_vertical()

    def check_horizontal(self) -> bool:
        return any(sum(row) == 5 for row in self.mark_mask)

    def check_vertical(self) -> bool:
        return any(sum(col) == 5 for col in zip(*self.mark_mask))

    def __str__(self):
        builder = "\n"
        for row in self.numbers:
            for num in row:
                x, y = self.index_dict[num]
                if self.mark_mask[y][x]:
                    builder += f"[{num:2d}]"
                else:
                    builder += f"{num:^4}"
            builder += "\n"
        return builder
