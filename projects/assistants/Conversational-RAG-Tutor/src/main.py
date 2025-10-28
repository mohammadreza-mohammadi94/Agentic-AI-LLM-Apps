"""
Main entry point for the Conversational LangChain Docs Assistant.

This script initializes all components (LLM, vector store, RAG chain) and
runs an interactive command-line loop to chat with the user.
"""

import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

import config
from vector_store import get_vector_store
from chain import create_conversational_rag_chain

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    """
    Initializes and runs the main interactive loop for the AI assistant.
    """
    # Load environment variables
    load_dotenv()
    logger.info("Starting the conversational LangChain Docs Assistant...")

    # Initialization
    # LLM
    llm = ChatOpenAI(
        model_name=config.LLM_MODEL_NAME,
        temperature=0,
        max_tokens=500,
    )

    # Vector store
    vector_store = get_vector_store()
    if vector_store is None:
        logger.critical(
            "Could not initialize the vector store. Application cannot start."
        )
        return

    # create a retriever from the vector store
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 4}
    )

    # create hte main conversational rag chain
    rag_chain = create_conversational_rag_chain(retriever, llm)

    # Initialize an empty list to store the conversation history
    chat_history = []

    # Interactive Loop
    print("\n" + "=" * 60)
    print("      Welcome to the LangChain Docs Assistant!      ")
    print(" You can ask me about LCEL, Runnables, Chains, or Agents.")
    print("         Type 'exit' to end the session.          ")
    print("=" * 60)

    while True:
        try:
            # Get user input from the command line
            user_input = input("\nYou: ")

            # Check for exit condition
            if user_input.lower() in ["exit", "quit"]:
                logger.info("User requested to exit. Shutting down.")
                break

            logger.info(f"User input received: '{user_input}'")

            # Invoke the RAG chain with the current input and the chat history
            response = rag_chain.invoke(
                {"input": user_input, "chat_history": chat_history}
            )

            # Extract the answer from the response dictionary
            answer = response.get(
                "answer",
                "Sorry, I encountered an issue and couldn't generate a response.",
            )
            print(f"AI Assistant: {answer}")

            # Update History
            # Append the user's message and the AI's response to the history
            # This is crucial for the chain to have context in the next turn
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=answer))

        except (KeyboardInterrupt, EOFError):
            # Handle Ctrl+C or Ctrl+D gracefully
            logger.info("\nInterrupted by user. Exiting.")
            break
        except Exception as e:
            # Log any other unexpected errors
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            print("\nAn unexpected error occurred. Please try again.")


if __name__ == "__main__":
    main()
