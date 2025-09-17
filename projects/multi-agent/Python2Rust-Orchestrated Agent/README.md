# Python2Rust-Orchestrated Agent

This project demonstrates a multi-agent system that automates the process of converting Python code to idiomatic, high-performance Rust. It leverages multiple large language models (LLMs) to generate different Rust solutions, and then uses a "judge" LLM to review and rank the submissions.

## Features

- **Automated Code Conversion:** Converts Python code to Rust using multiple LLMs.
- **Multi-Agent Approach:** Uses different LLMs as "contender" agents to generate code and a "judge" agent to review the code.
- **Code Execution and Validation:** Compiles and runs the generated Rust code to validate its correctness and performance.
- **Comprehensive Review:** The judge LLM provides a detailed review of each submission, considering correctness, performance, and idiomatic style.
- **Extensible:** Easily configurable to use different models from various providers (e.g., Groq, Cerebras).

## How it Works

The process is orchestrated by the `main.py` script and can be broken down into the following steps:

1.  **Initialization:** The script initializes the API clients for the configured LLM providers (Groq and Cerebras).
2.  **Code Generation:** The script sends a prompt to each of the "contender" LLMs, asking them to convert the given Python code to Rust.
3.  **Code Execution:** Each generated Rust solution is then compiled and run. The execution results (status, output, and any errors) are captured.
4.  **Review:** The script then sends a prompt to the "judge" LLM. This prompt includes the original Python code, the generated Rust solutions from all the contender models, and the execution results for each solution.
5.  **Saving Results:** The final review and all the generated Rust solutions are saved to a new directory in the `results` folder.

## Requirements

- Python 3.6+
- Rust and `rustc` compiler installed and in your system's PATH.
- An environment file (`.env`) with your API keys for the LLM providers you want to use.

## Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mohammadreza-mohammadi94/Agentic-AI-LLM-Apps.git
    cd projects/multi-agent/Python2Rust-Orchestrated Agent
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**
    Create a `.env` file in the project's root directory and add your API keys:
    ```
    GROQ_API_KEY="your-groq-api-key"
    CEREBRAS_API_KEY="your-cerebras-api-key"
    ```

4.  **Run the script:**
    ```bash
    python main.py
    ```

## Configuration

The models used for code generation and review can be configured in the `config.py` file.

-   `MODEL_CONFIG`: This dictionary defines the models to be used from each platform (e.g., `groq`, `cerebras`). You can add or remove models as needed.
-   `JUDGE_PLATFORM` and `JUDGE_MODEL_NAME`: These variables specify which model to use as the "judge" for the review task.

## Project Structure

```
.
├── config.py           # Model configuration
├── file_handler.py     # Handles saving the results
├── llm_clients.py      # API clients for LLM providers
├── main.py             # Main orchestration script
├── prompts.py          # Prompts for the LLMs
├── README.md           # This file
└── results/            # Output directory for the results
```

## Example

After running the script, a new directory will be created in the `results` folder with a name like `conversion_result_20240101_120000`. This directory will contain the following files:

-   `review_summary.md`: A markdown file containing the final review from the judge LLM.
-   `[model_name]_rust_code.rs`: A Rust file for each of the contender models, containing the generated Rust code.

The `review_summary.md` file will look something like this:

# Python to Rust Conversion Review

**Date:** 2024-01-01 12:00
**Judge Model:** `qwen-3-coder-480b`

## Original Python Code

```python
import time

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

# ... (rest of the Python code)
```

---

## Judge's Review of Submissions

### Submission from: `llama-3.3-70b-versatile`

**Execution Result:**
```
Status: success
Notes: Code compiled and executed successfully.

Output/Error:
... (output of the Rust code)
```

**Generated Code:**
```rust
use std::time::Instant;

fn mandelbrot(c: num_complex::Complex<f64>, max_iter: u32) -> u32 {
    let mut z = num_complex::Complex::new(0.0, 0.0);
    let mut n = 0;
    while z.norm_sqr() <= 4.0 && n < max_iter {
        z = z * z + c;
        n += 1;
    }
    n
}

// ... (rest of the Rust code)
```

**Critique:**

Rating: 9/10

This submission is excellent. The code is idiomatic, efficient, and correctly implements the logic of the original Python code.

... (and so on for the other submissions)
