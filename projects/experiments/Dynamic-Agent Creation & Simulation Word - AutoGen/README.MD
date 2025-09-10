# Multi-Agent Simulation World

[](https://www.python.org/downloads/)
[](https://opensource.org/licenses/MIT)

A flexible and extensible framework for creating and running multi-agent simulations. This project provides the core components to build a virtual "world" inhabited by autonomous AI agents that can interact with each other and their environment through a structured messaging system.

The primary goal of this framework is to allow developers and researchers to model complex systems, simulate social interactions, and observe the emergent behaviors of multiple AI agents collaborating or competing to achieve their goals.

-----

## ✨ Key Concepts

This framework is built upon four core modules that work together to create a dynamic simulation:

  * ### **`world.py` - The Simulation Environment**

    This is the heart of the simulation. The `World` class manages the environment's state, keeps track of all agents within it, and runs the main simulation loop. It is responsible for facilitating interactions and ensuring the rules of the environment are followed.

  * ### **`agent.py` - The Autonomous Entities**

    This module defines the `Agent` class. Each agent is an independent entity with its own distinct `persona` (defined by its system prompt and instructions), memory, and capabilities. Agents perceive the world, make decisions, and perform actions based on their individual goals.

  * ### **`creator.py` - The Agent Factory**

    To populate the world with diverse agents, the `creator.py` module acts as a factory. It contains logic to easily instantiate and configure multiple agents with different roles, personas, and goals, making it simple to set up complex simulation scenarios.

  * ### **`messages.py` - The Communication Protocol**

    Agents need a way to communicate with each other and with the world. This module defines the structured message types that agents use for interaction. This ensures that communication is clear, predictable, and can be easily logged and analyzed.


## ⚙️ How It Works

The simulation operates on a turn-based or event-driven loop managed by the `World` object. In each iteration of the loop:

1.  The `World` provides each agent with relevant information about the current state of the environment.
2.  Each `Agent` processes this information, decides on an action based on its persona and goals, and generates a `Message`.
3.  The `World` collects all messages and updates the environment state accordingly.
4.  The loop repeats, allowing for complex and emergent behaviors to unfold over time.


## 🔧 Getting Started

### Prerequisites

  * Python 3.9+
  * An OpenAI API key (or other LLM provider)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/mohammadreza-mohammadi94/AgenticAI.git
    cd <project-name>
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment:**
    Create a `.env` file in the root directory and add your API key:

    ```env
    OPENAI_API_KEY="sk-..."
    ```

## 🏃‍♀️ How to Run

The main simulation is likely initiated from the `world.py` script. To start the simulation, run:

```bash
python world.py
```

You can configure the initial state of the world, the number of agents, and their personas within the `world.py` or `creator.py` files.