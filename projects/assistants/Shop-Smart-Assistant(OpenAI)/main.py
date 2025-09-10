# Import standard Python libraries
import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

# Import third-party libraries
from openai import OpenAI
import gradio as gr
from typing import List, Dict, Any

# Import custom logger module
from logger import setup_logger

# ------------------------ #
# Configure Logger        #
# ------------------------ #
# Initialize logger for logging application events and errors
logger = setup_logger(__name__, log_file="shopsmart_assistant.log")

# ------------------------ #
# Load Environment Variables #
# ------------------------ #
# Load environment variables from .env file (e.g., API keys)
load_dotenv(override=True)

# ------------------------ #
# Initialize OpenAI Client #
# ------------------------ #
# Set up OpenAI client with API key from environment variables
try:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai = OpenAI(api_key=openai_api_key)
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found.")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    raise

# --------------------------------- #
# Load System Prompt from JSON File #
# --------------------------------- #
# Load system prompt from prompts.json or use fallback if loading fails
try:
    with open("prompts.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)
        SYSTEM_PROMPT = prompts.get("prompts", {}).get("system_prompt", {}).get("content", "")
        if not SYSTEM_PROMPT:
            raise ValueError("System prompt not found in prompts.json")
    logger.info("System prompt loaded successfully from prompts.json")
except Exception as e:
    logger.error(f"Failed to load system prompt: {e}")
    SYSTEM_PROMPT = "You are ShopSmart Assistant, a customer support agent for ShopSmart. Please assist customers professionally and empathetically. Log issues and notify the team for urgent cases."
    logger.warning("Using minimal fallback system prompt due to error")

# ------------------------------- #
# Initialize Pushover Credentials #
# ------------------------------- #
# Load Pushover credentials for sending notifications
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
# PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

if not PUSHOVER_USER or not PUSHOVER_TOKEN:
    logger.warning("Pushover credentials not set. Notifications will be logged locally only.")

# -------------------------------- #
# Ensure Customer Issues File Exists #
# -------------------------------- #
# Create customer_issues.jsonl file if it doesn't exist
ISSUES_FILE = "customer_issues.jsonl"
try:
    if not os.path.exists(ISSUES_FILE):
        with open(ISSUES_FILE, "a", encoding="utf-8") as f:
            pass  # Create empty file
        logger.info(f"Created {ISSUES_FILE} for logging customer issues")
except Exception as e:
    logger.error(f"Failed to create {ISSUES_FILE}: {e}")
    raise RuntimeError(f"Cannot initialize {ISSUES_FILE}. Please check file permissions and disk space.")

# -------------------------------- #
# Tool Definitions in JSON Format #
# -------------------------------- #
# Define tools for logging issues and sending notifications
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "log_customer_issue",
            "description": "Log a customer issue with details for tracking and resolution.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Unique identifier for the customer (e.g., email or ID)"
                    },
                    "issue_description": {
                        "type": "string",
                        "description": "Detailed description of the customer's issue"
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Urgency level of the issue"
                    }
                },
                "required": ["customer_id", "issue_description", "urgency"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_notification",
            "description": "Send a notification to the support team for urgent issues.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Notification message to send to the support team"
                    }
                },
                "required": ["message"],
                "additionalProperties": False
            }
        }
    }
]

# ------------------------ #
# Tool Functions           #
# ------------------------ #
def log_customer_issue(customer_id: str, issue_description: str, urgency: str) -> Dict[str, str]:
    """
    Log a customer issue to customer_issues.jsonl and return a confirmation.
    
    Args:
        customer_id (str): Unique identifier for the customer.
        issue_description (str): Description of the issue.
        urgency (str): Urgency level (low, medium, high).
    
    Returns:
        Dict[str, str]: Status and message indicating success or failure.
    """
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "customer_id": customer_id,
            "issue_description": issue_description,
            "urgency": urgency
        }
        with open(ISSUES_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        logger.info(f"Logged issue for {customer_id}: {issue_description} (Urgency: {urgency})")
        return {"status": "success", "message": "Issue logged successfully"}
    except Exception as e:
        logger.error(f"Failed to log issue to {ISSUES_FILE}: {e}")
        return {"status": "error", "message": f"Failed to log issue: {str(e)}"}

def send_notification(message: str) -> Dict[str, str]:
    """
    Send a notification to the support team via Pushover or log locally if credentials are missing.
    
    Args:
        message (str): Notification message to send.
    
    Returns:
        Dict[str, str]: Status and message indicating success or failure.
    """
    try:
        if PUSHOVER_USER and PUSHOVER_TOKEN:
            payload = {
                "user": PUSHOVER_USER,
                "token": PUSHOVER_TOKEN,
                "message": message
            }
            logger.debug(f"Sending Pushover notification with payload: {payload}")
            response = requests.post(PUSHOVER_URL, data=payload, timeout=5)
            response.raise_for_status()
            logger.info(f"Notification sent: {message}")
            return {"status": "success", "message": "Notification sent successfully"}
        else:
            logger.info(f"Local notification: {message}")
            return {"status": "success", "message": "Notification logged locally"}
    except requests.exceptions.HTTPError as e:
        error_detail = f"HTTP Error: {str(e)}"
        try:
            error_detail += f" - Response: {e.response.text}"
        except:
            pass
        logger.error(f"Failed to send notification: {error_detail}")
        return {"status": "error", "message": error_detail}
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return {"status": "error", "message": str(e)}

def handle_tool_calls(tool_calls: List[Any]) -> List[Dict[str, Any]]:
    """
    Process tool calls from the OpenAI API and return results.
    
    Args:
        tool_calls (List[Any]): List of tool call objects from the API response.
    
    Returns:
        List[Dict[str, Any]]: List of tool call results with role, content, and tool_call_id.
    """
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        try:
            arguments = json.loads(tool_call.function.arguments)
            logger.info(f"Executing tool: {tool_name} with arguments: {arguments}")
            tool_func = globals().get(tool_name)
            if tool_func:
                result = tool_func(**arguments)
            else:
                result = {"status": "error", "message": f"Tool {tool_name} not found"}
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in tool call arguments: {e}")
            results.append({
                "role": "tool",
                "content": json.dumps({"status": "error", "message": "Invalid tool arguments"}),
                "tool_call_id": tool_call.id
            })
    return results

def chat(message: str, history: List[Any]) -> str:
    """
    Handle customer support chat interactions with tool calling.
    
    Args:
        message (str): User's input message.
        history (List[Any]): Chat history from Gradio, typically a list of [user, assistant] pairs or dicts.
    
    Returns:
        str: Assistant's response or an error message.
    """
    try:
        # Normalize history to ensure all entries are valid message dictionaries
        normalized_history = []
        for item in history:
            if isinstance(item, dict) and "role" in item and "content" in item:
                normalized_history.append(item)
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                normalized_history.append({"role": "user", "content": str(item[0])})
                normalized_history.append({"role": "assistant", "content": str(item[1])})
            else:
                logger.warning(f"Invalid history item skipped: {item}")
        
        # Construct message history for OpenAI API
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + normalized_history + [{"role": "user", "content": message}]
        logger.debug(f"Sending messages to OpenAI API: {json.dumps(messages, indent=2)}")
        
        done = False
        max_attempts = 3
        attempt = 0

        while not done and attempt < max_attempts:
            attempt += 1
            try:
                # Call OpenAI API with tools
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    temperature=0.7
                )
                finish_reason = response.choices[0].finish_reason

                if finish_reason == "tool_calls":
                    message_response = response.choices[0].message
                    tool_calls = message_response.tool_calls
                    if tool_calls:
                        results = handle_tool_calls(tool_calls)
                        messages.append(message_response)
                        messages.extend(results)
                    else:
                        logger.warning("Tool calls requested but none provided")
                        done = True
                else:
                    done = True
                    return response.choices[0].message.content
            except Exception as e:
                logger.error(f"API call failed (attempt {attempt}/{max_attempts}): {e}")
                if attempt == max_attempts:
                    return "Sorry, I'm experiencing technical difficulties. Please try again later."
        
        return "Sorry, I couldn't process your request. Please contact support directly."
    except Exception as e:
        logger.error(f"Chat function error: {e}")
        return "An unexpected error occurred. Please try again."

def launch_chatbot() -> None:
    """
    Launch the Gradio chat interface for ShopSmart Assistant.
    
    Raises:
        Exception: If the Gradio interface fails to launch.
    """
    try:
        interface = gr.ChatInterface(
            fn=chat,
            chatbot=gr.Chatbot(height=500),
            title="ShopSmart Assistant",
            description="Welcome to ShopSmart Assistant, your AI-powered customer support for ShopSmart electronics. How can I assist you today?",
            theme="soft",
            examples=[
                "My laptop won't charge. Can you help?",
                "I need a refund for my order #12345.",
                "Urgent: My TV arrived damaged!"
            ],
            cache_examples=False
        )
        logger.info("Launching ShopSmart Assistant Gradio interface")
        interface.launch(server_name="127.0.0.1", server_port=7860, share=False)
    except Exception as e:
        logger.error(f"Failed to launch Gradio interface: {e}")
        raise

if __name__ == "__main__":
    # Send startup notification
    send_notification("ShopSmart Assistant started")
    # Launch the chatbot
    launch_chatbot()