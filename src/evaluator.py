import numpy as np
from executor import run_program

def evaluate(task, program):
    for ex in task["test"]:
        pred = run_program(program, ex["input"])
        if pred is None: 
            # Create zero array with same shape as expected output
            pred = np.zeros_like(np.array(ex["output"]))
            return pred, False
        if np.array_equal(pred, np.array(ex["output"])):
            return pred, False
    return pred, True

