"""
Text Splitter Module

This module provides functionality for splitting large documents into smaller chunks.
This is a crucial step in preparing data for embedding and vector storage, as it
ensures that the text segments are of a manageable size for the language model.
"""

import logging
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Setup logging
logger = logging.getLogger(__name__)

def text_splitter(
    documents: List[Document], chunk_size: int = 500, chunk_overlap: int = 50
) -> List[Document]:
    """
    Splits documents into smaller chunks.

    Args:
        documents (List[Document]): The list of documents to split.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of overlapping characters between chunks.

    Returns:
        List[Document]: A list of chunked documents.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunked_documents = splitter.split_documents(documents)
    logger.info(f"Documents split into {len(chunked_documents)} chunks")
    return chunked_documents