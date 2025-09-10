# -*- coding: utf-8 -*-
"""
image_analyzer_agent.py

This script demonstrates the use of a multi-modal AI agent from the AutoGen
library to analyze an image from a URL. It showcases two primary use cases:
1.  Generating a free-form, detailed description of the image.
2.  Extracting structured information from the image into a predefined
    Pydantic model.
"""

# Imports and Initial setup
import os
import asyncio
import requests
from io import BytesIO
from typing import Optional, Dict, Any, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from PIL import Image
from IPython.display import display, Markdown

from autogen_agentchat.messages import TextMessage, MultiModalMessage
from autogen_core import Image as AutoGenImage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken

# Configuration and Constants
# Load env
load_dotenv(override=True)
IMAGE_URL = "https://i.ibb.co/svfM3ygH/from-software-engineer-to-AI-DS.jpg"
MODEL_NAME = "gpt-4o-mini"

# Create and define Schema
class ImageDescription(BaseModel):
    """
    A Pydantic model to define the expected structured output from the agent.
    This ensures the LLM's response is predictable and validated.
    """
    scene: str = Field(description="A concise summary of the overall scene depicted in the image.")
    message: str = Field(description="The underlying message or point that the image is trying to convey.")
    style: str = Field(description="The artistic style of the image (e.g., 'photorealistic', 'cartoon', 'abstract').")
    orientation: Literal["portrait", "landscape", "square"] = Field(description="The orientation of the image.")
    
# Define Helper Functions
def fetch_image_from_url(url: str) -> Optional[AutoGenImage]:
    """
    Fetches an image from a URL and converts it into an AutoGenImage object.

    Args:
        url (str): The URL of the image to fetch.

    Returns:
        Optional[AutoGenImage]: An AutoGenImage object if successful, otherwise None.
    """
    try:
        print(f"Fetching image from: {url}")
        response = requests.get(url, timeout=20)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        pil_image = Image.open(BytesIO(response.content))
        autogen_image = AutoGenImage(pil_image)
        print("✅ Image fetched and converted successfully.")
        return autogen_image
    except requests.RequestException as e:
        print(f"❌ Error fetching image: {e}")
        return None
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return None
    
def display_structured_description(description: ImageDescription):
    """
    Formats and displays the structured image description in a readable format.

    Args:
        description (ImageDescription): The Pydantic object containing the description.
    """
    formatted_string = (
        f"**Scene:**\n{description.scene}\n\n"
        f"**Message:**\n{description.message}\n\n"
        f"**Style:**\n{description.style}\n\n"
        f"**Orientation:**\n{description.orientation}"
    )
    
    print("\n--- 🖼️ Structured Image Analysis 🖼️ ---")
    print(formatted_string)
    print("------------------------------------------")

# Core Agent 
async def analyze_image_with_agent(image: AutoGenImage, 
                                   structured_output: bool = False) -> Optional[Dict[str, Any]]:
    """
    Uses an AutoGen AssistantAgent to analyze the provided image.

    Args:
        image (AutoGenImage): The image to be analyzed.
        structured_output (bool): If True, the agent will be constrained to produce
                                  output matching the ImageDescription Pydantic model.

    Returns:
        The raw content of the agent's reply, which can be a string or a
        Pydantic object.
    """
    if not image:
        return None
    
    # Define the content of the message to send to the agent
    multi_model_message = MultiModalMessage(
        content=['Describe the content of this image in detail', image],
        source="user"
    )

    # Config model
    model_client = OpenAIChatCompletionClient(model=MODEL_NAME)

    # Config agent based on structured output is required
    if structured_output:
        print("\nInitializing agent for STRUCTUED description...")
        agent = AssistantAgent(
            name = "structued_description_agent",
            model_client=model_client,
            system_message="You are an expert and analyzing images and extracting specific details into a structued format.",
            output_content_type=ImageDescription
        )
    else:
        print("\nInitializing agent for FREE-FORM description...")
        agent = AssistantAgent(
            name="free_form_description_agent",
            model_client=model_client,
            system_message="You are an expert at describing images in rich, human-readable detail.",
        )

    # Run the agent and get the result
    print(f"Running {agent.name}")
    response = await agent.on_messages(
        [multi_model_message],
        cancellation_token=CancellationToken()
    )
    reply_content = response.chat_message.content
    return reply_content

# Main Execution
async def main():
    """
    Main function to run the complete image analysis pipeline.
    """
    image_to_analyze = fetch_image_from_url(IMAGE_URL)
    
    if image_to_analyze:
        # Get a free-form description ---
        free_form_reply = await analyze_image_with_agent(
            image=image_to_analyze,
            structured_output=False
        )
        if free_form_reply:
            print("\n--- 📝 Free-Form Image Description 📝 ---")
            print(free_form_reply)
            print("------------------------------------------")

        # Get a structured description ---
        structured_reply = await analyze_image_with_agent(
            image=image_to_analyze,
            structured_output=True
        )
        if isinstance(structured_reply, ImageDescription):
            display_structured_description(structured_reply)

if __name__ == "__main__":
    # This check ensures the code runs only when the script is executed directly
    asyncio.run(main())