"""
Retriever Module

This module is responsible for creating a retriever from a FAISS vector store.
The retriever is used to fetch relevant documents from the vector store based on
a user's query. It can be configured with parameters such as the number of
documents to retrieve and filtering options.
"""

import logging
from langchain_community.vectorstores import FAISS

# Setup logging
logger = logging.getLogger(__name__)

def create_retriever(vector_store: FAISS, selected_source: str, k: int = 4):
    """
    Creates a retriever from the FAISS vector store.
    Args:
        vector_store: The FAISS vector store.
        selected_source (str): The source to filter by.
        k (int): The number of top documents to retrieve.
    Returns:
        Retriever: The configured retriever.
    """
    retriever = vector_store.as_retriever(
        search_kwargs={"k": k, "filter": {"source": selected_source}}
    )
    logger.info(f"Retriever created with top {k} documents to retrieve.")
    return retriever