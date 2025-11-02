# src/main.py
"""
Main entry point for the ArxivHybridSearch application.
This script orchestrates the entire RAG pipeline and handles user interaction.
"""
import logging
from dotenv import load_dotenv

# Local module imports
import config
from data_loader import load_and_enrich_docs, split_documents
from retrievers import (
    get_embedding_model,
    get_faiss_vector_store,
    get_bm25_retriever,
    get_ensemble_retriever,
)
from chain import get_llm, create_rag_chain


def main():
    """Initializes and runs the main interactive loop for the AI assistant."""
    load_dotenv()
    config.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting ArxivHybridSearch application...")

    # Data and Retriever Preparation
    documents = load_and_enrich_docs()
    if not documents:
        logger.critical("No documents loaded. Exiting.")
        return
    chunks = split_documents(documents)
    embeddings = get_embedding_model()

    vector_store = get_faiss_vector_store(chunks, embeddings)
    faiss_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    bm25_retriever = get_bm25_retriever(chunks)
    ensemble_retriever = get_ensemble_retriever(faiss_retriever, bm25_retriever)

    # Chain and LLM Initialization
    llm = get_llm()
    rag_chain = create_rag_chain(ensemble_retriever, llm)

    # Interactive Loop
    print("\n" + "=" * 60)
    print("Welcome to ArxivHybridSearch! Ask questions about AI research papers.")
    print("Type 'exit' or 'quit' to end the session.")
    print("=" * 60)

    while True:
        try:
            user_question = input("\nYour Question: ")
            if user_question.lower() in ["exit", "quit"]:
                logger.info("User requested to exit. Goodbye!")
                break
            if not user_question.strip():
                continue

            logger.info(f"Invoking RAG chain with question: '{user_question}'")
            print("\nThinking...")
            answer = rag_chain.invoke(user_question)
            print("\n--- AI Research Assistant's Answer ---")
            print(answer)
            print("--- End of Answer ---")

        except (KeyboardInterrupt, EOFError):
            logger.info("\nInterrupted by user. Exiting.")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            print("\nAn unexpected error occurred. Please try again.")


if __name__ == "__main__":
    main()
