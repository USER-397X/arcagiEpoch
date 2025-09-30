import numpy as np

def run_program(code, grid):
    local_env = {}
    
    try:
        exec(code, {}, local_env)  # don't expose globals
        solve = local_env["solve"]
        return solve(np.array(grid))
    
    except Exception as e:
        print("Error:", e)
        return None
