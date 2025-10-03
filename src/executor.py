import numpy as np
import re

def run_program(code, grid):
    local_env = {'np': np}  # Make numpy available to the executed code

    try:
        exec(code, {}, local_env)  # don't expose globals
        
        # Try different possible function names in order of preference
        function_names = ['p', 'solve', 'transform', 'main']
        solve_func = None
        
        # First look for exact function definitions
        func_pattern = r'\bdef\s+(\w+)\s*\('
        defined_funcs = re.findall(func_pattern, code)
        
        # Try preferred names first, but only if they're actually defined as functions
        for name in function_names:
            if name in defined_funcs and name in local_env and callable(local_env[name]):
                solve_func = local_env[name]
                break
        
        # If no preferred names found, look for any defined function
        if solve_func is None:
            for name in defined_funcs:
                if name in local_env and callable(local_env[name]):
                    solve_func = local_env[name]
                    break
        
        if solve_func is None:
            raise NameError("No function definition found in the code")
            
        return solve_func(np.array(grid))

    except Exception as e:
        print("Error:", e)
        return None
