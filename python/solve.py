from copy import copy
from itertools import product
from collections import defaultdict

from puzzle import Puzzle

ALL_DIGITS = {str(i) for i in range(1, 10)}


def solve(input_puzzle: str) -> str:
    puzzle = Puzzle.from_string(input_puzzle)
    result = naive_solve(puzzle)
    print('One down!')
    return str(result)


def naive_solve(input_puzzle: Puzzle) -> Puzzle:
    current_puzzle = input_puzzle
    last_puzzle: Puzzle | None = None
    while True:
        print('Iterating solver')
        result = digit_elimination_update(current_puzzle) or square_elimination_update(current_puzzle)
        if result is None:
            raise RuntimeError("Deadend: couldn't solve puzzle")
        if result.is_solved:
            return result
        else:
            current_puzzle = result
        print('\n' + current_puzzle.pretty() + '\n')

def digit_elimination_update(puzzle: Puzzle) -> Puzzle | None:
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
                return new_puzzle
    return None

def square_elimination_update(puzzle: Puzzle) -> Puzzle | None:
    for digit in ALL_DIGITS:
        viable_locations = puzzle.spots_for(digit)
        by_row: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
        by_col: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
        by_grid: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
        for row, col in viable_locations:
            loc = row, col
            by_row[row].append(loc)
            by_col[col].append(loc)
            grid = Puzzle.grid_of_square(loc)
            by_grid[grid].append(loc)
        for dct in (by_row, by_col, by_grid):
            for key in dct:
                # This is the only place in the row/col/grid where this number can go.
                if len(dct[key]) == 1:
                    location, *_ = dct[key]
                    new_puzzle = copy(puzzle)
                    new_puzzle[location] = digit
                    return new_puzzle
    return None
