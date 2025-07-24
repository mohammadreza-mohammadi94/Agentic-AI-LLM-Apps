import instructor
from openai import OpenAI
from schemas import ProjectInfo
from prompts import EXTRACTOR_SYSTEM_PROMPT
from dotenv import load_dotenv

# Load env
load_dotenv()
# Create client
client = instructor.patch(OpenAI())

# Agent
def extract_project_info(unstructured_text: str) -> ProjectInfo:
    """
    Receives unstructured text and return project info in structured text.
    """
    project_details = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": EXTRACTOR_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": unstructured_text
            }
        ],
        response_model=ProjectInfo
    )
    return project_details