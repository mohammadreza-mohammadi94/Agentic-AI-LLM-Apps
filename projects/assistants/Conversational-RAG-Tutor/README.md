# Conversational RAG Tutor for LangChain

This project is a conversational AI assistant designed to help users learn about and navigate the LangChain documentation. It's a Retrieval-Augmented Generation (RAG) application that can understand conversational context and provide answers based on the official LangChain documentation.

## Features

- **Conversational Interface:** Ask follow-up questions and have a natural conversation with the assistant.
- **History-Aware:** The assistant remembers the context of your conversation to provide more relevant answers.
- **Retrieval-Augmented Generation (RAG):** The assistant retrieves relevant information from the LangChain documentation before generating an answer, ensuring that the information is accurate and up-to-date.
- **Powered by LangChain:** Built using the LangChain library to create a powerful and flexible conversational AI.

## How it Works

The application uses a sophisticated conversational RAG chain built with LangChain. Here's a high-level overview of the process:

1.  **Question Reformulation:** When you ask a follow-up question, the assistant first reformulates it into a standalone question based on your chat history. This ensures that the retrieval process is accurate even if your question is not self-contained.
2.  **Document Retrieval:** The reformulated question is used to retrieve relevant documents from a FAISS vector store containing the LangChain documentation.
3.  **Answer Generation:** The retrieved documents, along with your original question and chat history, are passed to a large language model (LLM) to generate a final answer.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd Conversational-RAG-Tutor
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your environment variables:**
    Create a `.env` file in the root of the project and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your-openai-api-key"
    ```

## Usage

To start the conversational assistant, run the `main.py` script from within the `src` directory:

```bash
python src/main.py
```

The application will load the necessary models and data, and then prompt you to ask a question.

## Example Conversation

```
Starting the conversational LangChain Docs Assistant...
Ask a question about LangChain (or type 'exit' to quit): What are agents?

> Agent: Agents are computational systems that perceive their environment and act to achieve their goals. In LangChain, agents use an LLM to decide which actions to take.

Ask a question about LangChain (or type 'exit' to quit): how do they decide?

> Agent: Agents decide which action to take by using a thought process that is prompted by the LLM. The LLM is given a prompt that includes the agent's personality, the tools it has access to, and the user's input. The LLM then generates a thought, which is a plan for how to respond to the user's input. The agent then executes the plan.
```
