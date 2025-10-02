from langchain_ollama import OllamaLLM

from pathlib import Path

from arc_loader import train_tasks_small #, eval_tasks
from evaluator import evaluate

from utils.cleanser import extract_function_def, remove_think
from utils.plotprediction import plot_prediction



llm = OllamaLLM(
    model="deepseek-r1:32b",
    num_predict= 4096,
    num_ctx=4096,
    temperature=0.7
)

llm_code = OllamaLLM(
    model="qwen3-coder:latest",
    num_predict= 4096,
    num_ctx=4096,
    temperature=0.1
)


def create_reasoning(task):
    prompt = (
            "You are an expert algorithm designer specializing in grid-based puzzles. Your task is to analyze pairs of input/output grids and deduce the transformation rule. "
            "Based on the provided training examples, describe the transformation as a precise, step-by-step algorithm that can be implemented in Python. "
            "Focus on grid properties, object shapes, colors, and movements. Your description should be unambiguous and detailed enough for a programmer to follow. "
            "For example, instead of 'move the shape', specify 'find the largest contiguous object of color blue (2) and shift all its pixels down by 3 rows'.\n\n"
            "CRITICAL: Enclose your final algorithmic description ONLY within <reasoning>...</reasoning> tags. Do not add any other text, greetings, or explanations outside these tags.\n\n"
            f"TASK EXAMPLES:\n{task}\n\n"
        )

    return llm.invoke(prompt)



def synthesize_program(steps):
    prompt = (
            "You are a robotic, highly-disciplined Python code writer. You will be given a set of REASONING steps. "
            "Your one and only job is to translate these steps into a single, complete Python function named `p`. "
            "The function must adhere strictly to the signature `def p(grid: list[list[int]]) -> list[list[int]]:`.\n"
            "Your output must be **only the code**. Do not write any explanations, comments, markdown, or any text whatsoever. "
            "Your response must begin with `def p` and nothing else. The function body must be fully implemented, not a placeholder.\n\n"
            "--- PERFECT EXAMPLE ---\n"
            "REASONING:\n"
            "1. Get the dimensions of the input grid (height and width).\n"
            "2. Create a new grid of the same dimensions, filled with zeros.\n"
            "3. Iterate through each cell (r, c) of the input grid.\n"
            "4. If the cell's value is 2 (blue), place a 4 (red) at the corresponding location in the new grid.\n"
            "5. Otherwise, copy the original cell's value to the new grid.\n"
            "6. Return the new grid.\n\n"
            "def p(grid: list[list[int]]) -> list[list[int]]:\n"
            "    height = len(grid)\n"
            "    width = len(grid[0])\n"
            "    new_grid = [[0 for _ in range(width)] for _ in range(height)]\n"
            "    for r in range(height):\n"
            "        for c in range(width):\n"
            "            if grid[r][c] == 2:\n"
            "                new_grid[r][c] = 4\n"
            "            else:\n"
            "                new_grid[r][c] = grid[r][c]\n"
            "    return new_grid\n"
            "--- END OF EXAMPLE ---\n\n"
            "--- YOUR TASK ---\n"
            "REASONING:\n"
            f"{steps}\n\n"
            "CODE:"
    )
    
    return llm_code.invoke(prompt)


def main():
    #Set output dir
    output_dir = Path(__file__).resolve().parent.parent / 'output'

    for id, task in train_tasks_small.items():
        print(f"Working on {id}")
        
        #Create reasoning steps
        plan = create_reasoning(task)
        plan = remove_think(plan)

        # Save the plan in output/reasoning/id.txt
        output_path = output_dir / 'reasoning' / Path(id).with_suffix('.txt') 
        output_path.write_text(plan)
        print(f"Saved plan for task {id} to {output_path}")

        #Create program
        program = synthesize_program(plan)
        program = extract_function_def(program)

        #Save the program in output/programs/id.py
        output_path = output_dir / 'programs' / Path(id).with_suffix('.py') 
        output_path.write_text(program)
        print(f"Saved program for task {id} to {output_path}")

        # Evaluate program
        grid, correct = evaluate(task,program)

        #Save the visualized result in output/visuals/id.png
        plot_prediction(grid, task, id)
        print(f"Saved result for task {id} to {output_path}")

    return 



if __name__ == '__main__':
    main()
