"""
Vector Store Module

This module handles the creation and management of the vector store. It includes
functionality for initializing embedding models and creating a FAISS vector store
from document chunks. The vector store is essential for efficient similarity
searches in the RAG pipeline.
"""

import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Setup logging
logger = logging.getLogger(__name__)

def get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Initializes and returns a HuggingFace embedding model.

    Args:
        model_name (str): The name of the HuggingFace model to use.
    Returns:
        HuggingFaceEmbeddings: The initialized embedding model.
    """
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    logger.info(f"Embedding model '{model_name}' initialized.")
    return embeddings

def create_vector_store(
    chunks: List[Document], embedding_model, persist_dir: str = "data/vectorstore"
):
    """
    Creates and persists a FAISS vector store from document chunks.

    Args:
        chunks (List[Document]): The list of document chunks to index.
        embedding_model: The embedding model to use.
        persist_dir (str): Directory to save the vector store.

    Returns:
        FAISS: The created FAISS vector store.
    """
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model,
        normalize_L2=True,
    )
    vector_store.save_local(persist_dir)
    logger.info(f"Vector store created and saved to '{persist_dir}'")
    return vector_store