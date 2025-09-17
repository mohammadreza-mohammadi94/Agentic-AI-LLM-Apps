# main.py

import os
import subprocess
from dotenv import load_dotenv
from config import MODEL_CONFIG, JUDGE_PLATFORM, JUDGE_MODEL_NAME
from prompts import create_conversion_prompt, create_review_prompt_with_execution
from llm_clients import GroqClient, CerebrasClient
from file_handler import save_results

def initialize_clients() -> dict:
    """Initializes API clients based on available keys."""
    load_dotenv()
    clients = {}
    try:
        clients["groq"] = GroqClient(api_key=os.getenv("GROQ_API_KEY"))
    except ValueError as e:
        print(e)
    try:
        clients["cerebras"] = CerebrasClient(api_key=os.getenv("CEREBRAS_API_KEY"))
    except ValueError as e:
        print(e)
    return clients

def execute_rust_code(rust_code: str, model_name: str) -> dict:
    """
    Tries to compile and run the given Rust code.

    Args:
        rust_code (str): The Rust code to execute.
        model_name (str): The name of the model that generated the code, used for filenames.

    Returns:
        dict: A dictionary containing the status ('success' or 'error'),
              and the output or error message.
    """
    # Sanitize model name for filename
    safe_model_name = model_name.replace("/", "_")
    file_name = f"temp_{safe_model_name}"
    
    with open(f"{file_name}.rs", "w", encoding="utf-8") as f:
        f.write(rust_code)
        
    try:
        # Step 1: Compile the code using rustc
        # -O for optimization
        compile_process = subprocess.run(
            ["rustc", "-O", f"{file_name}.rs"],
            check=True,
            capture_output=True,
            text=True,
            timeout=30  # 30-second timeout for compilation
        )
        
        # Step 2: Run the compiled executable
        run_process = subprocess.run(
            [f"./{file_name}"],
            check=True,
            capture_output=True,
            text=True,
            timeout=15  # 15-second timeout for execution
        )
        
        return {
            "status": "success",
            "output": run_process.stdout,
            "notes": "Code compiled and executed successfully."
        }
        
    except FileNotFoundError:
        return {
            "status": "error",
            "output": "Compiler Error: `rustc` not found. Is Rust installed and in your PATH?"
        }
    except subprocess.CalledProcessError as e:
        # This catches both compilation and runtime errors
        return {
            "status": "error",
            "output": e.stderr,
            "notes": "The code failed during compilation or execution."
        }
    except subprocess.TimeoutExpired as e:
        return {
            "status": "error",
            "output": f"Process timed out: {e.cmd}",
            "notes": "The code took too long to compile or run."
        }
    finally:
        # Clean up temporary files
        for ext in [".rs", ""]:
            if os.path.exists(f"{file_name}{ext}"):
                os.remove(f"{file_name}{ext}")


def main():
    """Main function to orchestrate the conversion, execution, and review process."""
    
    python_to_convert = """
import time

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def compute_mandelbrot(width, height, max_iter):
    image = [[0] * width for _ in range(height)]
    for row in range(height):
        for col in range(width):
            c = complex(-2.0 + (col / width) * 3.0, -1.5 + (row / height) * 3.0)
            color = mandelbrot(c, max_iter)
            image[row][col] = color
    return image

if __name__ == "__main__":
    start_time = time.time()
    
    WIDTH, HEIGHT = 80, 40
    MAX_ITER = 256
    
    image = compute_mandelbrot(WIDTH, HEIGHT, MAX_ITER)
    
    chars = ".,-~:;=!*#$@"
    for row in image:
        line = ""
        for val in row:
            if val == MAX_ITER:
                line += " "
            else:
                line += chars[val % len(chars)]
        print(line)
        
    end_time = time.time()
    print(f"\\nPython Execution Time: {end_time - start_time:.4f} seconds")
"""

    clients = initialize_clients()
    if not clients:
        print("No API clients could be initialized.")
        return

    rust_solutions = {}
    conversion_prompt = create_conversion_prompt(python_to_convert)

    print("--- Starting Code Generation and Execution Phase ---")
    contender_models = [
        (p, m) for p, conf in MODEL_CONFIG.items() for m in conf["models"]
        if not (p == JUDGE_PLATFORM and m == JUDGE_MODEL_NAME)
    ]
    
    for platform, model_name in contender_models:
        if platform not in clients:
            print(f"Skipping platform {platform} as client is not available.")
            continue
        
        client = clients[platform]
        print(f"\n--- Generating and Executing for {model_name} on {platform} ---")
        
        # Generate the code
        rust_code = client.generate(model_name, conversion_prompt)
        rust_code = rust_code.replace("```rust", "").replace("```", "").strip()
        
        # Compile and run the code
        execution_result = execute_rust_code(rust_code, model_name)
        
        rust_solutions[model_name] = {
            "code": rust_code,
            "execution": execution_result
        }
        print(f"Execution status for {model_name}: {execution_result['status']}")

    print("\n\n--- Starting Review Phase ---")
    if JUDGE_PLATFORM not in clients:
        review_text = "Review phase was skipped."
    else:
        judge_client = clients[JUDGE_PLATFORM]
        # Use the new, richer review prompt
        review_prompt = create_review_prompt_with_execution(python_to_convert, rust_solutions)
        review_text = judge_client.generate(JUDGE_MODEL_NAME, review_prompt)

    print("\n\n--- Saving Results ---")
    # You might want to update save_results to handle the new structure
    # For now, we pass a simplified version for demonstration
    simplified_solutions = {k: v['code'] for k, v in rust_solutions.items()}
    save_results(python_to_convert, simplified_solutions, review_text)
    print("\nProcess finished successfully.")


if __name__ == "__main__":
    main()