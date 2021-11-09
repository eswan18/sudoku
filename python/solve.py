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
        next_puzzle = digit_elimination_update(current_puzzle)
        next_puzzle = square_elimination_update(next_puzzle)
        if next_puzzle.is_solved:
            return next_puzzle
        if next_puzzle == current_puzzle:
            raise RuntimeError("Deadend: couldn't solve puzzle")

def digit_elimination_update(puzzle: Puzzle) -> Puzzle:
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
    return puzzle

def square_elimination_update(puzzle: Puzzle) -> Puzzle:
    for digit in ALL_DIGITS:
        viable_locations = puzzle.spots_for(digit)
        print(f'found {len(viable_locations)} for digit {digit}')
        if len(viable_locations) == 1:
            print(f'found just one location for {digit}')
            viable_location, *_ = viable_locations
            new_puzzle = copy(puzzle)
            new_puzzle[viable_location] = digit
            return new_puzzle
    return puzzle
