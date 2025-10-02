import numpy as np
from executor import run_program

def evaluate(task, program):
    for ex in task["test"]:
        pred = run_program(program, ex["input"])
        if pred is None: 
            # Create zero array with same shape as expected output
            pred = np.zeros_like(np.array(ex["output"]))
            return pred, False
        
        try:
            # Ensure we have numpy arrays with consistent types
            pred_array = np.asarray(pred, dtype=int)
            expected_array = np.asarray(ex["output"], dtype=int)
            
            # Check if shapes match first
            if pred_array.shape != expected_array.shape:
                return pred_array, False
                
            # Use element-wise comparison and check if all elements are equal
            is_equal = (pred_array == expected_array).all()
            
            if is_equal:
                return pred_array, True
                
        except Exception as e:
            print(f"Error during evaluation: {str(e)}")
            return np.asarray(pred), False
            
    # If we get here, none of the test cases matched
    return np.asarray(pred), False

