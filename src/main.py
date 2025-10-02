from langchain_ollama import OllamaLLM
from pathlib import Path

from arc_loader import train_tasks, eval_tasks
from evaluator import evaluate

from utils.cleanser import extract_code, extract_reasoning, extract_function_def, remove_think
from utils.plotprediction import plot_prediction



llm = OllamaLLM(
    model="qwen3:30B",
    num_predict= 4096
)

llm_code = OllamaLLM(
    model="qwen3-coder:latest",
    temperature = 0.1,
    num_predict = 1024
)



def create_reasoning(task):
    prompt = f"""
    You are an expert algorithm designer specializing in grid-based puzzles. Your task is to analyze pairs of input/output grids and deduce the transformation rule. 
    
    Based on the provided training examples, describe the transformation as a precise, step-by-step algorithm that can be implemented in Python. 
    
    Focus on grid properties, object shapes, colors, and movements. Your description should be unambiguous and detailed enough for a programmer to follow. 
    
    For example, instead of 'move the shape', specify 'find the largest contiguous object of color blue (2) and shift all its pixels down by 3 rows'.
            
    "CRITICAL: Enclose your final algorithmic description ONLY within <reasoning>...</reasoning> tags. Do not add any other text, greetings, or explanations outside these tags."
    
    f"TASK EXAMPLES:\n{task['train']}
    """

    return llm.invoke(prompt)



def synthesize_program(reasoning_steps):
    prompt = f"""
    You are a robotic, highly-disciplined Python code writer. You will be given a set of REASONING steps. 
            Your one and only job is to translate these steps into a single, complete Python function named `p`. 
            The function must adhere strictly to the signature `def p(grid: list[list[int]]) -> list[list[int]]:`.
            Your output must be **only the code**. Do not write any explanations, comments, markdown, or any text whatsoever. 
            Your response must begin with `def p` and nothing else. The function body must be fully implemented, not a placeholder.
            --- PERFECT EXAMPLE ---
            REASONING:
            1. Get the dimensions of the input grid (height and width).
            2. Create a new grid of the same dimensions, filled with zeros.
            3. Iterate through each cell (r, c) of the input grid.
            4. If the cell's value is 2 (blue), place a 4 (red) at the corresponding location in the new grid.
            5. Otherwise, copy the original cell's value to the new grid.
            6. Return the new grid.
            def p(grid: list[list[int]]) -> list[list[int]]:
                height = len(grid)
                width = len(grid[0])
                new_grid = [[0 for _ in range(width)] for _ in range(height)]
                for r in range(height):
                    for c in range(width):
                        if grid[r][c] == 2:
                            new_grid[r][c] = 4
                        else:
                            new_grid[r][c] = grid[r][c]
                return new_grid
            --- END OF EXAMPLE ---
            --- YOUR TASK ---
            REASONING
            {reasoning_steps}
            "CODE:"
    """
    return llm.invoke(prompt)


def main():
    #Set output dir
    output_dir = Path(__file__).resolve().parent.parent / 'output'

    for id, task in eval_tasks.items():
        print(f"Working on {id}")
        
        #Create reasoning steps
        plan = create_reasoning(task)
        plan = extract_reasoning(plan)

        # Save the plan in output/reasoning/id.txt
        output_path = output_dir / 'reasoning' / Path(id).with_suffix('.txt') 
        output_path.write_text(plan)
        print(f"Saved plan for task {id} to {output_path}")

        #Create program
        program = synthesize_program(plan)
        program = remove_think(program)

        #Save the program in output/programs/id.py
        output_path = output_dir / 'programs' / Path(id).with_suffix('.py') 
        output_path.write_text(program)
        print(f"Saved program for task {id} to {output_path}")

        # Evaluate program
        grid, correct = evaluate(task,program)

        #Save the visualized result in output/visuals/id.png
        plot_prediction(grid, task['test'], id)
        print(f"Saved result for task {id} to {output_path}")

    for id, task in train_tasks.items():
        print(f"Working on {id}")
        
        #Create reasoning steps
        plan = create_reasoning(task)
        plan = extract_reasoning(plan)

        # Save the plan in output/reasoning/id.txt
        output_path = output_dir / 'reasoning' / Path(id).with_suffix('.txt') 
        output_path.write_text(plan)
        print(f"Saved plan for task {id} to {output_path}")

        #Create program
        program = synthesize_program(plan)
        program = remove_think(program)

        #Save the program in output/programs/id.py
        output_path = output_dir / 'programs' / Path(id).with_suffix('.py') 
        output_path.write_text(program)
        print(f"Saved program for task {id} to {output_path}")

        # Evaluate program
        grid, correct = evaluate(task,program)

        #Save the visualized result in output/visuals/id.png
        plot_prediction(grid, task['test'], id)
        print(f"Saved result for task {id} to {output_path}")

    return 



if __name__ == '__main__':
    main()
