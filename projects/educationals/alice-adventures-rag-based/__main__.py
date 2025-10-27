"""Main script demonstrating the RAG system."""

import logging
from pathlib import Path
from dotenv import load_dotenv

from config.settings import load_config
from core.document_loader import load_documents, chunk_documents
from core.vectorstore import create_embeddings, build_vectorstore
from core.llm import get_chat_model, create_rag_chain

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Run the RAG pipeline with example questions."""
    logger.info("=" * 50)
    logger.info("Simple RAG System Based on LangChain and FAISS")
    logger.info("Alice's Adventures in Wonderland by Lewis Carroll")
    logger.info("=" * 50)

    try:
        # Load environment variables and configuration
        load_dotenv()
        config = load_config()

        # Load and process documents
        docs = load_documents(config.data_dir)
        chunks = chunk_documents(
            docs, chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap
        )

        # Create embeddings and vectorstore
        embedding_model = create_embeddings(config.embedding_model)
        vectorstore = build_vectorstore(chunks, embedding_model, config.vectorstore_dir)

        # Set up retriever
        retriever = vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}
        )

        # Initialize LLM and create chain
        llm = get_chat_model(
            model_name=config.llm_model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
        rag_chain = create_rag_chain(retriever, llm)

        # Test the system
        logger.info("\nQuerying the RAG system...")

        test_questions = [
            "Who did Alice follow down the rabbit-hole?",
            "What is written on the cake that Alice finds?",
            "Describe the Cheshire Cat.",
            "What is the capital of France?",  # Answer is NOT in the text
        ]

        for i, question in enumerate(test_questions, 1):
            logger.info(f"\n--- Test Question {i} ---")
            logger.info(f"Question: {question}")
            answer = rag_chain.invoke(question)
            logger.info(f"Answer: {answer}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise

    logger.info("\nRAG pipeline execution finished.")


if __name__ == "__main__":
    main()
