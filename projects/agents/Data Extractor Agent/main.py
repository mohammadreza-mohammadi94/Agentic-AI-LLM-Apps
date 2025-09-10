from agents import extract_project_info

SAMPLE_PROJECT_DESCRIPTION = """
For our new initiative, 'Project Phoenix', we need to build a customer churn prediction model.
The core of this system will be developed using Python, mainly with libraries like Scikit-learn and Pandas.
The main goal is to analyze user behavior and accurately identify customers who are likely to leave, ultimately aiming to reduce customer loss by at least 15% in the next quarter.
"""

def main():
    "Controls Workflow"
    print(" --- Unstructured Text ---")
    print(SAMPLE_PROJECT_DESCRIPTION)
    print("--------------------------")

    # Extract data with agent
    print("Extracting information using AI Agent...")
    extracted_data = extract_project_info(SAMPLE_PROJECT_DESCRIPTION)

    # Show structued data
    print("\n --- Extracted Structured Data ---")
    print(f"Project Name: {extracted_data.project_name}")
    print(f"Technologoes: {extracted_data.technologies}")
    print(f"Main Goal: {extracted_data.main_goal}")
    print("--------------------------")


if __name__ == '__main__':
    main()