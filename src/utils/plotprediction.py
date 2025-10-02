import matplotlib.pyplot as plt
from pathlib import Path

def plot_prediction(result, task, task_id):
    plt.figure(figsize=(15, 5))
        
    plt.subplot(1, 3, 1)
    plt.imshow(task[0]['input'], cmap='tab10')
    plt.title('Input')
    
    plt.subplot(1, 3, 2)
    plt.imshow(result, cmap='tab10')
    plt.title('Output')
    
    plt.subplot(1, 3, 3)
    plt.imshow(task[0]['output'], cmap='tab10')
    plt.title('Expected')
    
    plt.suptitle(f'Task {task_id}')
    plt.tight_layout()
    
    # Create visuals directory in output folder
    visuals_dir = Path(__file__).resolve().parent.parent.parent / 'output' / 'visuals'
    
    # Save figure
    fig_path = visuals_dir / f"{task_id.replace('.json', '.png')}"
    plt.savefig(fig_path, bbox_inches='tight', dpi=300)
    plt.close()  # Close the figure to free memory
        
    return
