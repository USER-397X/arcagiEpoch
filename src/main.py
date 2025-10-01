from langchain_ollama import OllamaLLM
from pathlib import Path
import regex as re

from arc_loader import eval_tasks_small, eval_tasks
from executor import run_program
from utils.cleanser import extract_code



llm = OllamaLLM(
    model="qwen3:30B",
    num_predict=4096
)



def create_reasoning(task):
    prompt = f"""
    You are solving an ARC AGI task.
    Each grid is a 2D array of integers (0–9).
    Train examples:
    {task['train']}

    Write the logic on how to solve the task. It has to be a structured approach
    and it must be a step by step instruction which can be followed programatically 

    Make sure you are concise.
    """
    return llm.invoke(prompt)



def synthesize_program(reasoning_steps):
    prompt = f"""
    You are solving an ARC AGI task.
    Each grid is a 2D array of integers (0–9).
    The approach you need to take to solve the task has been layed out for you.
    
    Solution:
    {reasoning_steps}

    Write a Python function `solve(grid)` that
    transforms an input grid into the correct output.

    Respond with only a Python code block containing the function.
    Do not include explanations, math markup, or extra text. 
    """
    return llm.invoke(prompt)


def main():
    #Set output dir
    output_dir = Path(__file__).resolve().parent.parent / 'output'
    
    for id, task in eval_tasks.items():
        #Create reasoning steps
        plan = create_reasoning(task)

        # Save the plan in output/reasoning/id.txt
        output_path = output_dir / 'reasoning' / Path(id).with_suffix('.txt') 
        output_path.write_text(plan)
        print(f"Saved plan for task {id} to {output_path}")

        #Create program
        program_full = synthesize_program(plan)
        program = extract_code(program_full)

        #Save the program in output/programs/id.py
        output_path = output_dir / 'programs' / Path(id).with_suffix('.py') 
        output_path.write_text(program)
        print(f"Saved program for task {id} to {output_path}")

        # Run the program
        # output = run_program(program, task['test'][0]['input'])

    return



if __name__ == '__main__':
    main()
