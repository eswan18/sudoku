import sys

from puzzle import Puzzle

def solve(input_puzzle: str) -> str:
    puzzle = Puzzle.from_string(input_puzzle)
    result = puzzle  # This ... needs more logic
    print('0' in puzzle)
    print('30' in puzzle)
    return str(result)

def naive_solve(input_puzzle: Puzzle) -> Puzzle:
    current_puzzle = input_puzzle
    next_puzzle = None
    while next_puzzle != current_puzzle:
        current_puzzle = next_puzzle
        next_puzzle = naive_update(current_puzzle)
    if '0' in current_puzzle:
        raise RuntimeError("Couldn't solve puzzle")
    else:
        return current_puzzle
