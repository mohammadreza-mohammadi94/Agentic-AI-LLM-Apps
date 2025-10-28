"""
Main application module for the Tech News RAG Assistant.

This module serves as the entry point for the application. It orchestrates the
entire RAG pipeline, from loading data and initializing models to handling user
interaction and generating responses. The main function guides the user through
the process of asking questions and receiving answers based on a set of articles.
"""

import logging
from config import load_environment
from document_loader import load_and_tag_articles
from vector_store import get_embedding_model, create_vector_store
from llm import get_chat_model
from retriever import create_retriever
from rag import create_rag_chain

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the Tech News RAG Assistant.

    This function initializes the RAG pipeline, including loading articles,
    creating a vector store, and setting up the language model. It then enters
    a loop to interact with the user, allowing them to ask questions and
    receive answers from the RAG chain.
    """
    load_environment()
    logger.info("Starting the Tech News RAG Assistant!")
    articles_to_load = {
        "KD Nuggets": "https://www.kdnuggets.com/agentic-ai-coding-with-google-jules",
        "Tech Crunch": "https://techcrunch.com/2025/10/23/openai-buys-sky-an-ai-interface-for-mac/",
    }
    logger.info("Initializing embedding...")
    embeddings = get_embedding_model()
    logger.info("Initializing LLM Model...")
    llm = get_chat_model()

    documents = load_and_tag_articles(articles_to_load)
    if not documents:
        logger.warning(
            "No documents were loaded. The assistant may not have any knowledge."
        )
        return

    vector_store = create_vector_store(documents, embeddings)

    while True:
        print("\n" + "-" * 50)
        question = input("Ask a question about the articles (type 'q' to quit.): ")
        if question.lower() == "q":
            logger.info("Exiting the assistant.")
            break
        print("\nAvailable sources to filter by:")
        sources = list(articles_to_load.keys())
        for i, source in enumerate(sources, 1):
            print(f"{i}. {source}")
        print(f"{len(sources) + 1}. All")

        try:
            choice = int(input(f"Choose a source number [1-{len(sources)+1}]: "))
            if choice < 1 or choice > len(sources) + 1:
                raise ValueError
        except ValueError:
            logger.warning("Invalid source choice. Defaulting to 'All' sources.")
            choice = len(sources) + 1

        if choice <= len(sources):
            selected_source = sources[choice - 1]
            logger.info(f"Searching for answers within '{selected_source}' articles...")
            retriever = create_retriever(vector_store, selected_source)
        else:
            logger.info("Searching for answers within 'All' articles...")
            retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        rag_chain = create_rag_chain(retriever, llm)

        logger.info(f"Invoking RAG chain with question: '{question}'")
        answer = rag_chain.invoke(question)

        print("\n--- Answer ---")
        print(answer)
        print("--- End of Answer ---")


if __name__ == "__main__":
    main()
