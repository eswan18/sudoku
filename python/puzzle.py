from copy import copy
from array import array
from collections.abc import Iterable
from itertools import product

from typing import overload, Generator

class Puzzle:
    def __init__(self, rows: Iterable[Iterable[str]]):
        self._rows = list(list(x for x in row) for row in rows)
        self._flat = tuple(x for row in rows for x in row)

    @classmethod
    def from_string(cls, s: str) -> 'Puzzle':
        if len(s) != 81:
            raise ValueError('input string must be 81 digits')
        digits = list(s)
        rows = [digits[n:n+9] for n in range(0, 81, 9)]
        return cls(rows)

    @property
    def is_solved(self):
        return '0' not in self

    @property
    def rows(self):
        return tuple(tuple(row) for row in self._rows)

    @property
    def columns(self):
        return tuple(col for col in zip(*self.rows))

    @property
    def occupied_squares(self) -> Generator[tuple[int, int], None, None]:
        return (
            (idx // 9, idx % 9)
            for idx, val in enumerate(self._flat)
            if val != '0'
        )

    def to_string(self) -> str:
        return ''.join(digit for row in self._rows for digit in row)

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        offset = len(cls_name) + 2
        rows_repr = '\n'.join(['    ' + repr(row) for row in self.rows])
        return f'{cls_name}([\n{rows_repr}\n])'

    def pretty(self) -> str:
        lines = []
        for idx, row in enumerate(self._rows):
            if idx in (3, 6):
                lines.append('-' * 5 + '|' + '-' * 5 + '|' + '-' * 5)
            lines.append(f' {"".join(row[:3])} | {"".join(row[3:6])} | {"".join(row[6:])} ')
        return '\n'.join(lines)


    @overload
    def __getitem__(self, key: int) -> list[str]:
        ...

    @overload
    def __getitem__(self, key: tuple[int,int]) -> str:
        ...

    def __getitem__(self, key):
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
            self._flat = tuple(x for row in self._rows for x in row)
        elif isinstance(key, int):
            self._rows[key] = value
            self._flat = tuple(x for row in self._rows for x in row)
        else:
            raise TypeError(f'unexpected key {key}')

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return all(
            self_row == other_row
            for (self_row, other_row) in zip(self.rows, other.rows)
        )

    def __contains__(self, value: str) -> bool:
        return any(value in row for row in self._rows)

    def __copy__(self) -> 'Puzzle':
        cls = self.__class__
        return cls(copy(row) for row in self._rows)

    def spots_for(self, digit) -> set[tuple[int, int]]:
        locations = self.locations_of(digit)
        rows, columns = zip(*locations)
        remaining_rows = set(range(9)) - set(rows)
        remaining_cols = set(range(9)) - set(columns)
        viable_squares = set(product(remaining_rows, remaining_cols))
        viable_squares -= set(self.occupied_squares)
        return viable_squares

    def locations_of(self, digit) -> list[tuple[int, int]]:
        locations: list[tuple[int, int]] = []
        for row_idx, row in enumerate(self._rows):
            if digit in row:
                locations.append((row_idx, row.index(digit)))
        return locations

    @staticmethod
    def grid_of_square(location: tuple[int, int]) -> int:
        row, col = location
        grid_row = row // 3
        grid_col = col // 3
        return grid_row * 3 + grid_col
