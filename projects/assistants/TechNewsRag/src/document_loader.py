"""
Document Loader Module

This module is responsible for loading documents from various sources, such as web pages.
It includes functionality to tag documents with metadata, such as their source, to
facilitate filtering and tracking during the RAG process.
"""

import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader

# Setup logging
logger = logging.getLogger(__name__)

def load_and_tag_articles(articles: dict) -> List[Document]:
    """
    Loads articles from a dictionary of sources and URLs,
    and tags each document with its source.

    Args:
        articles (dict): A dictionary where keys are source names
                         and values are article URLs.

    Returns:
        List[Document]: A list of all loaded documents with metadata.
    """
    all_documents = []
    logger.info("Starting to load and tag articles...")
    for source, url in articles.items():
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()

            for doc in documents:
                doc.metadata["source"] = source

            all_documents.extend(documents)
            logger.info(f"Successfully loaded article from {source}")
        except Exception as e:
            logger.error(f"Failed to load article from {source}: {str(e)}")

    logger.info(f"Total documents loaded: {len(all_documents)}")
    return all_documents