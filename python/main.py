from solve import solve

DATA_FILE = '../data/sudoku.csv'
with open(DATA_FILE, 'r') as f:
    data = f.read()

header, *samples = data.split('\n')
test_cases = (line.split(',') for line in samples)
for puzzle, correct_solution in test_cases:
    solution = solve(puzzle)
    assert solution == correct_solution
