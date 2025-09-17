import os
import datetime
from config import JUDGE_MODEL_NAME

def save_results(python_code: str, rust_solutions: dict, review: str):
    """Saves the generated Rust code and final review to files"""
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"results/conversion_result_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save each rust solution 
    for model_name, rust_code in rust_solutions.items():
        safe_model_name = model_name.replace("/", "_")
        file_path = os.path.join(output_dir, f"{safe_model_name}_rust_code.rs")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rust_code)
        print(f"Saved rust code to {file_path}")
    
    # Create and save the final review markdown file
    md_content = f"# Python to Rust Conversion Review\n\n"
    md_content += f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md_content += f"**Judge Model:** `{JUDGE_MODEL_NAME}`\n\n"
    md_content += "## Original Python Code\n\n"
    md_content += f"```python\n{python_code}\n```\n\n"
    md_content += "--- \n\n"
    md_content += "## Judge's Review of Submissions\n\n"
    md_content += review
    
    review_file_path = os.path.join(output_dir, "review_summary.md")
    with open(review_file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ Saved review summary to {review_file_path}")