from langchain_ollama import OllamaLLM
from arc_loader import eval_tasks, eval_tasks_small
from executor import run_program

llm = OllamaLLM(model="qwen3:30b")

def synthesize_program(task):
    prompt = f"""
    You are solving an ARC AGI task.
    Each grid is a 2D array of integers (0–9).
    
    Train examples:
    {task['train']}
    
    Write a Python function `solve(grid)` that
    transforms an input grid into the correct output.
    """
    return llm.invoke(prompt)

def main():
    
    for task in eval_tasks_small.values():
        program = synthesize_program(task)
        print(program)

    return "All done"

if __name__ == '__main__':
    main()
