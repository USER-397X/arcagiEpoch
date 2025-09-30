from arc_loader import eval_tasks_small
import numpy as np

task = 'fc754716.json'

test = eval_tasks_small[task]['test'][0]['input']

def solve(grid):
    val = 0
    for row in grid:
        for cell in row:
            if cell != 0:
                val = cell
    rows = len(grid)
    cols = len(grid[0])
    output = []
    for i in range(rows):
        new_row = []
        for j in range(cols):
            if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                new_row.append(val)
            else:
                new_row.append(0)
        output.append(new_row)
    output = np.array(output, dtype=int)
    return output

print(solve(np.array(test)))