def create_conversion_prompt(python_code: str) -> list:
    """Creates the messages list for the python to rust conversion task."""
    system_prompt = (
        "You are an expert Rust programmer. Your task is to rewrite a given Python script "
        "into idiomatic, high-performance, and memory-safe Rust code. "
        "Respond ONLY with the complete, compilable Rust code inside a single markdown block. "
        "Do not provide any explanations, introductions, or conclusions outside of the code block."
    )
    user_prompt = (
        "Please convert the following Python code to Rust. Ensure the logic remains identical "
        "and the implementation is as efficient as possible. Add comments where the Rust "
        "code might be non-obvious to a Python programmer.\n\n"
        "```python\n"
        f"{python_code}\n"
        "```"
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}]


def create_review_prompt_with_execution(python_code: str, rust_solutions: dict) -> list:
    """
    Creates an enhanced review prompt that includes code execution results.
    """
    system_prompt = (
        "You are a world-class software architect and Rust expert. Your task is to act as a judge "
        "and provide a critical review of several AI-generated Rust code submissions. "
        "Crucially, you will also be given the result of compiling and running each submission. "
        "Use this execution feedback as a primary factor in your evaluation."
    )

    user_prompt = (
        "The following Python code was given as a conversion task:\n\n"
        "```python\n"
        f"{python_code}\n"
        "```\n\n"
        "Here are the Rust submissions from different AI models, along with their compilation and execution results. "
        "Please review each one based on the following criteria in order of importance:\n"
        "1.  **Execution Result:** Did the code compile and run? Does its output seem correct?\n"
        "2.  **Performance:** Does the implementation look efficient?\n"
        "3.  **Idiomatic Style:** Is the code clean, safe, and idiomatic Rust?\n\n"
        "For each submission, provide a rating from 1 to 10 and a brief critique.\n\n"
        "---"
    )

    for model_name, data in rust_solutions.items():
        user_prompt += (
            f"\n\n### Submission from: `{model_name}`\n\n"
            "**Execution Result:**\n"
            f"```\n"
            f"Status: {data['execution']['status']}\n"
            f"Notes: {data['execution']['notes']}\n\n"
            f"Output/Error:\n{data['execution']['output']}\n"
            f"```\n\n"
            "**Generated Code:**\n"
            "```rust\n"
            f"{data['code']}\n"
            "```"
        )
    
    user_prompt += "\n\n--- \nPlease provide your final, consolidated review."

    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]