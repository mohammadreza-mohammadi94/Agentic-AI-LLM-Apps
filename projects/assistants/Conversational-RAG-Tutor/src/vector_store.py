"""
Module for managing the FAISS vector store.

This includes creating the vector store from documents, saving it to disk for
persistence, and loading it if it already exists to speed up startup time.
"""

import os
import logging
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import Optional
from data_loader import get_langchain_documents
import config

# initialize logger
logger = logging.getLogger(__name__)


def get_vector_store() -> Optional[FAISS]:
    """
    Creates or loads the FAISS vector store.

    This function checks if a local FAISS index already exists at the path
    defined in the config. If it does, it loads the index. If not, it creates
    a new index by fetching documents, splitting them into chunks, and
    embedding them. The new index is then saved to disk.

    Returns:
        Optional[FAISS]: The initialized FAISS vector store instance, or None if
                         creation fails due to a lack of documents.
    """
    # Initialize embedding model
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
    logger.info(f"Embedding Model Loaded: {embeddings.model_name}")

    # Check if the vectorstore already exits
    if os.path.exists(config.VECTORSTORE_DIR):
        logger.info(f"Loading existing vectorstore from: {config.VECTORSTORE_DIR}")
        try:
            return FAISS.load_local(
                config.VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True
            )
        except Exception as e:
            logger.error(f"Error loading vectorstore: {e}")

    logger.info("No existing vectorstore found, creating a new one...")

    # load the source documents from the web
    documents = get_langchain_documents()

    if not documents:
        logger.critical(
            "Failed to create vector store because no documents were loaded."
        )
        return None

    # Split the documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # Create FAISS vectorstore
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
        normalize_L2=True,
    )
    # Save vectorstore
    vector_store.save_local(config.VECTORSTORE_DIR)
    logger.info(f"Vectorstore saved at: {config.VECTORSTORE_DIR}")

    return vector_store
