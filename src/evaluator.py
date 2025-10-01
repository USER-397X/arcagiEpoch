import numpy as np
from executor import run_program

def evaluate(task, program):
    for ex in task["train"]:
        pred = run_program(program, ex["input"])
        if pred is None or not np.array_equal(pred, np.array(ex["output"])):
            return False
    return True

