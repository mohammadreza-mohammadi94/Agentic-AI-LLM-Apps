# Multi-Modal Image Analyzer Agent

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)
[](https://microsoft.github.io/autogen/)

This project demonstrates an advanced multi-modal AI agent built with the **Microsoft AutoGen** framework. The agent is capable of analyzing an image from a URL and generating both a detailed, free-form description and a structured analysis of its contents, style, and message.

The core of the project is an `AssistantAgent` powered by a multi-modal model (like GPT-4o) that can understand and interpret visual information in conjunction with text-based prompts.

-----

## ✨ Key Features

  - **Multi-Modal Input**: Processes both text prompts and images simultaneously to perform complex analysis.
  - **Dual Output Modes**: Can generate either a human-readable, free-form description or structured, predictable data using Pydantic models.
  - **AutoGen Framework**: Built on a powerful framework for creating sophisticated and conversational AI agents.
  - **Modular Codebase**: The code is organized into reusable functions with clear error handling, making it easy to read, maintain, and extend.

-----

## 🚀 Example: Agent Analysis

This example showcases the agent's ability to generate a detailed, free-form description of a complex image.

### Input Image

### Generated Free-Form Description

The agent produced the following detailed breakdown of the image:

> The image depicts a whimsical, colorful room that blends elements of technology and creativity.
>
> **Room Layout**
>
>   * **Configuration**: The room features a desk on the left side with a chair and computer setup. The floor extends out, with visible patterns of vibrant colors that draw the eye towards the open door on the right.
>
> **Desk Area**
>
>   * **Furniture**: The desk is wooden and has a simple design. A computer monitor is perched on it, displaying lines of code, implying a tech-savvy environment.
>   * **Accessories**:
>       * A desk lamp with a flexible arm illuminates the workspace.
>       * A small audio speaker sits next to the monitor, suggesting a multimedia focus.
>       * The base of the chair is distinctively minimalist and functional.
>
> **Robot Figure**
>
>   * **Appearance**: Sitting in the chair is a small, cartoonish robot. It has a friendly face with large eyes and a slight smile, giving it a friendly, approachable appearance.
>   * **Position**: The robot seems engaged with the computer or the room’s atmosphere, enhancing the tech theme.
>
> **Doorway and Colors**
>
>   * **Door**: The door is wide open, inviting as it leads to an explosion of colors. It contrasts sharply with the more muted tones of the room.
>   * **Colorful Background**: Beyond the door, vibrant streaks of colors—red, blue, green, and yellow—radiate from a central point that resembles a starburst or cosmic energy. This creates a captivating visual that suggests creativity, innovation, or perhaps a gateway to different realms of ideas.
>
> **Wall and Clock**
>
>   * **Wall**: The walls are a soothing teal color that enhances the bright colors of the door.
>   * **Clock**: A wall clock is mounted above the desk, indicating the time in a classic analog style, subtly grounding the futuristic elements of the room.
>
> The entire scene evokes a sense of inspiration and curiosity, combining both the seriousness of coding and the imaginative possibilities that lie beyond the door.

-----

## 🔧 Setup and Installation

Follow these steps to set up and run the project locally.

### 1\. Clone the Repository

```bash
git clone https://github.com/mohammadreza-mohammadi/AgenticAI.git
cd Image Analyzer Agent - AutoGen
```

### 2\. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3\. Install Dependencies

Create a `requirements.txt` file with the following content:

```txt
pyautogen
python-dotenv
requests
Pillow
ipython
```

Then, run the installation command:

```bash
pip install -r requirements.txt
```

### 4\. Configure Environment Variables

Create a file named `.env` in the root of your project and add your OpenAI API key:

```env
OPENAI_API_KEY="sk-..."
```

-----

## 🏃‍♀️ How to Run

Execute the main script from your terminal to run the analysis pipeline:

```bash
python image_analyzer_agent.py
```

The script will fetch the image, run both the free-form and structured analysis, and print the results to your console.