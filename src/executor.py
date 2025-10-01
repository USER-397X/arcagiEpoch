import numpy as np
from utils.cleanser import extract_code

def run_program(code, grid):
    local_env = {}
    
    try:
        code = extract_code(code)
        exec(code, {}, local_env)  # don't expose globals
        solve = local_env["solve"]
        return solve(np.array(grid))
    
    except Exception as e:
        print("Error:", e)
        return None