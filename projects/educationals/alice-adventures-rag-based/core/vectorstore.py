"""Vector store and embedding functionality."""

import logging
from typing import List, Optional
from pathlib import Path
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)


def create_embeddings(model_name: str = "sentence-transformers/all-distilroberta-v1"):
    """Create an embeddings model instance.

    Parameters
    ----------
    model_name: str, optional
        Name of the HuggingFace model to use for embeddings

    Returns
    -------
    HuggingFaceEmbeddings
        The embeddings model instance
    """
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    logger.info(f"Embedding Model Loaded: {embeddings.model_name}")
    return embeddings


def build_vectorstore(
    documents: List[Document], embedding_model, persist_dir: Optional[Path] = None
):
    """Build and optionally persist a FAISS vectorstore.

    Parameters
    ----------
    documents: List[Document]
        Documents to index in the vectorstore
    embedding_model:
        The embeddings model to use
    persist_dir: Optional[Path]
        Directory to save the vectorstore (if None, won't persist)

    Returns
    -------
    FAISS
        The vectorstore instance
    """
    vectorstore = FAISS.from_documents(
        documents=documents, embedding=embedding_model, normalize_L2=True
    )

    if persist_dir:
        vectorstore.save_local(str(persist_dir))
        logger.info(f"Vectorstore saved at: {persist_dir}")

    return vectorstore
