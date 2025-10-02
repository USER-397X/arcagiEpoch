from arc_loader import eval_tasks_small,train_tasks_small
from evaluator import evaluate

import numpy as np

task = '8be77c9e.json'

test_input = train_tasks_small[task]['test'][0]['input']
test_output = train_tasks_small[task]['test'][0]['output']

def p(grid: list[list[int]]) -> list[list[int]]:
    if not grid:
        return []
    R = len(grid)
    C = len(grid[0])
    output_grid = [[0 for _ in range(C)] for _ in range(2 * R)]
    for i in range(R):
        output_grid[i] = grid[i].copy()
    for j in range(R):
        output_grid[R + j] = grid[R - 1 - j].copy()
    return output_grid

pred = np.array(p(test_input))
print(pred)
print(np.array(test_output))
print(np.array_equal(np.array(pred), np.array(test_output)))