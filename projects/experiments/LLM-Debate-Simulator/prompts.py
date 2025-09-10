# /prompts.py
from config import DEBATE_TOPIC

def get_debate_prompt(stance):
    """
    Generates the system prompt for a debater LLM based on its stance.

    Args:
        stance (str): The stance the LLM should take ('pro', 'con', or 'neutral').

    Returns:
        str: The formatted system prompt.
    """
    if stance == 'pro':
        argument_position = "You are a string advocate for remote work."
        instruction = "Argue passionately in favor of making remote work the default standard for tech companies."
    elif stance == 'con':
        argument_position = "You are a staunch critic of remote work."
        instruction = "Argue persuasively against making remote work the default standard, highlighting its drawbacks."
    else: # neutral
        argument_position = "You are a neutral, balanced analyst."
        instruction = "Provide a balanced, objective view, weighing the pros and cons of making remote work the default standard."

    return f"""
    **Role**: {argument_position}
    **Topic**: "{DEBATE_TOPIC}"
    **Task**: {instruction}
    
    **Instructions**:
    1. Your argument must be clear, logical, and persuasive.
    2. Use strong reasoning and, if possible, hypothetical examples.
    3. The argument should be concise, between 200 and 300 words.
    4. Do not introduce yourself or break character. Focus solely on the argument.
    """

def get_judge_prompt(arguments):
    """
    Generates the prompt for the evaluator LLM to rank the debate arguments.

    Args:
        arguments (Dict[str, Dict[str, str]]): A dictionary containing the arguments
            from each debater, including their model and stance.

    Returns:
        str: The formatted prompt for the judge.
    """
    argument_section = ""
    for debater, info in arguments.items():
        argument_section += f"--- Argument from {debater} ({info['stance']}) ---\n"
        argument_section += f"{info['argument']}\n\n"

    return f"""
    **Role**: You are an expert debate judge and logical analyst.
    **Task**: Evaluate the following three arguments on the topic: "{DEBATE_TOPIC}".
    
    **Arguments to Evaluate**:
    {argument_section}
    
    **Evaluation Criteria**:
    1.  **Clarity**: How clear and easy to understand is the argument?
    2.  **Logic**: How strong and well-reasoned are the points? Is the reasoning sound?
    3.  **Persuasiveness**: How compelling is the argument? Does it effectively convince the reader of its position?

    **Output Format**:
    You MUST provide your response in a valid JSON object. Do not include any text before or after the JSON.
    The JSON object must have a single key "ranking" which is a list of objects.
    Each object in the list represents one debater and must contain the following keys:
    - "rank": The rank of the argument (1, 2, or 3), where 1 is the best.
    - "debater": The name of the debater (e.g., 'Debater_Pro').
    - "stance": The debater's stance ('pro', 'con', 'neutral').
    - "model": The model used by the debater.
    - "reasoning": A brief, one-sentence explanation for why you assigned this rank, based on your criteria.
    
    **Example JSON Output**:
    {{
      "ranking": [
        {{
          "rank": 1,
          "debater": "Debater_Con",
          "stance": "con",
          "model": "gpt-4o-mini",
          "reasoning": "Presented the most logically structured argument with compelling evidence against the motion."
        }},
        {{
          "rank": 2,
          "debater": "Debater_Pro",
          "stance": "pro",
          "model": "llama3-8b-8192",
          "reasoning": "Made a passionate and clear case, but lacked sufficient counter-arguments."
        }},
        {{
          "rank": 3,
          "debater": "Debater_Neutral",
          "stance": "neutral",
          "model": "deepseek-coder",
          "reasoning": "The argument was balanced but lacked the persuasive force expected in a debate."
        }}
      ]
    }}
    """