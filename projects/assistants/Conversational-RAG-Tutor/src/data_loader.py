"""
Module for loading and preparing the source documents for the RAG system.

This module fetches content from the official LangChain documentation website
and tags each document with relevant metadata.
"""

from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from typing import List, Dict
import logging

# initialize logger
logger = logging.getLogger(__name__)

# By loading the whole page, we get all the context in one go.
LANGCHAIN_CONCEPTS_URL = "https://python.langchain.com/v0.2/docs/concepts/"


def get_langchain_documents() -> List[Document]:
    """
    Loads the main "Concepts" page from the LangChain documentation website.

    This function loads the entire content of the specified URL and tags it
    with a general topic and the source URL for citation.

    Returns:
        List[Document]: A list containing the loaded document, or an empty list
                        if loading fails.
    """
    all_documents = []
    logger.info(f"Loading document from LangChain URL: {LANGCHAIN_CONCEPTS_URL}")

    try:
        # Initialize a loader for the URL
        loader = WebBaseLoader(LANGCHAIN_CONCEPTS_URL)
        # Load the document content
        documents = loader.load()

        # Add metadata to the loaded document(s)
        for doc in documents:
            doc.metadata["topic"] = "LangChain Concepts"
            doc.metadata["source"] = LANGCHAIN_CONCEPTS_URL

        all_documents.extend(documents)
        logger.info(f"Successfully loaded {len(all_documents)} document(s).")

    except Exception as e:
        # Log an error if the URL fails to load
        logger.error(
            f"Failed to load documentation from {LANGCHAIN_CONCEPTS_URL}. Error: {e}"
        )

    if not all_documents:
        logger.warning("No documents were loaded. The knowledge base will be empty.")

    return all_documents
