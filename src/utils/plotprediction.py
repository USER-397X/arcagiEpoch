import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path

def plot_prediction(task_filename, prediction):
    """
    Plot the ARC task including training examples, test input, model prediction, and actual output
    
    Args:
        task_filename (str): Name of the json file containing the task (e.g. '00576224.json')
        prediction (np.ndarray): Model's prediction output grid
    """
    # Load the task data
    task_path = Path('data') / 'evaluation' / task_filename
    with task_path.open('r') as f:
        task_data = json.load(f)
    
    # Get number of training examples
    n_train = len(task_data['train'])
    
    # Create figure with subplots for training examples and test case
    n_rows = max(2, (n_train + 1) // 2)  # At least 2 rows for test case
    fig = plt.figure(figsize=(15, 5 * n_rows))
    
    # Plot training examples
    for idx, train_example in enumerate(task_data['train']):
        # Input
        ax_in = fig.add_subplot(n_rows, 4, idx*2 + 1)
        ax_in.imshow(np.array(train_example['input']), cmap='tab10', vmin=0, vmax=9)
        ax_in.set_title(f'Train {idx+1} Input')
        ax_in.grid(True)
        
        # Output
        ax_out = plt.subplot(n_rows, 4, idx*2 + 2)
        ax_out.imshow(np.array(train_example['output']), cmap='tab10', vmin=0, vmax=9)
        ax_out.set_title(f'Train {idx+1} Output')
        ax_out.grid(True)
    
    # Plot test case in the last row
    test_row_start = ((n_train + 1) // 2) * 4 + 1
    
    # Test input
    ax_test_in = fig.add_subplot(n_rows, 4, test_row_start)
    test_input = np.array(task_data['test'][0]['input'])
    ax_test_in.imshow(test_input, cmap='tab10', vmin=0, vmax=9)
    ax_test_in.set_title('Test Input')
    ax_test_in.grid(True)
    
    # Model prediction
    ax_pred = fig.add_subplot(n_rows, 4, test_row_start + 1)
    ax_pred.imshow(prediction, cmap='tab10', vmin=0, vmax=9)
    ax_pred.set_title('Model Prediction')
    ax_pred.grid(True)
    
    # Actual test output
    ax_test_out = fig.add_subplot(n_rows, 4, test_row_start + 2)
    test_output = np.array(task_data['test'][0]['output'])
    ax_test_out.imshow(test_output, cmap='tab10', vmin=0, vmax=9)
    ax_test_out.set_title('Actual Output')
    ax_test_out.grid(True)
    
    # Add task ID as overall title
    plt.suptitle(f'Task {task_filename}', size=16)
    
    plt.tight_layout()
    plt.show()
