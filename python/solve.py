from copy import copy
from itertools import product

from puzzle import Puzzle

ALL_DIGITS = {str(i) for i in range(1, 10)}

def solve(input_puzzle: str) -> str:
    puzzle = Puzzle.from_string(input_puzzle)
    result = naive_solve(puzzle)
    print('One down!')
    return str(result)


def naive_solve(input_puzzle: Puzzle) -> Puzzle:
    current_puzzle = next_puzzle = input_puzzle
    while True:
        current_puzzle = next_puzzle
        next_puzzle = elimination_update(current_puzzle)
        if next_puzzle.is_solved:
            return next_puzzle
        if next_puzzle == current_puzzle:
            raise RuntimeError("Couldn't solve puzzle")

def elimination_update(puzzle: Puzzle) -> Puzzle:
    # Look at every position on the board until you find one that can only take one
    # value.
    for i, j in product(range(9), range(9)):
        if puzzle[i, j] == '0':
            used_digits = set(puzzle.rows[i]) | set(puzzle.columns[j])
            used_digits -= {'0'}
            if len(used_digits) == 8:
                print('used digits:', used_digits)
                missing_digit, *_ = list(ALL_DIGITS - used_digits)
                new_puzzle = copy(puzzle)
                new_puzzle[i, j] = missing_digit
                print(f'Updated [{i}, {j}] to be {missing_digit}]')
                print(repr(new_puzzle))
                return new_puzzle
    raise RuntimeError('Dead-end')
