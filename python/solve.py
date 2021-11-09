import sys
from collections.abc import Sequence
from typing import overload

def solve(input_puzzle: str):
    assert len(input_puzzle) == 81
    # Break the puzzle into a grid
    puzzle = Puzzle.from_string(input_puzzle)
    print(puzzle.rows)
    print(puzzle.columns)
    print(puzzle[0, 0])
    puzzle[1, 2] = '3'
    print(puzzle.rows)
    sys.exit(0)

class Puzzle:
    def __init__(self, rows: list[list[str]]):
        self._rows = rows

    @classmethod
    def from_string(cls, s: str) -> 'Puzzle':
        digits = list(s)
        rows = [digits[n:n+3] for n in range(0, 9, 3)]
        return cls(rows)

    @property
    def rows(self):
        return tuple(tuple(row) for row in self._rows)

    @property
    def columns(self):
        return tuple(col for col in zip(*self.rows))

    def __getitem__(self, key: int | tuple[int, int]) -> str | list[str]:
        if isinstance(key, tuple):
            if len(key) != 2:
                raise ValueError('slices must have length two')
            row, col = key
            return self._rows[row][col]
        elif isinstance(key, int):
            return self._rows[key]
        else:
            raise TypeError(f'unexpected key {key}')

    @overload
    def __setitem__(self, key: int, value: list[str]):
        ...

    @overload
    def __setitem__(self, key: tuple[int,int], value: str):
        ...

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            if len(key) != 2:
                raise ValueError('slices must have length two')
            row, col = key
            self._rows[row][col] = value
        elif isinstance(key, int):
            self._rows[key] = value
        else:
            raise TypeError(f'unexpected key {key}')
