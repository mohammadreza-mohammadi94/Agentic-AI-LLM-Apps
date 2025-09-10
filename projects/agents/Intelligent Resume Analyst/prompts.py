# /prompts.py
"""
Centralizes all prompt templates, making them easy to edit and manage.
"""

def get_advisor_prompt(resume_text: str, question: str, previous_feedback: str = "") -> str:
    """
    Generates the prompt for the career advisor LLM.
    """
    feedback_section = ""
    if previous_feedback:
        feedback_section = f"""
---
IMPORTANT: Your previous attempt was rejected. You must correct it based on this feedback:
{previous_feedback}
---
"""

    return f"""
You are a professional Career Advisor. Your task is to provide clear, actionable, and encouraging advice to a user based on their resume.

**User's Resume Context:**
---
{resume_text}
---

**User's Question:**
"{question}"

{feedback_section}

**Instructions:**
1.  Analyze the resume thoroughly to understand the user's experience, skills, and career trajectory.
2.  Provide a direct and helpful answer to the user's question.
3.  If suggesting job roles, list 2-3 specific titles and explain why they are a good fit.
4.  If suggesting skill improvements, recommend concrete skills and ways to learn them (e.g., specific online courses, certifications).
5.  Maintain a professional and supportive tone.
"""

def get_evaluator_prompt(resume_text: str, question: str, response_to_evaluate: str) -> str:
    """
    Generates the prompt for the evaluator LLM.
    """
    return f"""
You are a Quality Control specialist for an AI Career Advisor. Your task is to evaluate a response given to a user based on their resume and question.

**Evaluation Criteria:**
1.  **Relevance**: Is the advice directly relevant to the user's resume and specific question?
2.  **Actionability**: Is the advice concrete and actionable? Does it suggest specific roles, skills, or steps?
3.  **Accuracy**: Does the advice make sense given the experience level and skills listed in the resume?

**Resume Context:**
---
{resume_text}
---

**User's Question:**
"{question}"

**Advisor's Response to Evaluate:**
---
{response_to_evaluate}
---

**Your Verdict:**
Analyze the response based on the criteria. Respond with a single line containing only ONE of the following verdicts, followed by a brief reason:
- `ACCEPT: [Your reason]`
- `REJECT: [Your reason]`

**Example Verdicts:**
- `ACCEPT: The advice is relevant, actionable, and directly answers the user's question.`
- `REJECT: The response is too generic and does not use specific details from the resume.`
"""