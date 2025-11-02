# src/retrievers.py
"""
Module for creating and managing all retriever components.
"""
import os
import logging
from typing import List

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

import config

logger = logging.getLogger(__name__)


def get_embedding_model() -> HuggingFaceEmbeddings:
    """Initializes and returns the embedding model."""
    logger.info("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    logger.info(f"Embedding model '{config.EMBEDDING_MODEL_NAME}' initialized.")
    return embeddings


def get_faiss_vector_store(
    chunks: List[Document], embeddings: HuggingFaceEmbeddings
) -> FAISS:
    """Loads a FAISS vector store from disk or creates a new one."""
    persist_directory = str(config.VECTOR_STORE_PATH.resolve())
    logger.info(f"Accessing vector store at: {persist_directory}")

    if os.path.exists(persist_directory):
        logger.info("Loading existing FAISS vector store...")
        return FAISS.load_local(
            persist_directory, embeddings, allow_dangerous_deserialization=True
        )

    logger.info("Creating a new FAISS vector store...")
    vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
    vectorstore.save_local(persist_directory)
    logger.info(f"Vector store created and persisted.")
    return vectorstore


def get_bm25_retriever(chunks: List[Document]) -> BM25Retriever:
    """Creates a BM25Retriever from document chunks."""
    logger.info("Creating BM25 retriever...")
    return BM25Retriever.from_documents(chunks)


def get_ensemble_retriever(faiss_retriever, bm25_retriever) -> EnsembleRetriever:
    """Creates an EnsembleRetriever combining keyword and semantic retrievers."""
    logger.info("Creating ensemble retriever...")
    return EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5]
    )
