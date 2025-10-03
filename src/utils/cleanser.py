import regex as re



def extract_reasoning(text):
    """
    Extracts the text between a single pair of <reasoning> tags.
    Returns a clean, structured explanation or empty string if no reasoning block is found.
    """
    # Find content between <reasoning> tags
    match = re.search(r"<reasoning>([\s\S]*?)</reasoning>", text, re.IGNORECASE | re.DOTALL)
    if not match:
        return text
    
    reasoning = match.group(1).strip()

    # Remove unnecessary whitespace
    reasoning = re.sub(r'\n\s*\n', '\n\n', reasoning)
    
    return reasoning.strip()

def remove_think(text):
    """
    Removes all content between <think> and </think> tags from the input text.
    Returns the text with all thinking sections removed.
    """
    # Remove all content between <think> tags
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # Clean up any double newlines or excessive whitespace that might be left
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)
    return cleaned_text.strip()

def extract_code(code):
    """
    Extracts the Python code block from a text that may contain <think>...</think>
    reasoning or explanations. If multiple solve functions exist, returns the last one
    including all code up to its last 'return grid' statement.
    """
    # First try to find code blocks
    code_blocks = re.findall(r"```python\n(.*?)```", code, re.DOTALL)
    if code_blocks:
        code = "\n".join(code_blocks)
    
    # Find all solve function definitions
    solve_starts = re.finditer(r"def\s+solve\s*\([^)]*\):", code, re.DOTALL)
    
    last_solve = None
    for match in solve_starts:
        start_pos = match.start()
        # Find all return grid/output statements after this function definition
        returns = list(re.finditer(r"return\s+(?:grid|output)", code[start_pos:], re.DOTALL))
        if returns:
            # Get position of last return grid/output in this function
            last_return = returns[-1]
            # Extract from function start to last return + the returned value
            func_code = code[start_pos:start_pos + last_return.end()]
            last_solve = func_code
    
    if last_solve:
        return last_solve.strip()
    
    # Fallback: try to find any solve function with any return statement
    solve_matches = re.finditer(r"def\s+solve\s*\([^)]*\):.*?(?:return\s+[^:;\n]+)", code, re.DOTALL)
    last_any_solve = None
    for match in solve_matches:
        last_any_solve = match.group(0)
    
    return last_any_solve.strip() if last_any_solve else ""

def extract_function_def(generated_text: str) -> str:
    # Extract code from code blocks if present
    code_block_match = re.search(r"```(?:python)?([\s\S]*?)```", generated_text, re.DOTALL | re.IGNORECASE)
    if code_block_match:
        code = code_block_match.group(1).strip()
    else:
        code = generated_text.strip()

    # Remove any stray leading or trailing fences
    code = re.sub(r'^```(?:python)?\s*', '', code, re.IGNORECASE)
    code = re.sub(r'\s*```$', '', code)
    
    # Remove "--- END OF EXAMPLE ---" and similar markers
    code = re.sub(r'---\s*(?:END OF|START OF|BEGIN|END)\s*(?:EXAMPLE|CODE|SOLUTION)\s*---.*?\n', '', code, flags=re.IGNORECASE|re.MULTILINE)

    # Common header pattern with optional return type
    header_pattern = r"def\s+{name}\s*\([^)]*\)\s*(->\s*[^:]+)?\s*:"
    body_pattern = r"[\s\S]+?return\s+(?:result|grid|output)"  # Stop at return statement
    lookahead = r"(?=\n\s*def\s+[a-zA-Z_]\w*\s*\(|$)"

    # Try patterns in order of preference
    patterns = [
        header_pattern.format(name="p"),  # First try def p
        header_pattern.format(name="transform"),  # Then try def transform
        r"def\s+[a-zA-Z_]\w*\s*\([^)]*\)\s*(->\s*[^:]+)?\s*:"  # Finally try any function
    ]

    final_code = None
    for pattern in patterns:
        func_match = re.search(pattern + body_pattern + lookahead, code, re.DOTALL)
        if func_match:
            final_code = func_match.group(0).strip()
            break

    if not final_code:
        final_code = code

    # Remove any remaining code blocks and clean up
    final_code = re.sub(r"```.*?```", "", final_code, re.DOTALL).strip()

    return final_code
