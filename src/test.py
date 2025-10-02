from arc_loader import eval_tasks_small
from evaluator import evaluate

import numpy as np

task = 'fc754716.json'

test_input = eval_tasks_small[task]['test'][0]['input']
test_output = eval_tasks_small[task]['test'][0]['output']

def p(grid: list[list[int]]) -> list[list[int]]:
    if not grid:
        return []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    seed_value = None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0:
                seed_value = grid[i][j]
                break
        if seed_value is not None:
            break
    if seed_value is None:
        return [row[:] for row in grid]
    output = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                output[i][j] = seed_value
    return output

pred = np.array(p(test_input))
print(pred)
print(np.array_equal(np.array(pred), np.array(test_output)))