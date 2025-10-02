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
            # Convert both arrays to numpy arrays with explicit int dtype
            pred_array = np.asarray(pred, dtype=int)
            expected_array = np.asarray(ex["output"], dtype=int)
            print(pred_array)
            print(expected_array)


            # Check if shapes match first
            if pred_array.shape != expected_array.shape:
                print(f"Error: Output dimensions don't match. Expected shape {expected_array.shape}, but got {pred_array.shape}")
                return pred_array, False
                
            # Use element-wise comparison and check if all elements are equal
            is_equal = (pred_array == expected_array).all()
            
            if is_equal:
                return pred_array, True
                
        except Exception as e:
            print(f"Error: Failed to compare outputs - {str(e)}")
            return pred, False
            
    # If we get here, none of the test cases matched
    return pred, False

