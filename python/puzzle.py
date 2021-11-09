from typing import overload

class Puzzle:
    def __init__(self, rows: list[list[str]]):
        self._rows = rows

    @classmethod
    def from_string(cls, s: str) -> 'Puzzle':
        if len(s) != 81:
            raise ValueError('input string must be 81 digits')
        digits = list(s)
        rows = [digits[n:n+9] for n in range(0, 81, 9)]
        return cls(rows)

    def to_string(self) -> str:
        return ''.join(digit for row in self._rows for digit in row)

    def __str__(self) -> str:
        return self.to_string()

    @property
    def rows(self):
        return tuple(tuple(row) for row in self._rows)

    @property
    def columns(self):
        return tuple(col for col in zip(*self.rows))

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
