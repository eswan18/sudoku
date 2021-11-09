from copy import copy
from collections.abc import Iterable

from typing import overload

class Puzzle:
    def __init__(self, rows: Iterable[Iterable[str]]):
        self._rows = list(list(x for x in row) for row in rows)

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

    def to_string(self) -> str:
        return ''.join(digit for row in self._rows for digit in row)

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        offset = len(cls_name) + 2
        rows_repr = '\n'.join(['    ' + repr(row) for row in self.rows])
        return f'{cls_name}([\n{rows_repr}\n])'

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
        elif isinstance(key, int):
            self._rows[key] = value
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
