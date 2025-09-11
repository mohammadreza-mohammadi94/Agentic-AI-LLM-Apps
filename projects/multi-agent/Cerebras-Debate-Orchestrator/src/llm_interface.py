from cerebras.cloud.sdk import Cerebras, CerebrasError
from typing import List, Dict

# The client is initialized once as a module-level
# global variable for efficiency.

try:
    cerebras_client = Cerebras(api_key="csk-5xdrewnk9jjk8x5xfk62yj2kmce5td3549dfkvwkmnrjy6kx")
    print("Cerebras client initialized successfully.")
except CerebrasError as e:
    print(f"Error initializing Cerebras client: {e}")
    cerebras_client = None

def get_cerebras_response(model, system_prompt, history):
    """
    Fetches a response from a specified Cerebras model.

    Args:
        model: The name of the model to call.
        system_prompt: The system prompt defining the agent's persona.
        history: The conversation history up to this point.

    Returns:
        The content of the model's response as a string.
    """
    if not cerebras_client:
        return "Error: Cerebras client is not initialized."
    
    messages = [{"role": "system", "content": system_prompt}] + history
    
    try:
        response = cerebras_client.chat.completions.create(
            model=model,
            messages=messages,
            max_completion_tokens=512,
            temperature=0.7,
            top_p=0.95,
        )
        return response.choices[0].message.content.strip()
    except CerebrasError as e:
        print(f"An error occured with model {model}: {e}")
        return f"An error occured while calling the model {model}."

