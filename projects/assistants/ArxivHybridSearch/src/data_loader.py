# src/data_loader.py
"""
Module responsible for loading, enriching, and splitting documents.
"""
import os
import logging
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from metadata import PAPERS_METADATA
import config

logger = logging.getLogger(__name__)


def load_and_enrich_docs() -> List[Document]:
    """
    Loads PDF documents and enriches them with custom metadata.
    """
    directory_path = str(config.DOCS_PATH.resolve())
    logger.info(f"Loading documents from {directory_path}...")

    loader = DirectoryLoader(path=directory_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} pages from all documents.")

    logger.info("Adding custom metadata to documents...")
    enriched_documents = []
    for doc in documents:
        source_path = doc.metadata.get("source", "")
        filename = os.path.basename(source_path)
        if filename in PAPERS_METADATA:
            custom_metadata = PAPERS_METADATA[filename]
            doc.metadata.update(custom_metadata)
            enriched_documents.append(doc)
        else:
            logger.warning(f"Metadata not found for file: {filename}. Skipping.")

    logger.info(f"Successfully enriched {len(enriched_documents)} pages.")
    return enriched_documents


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Splits the loaded documents into smaller chunks.
    """
    logger.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=450,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} chunks.")
    return chunks
