"""Document loading and processing functionality."""

import logging
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def load_documents(data_dir: Path) -> List[Document]:
    """Load all text documents from a directory.

    Parameters
    ----------
    data_dir: Path
        Path to the directory containing `.txt` files.

    Returns
    -------
    List[Document]
        A list of LangChain `Document` objects loaded from the files.

    Raises
    ------
    ValueError
        If the data directory doesn't exist or contains no .txt files
    """
    if not data_dir.exists():
        raise ValueError(f"Data directory not found: {data_dir}")

    # List .txt files before loading
    txt_files = list(data_dir.glob("**/*.txt"))
    if not txt_files:
        raise ValueError(f"No .txt files found in {data_dir}")

    logger.info(f"Found {len(txt_files)} .txt files in {data_dir}")

    loader = DirectoryLoader(
        path=str(data_dir),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    try:
        documents = loader.load()
        logger.info(f"Successfully loaded {len(documents)} documents from {data_dir}")

        if not documents:
            raise ValueError("Documents were loaded but the result is empty")

        return documents
    except Exception as e:
        logger.error(f"Error loading documents from {data_dir}: {str(e)}")
        raise


def chunk_documents(
    documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 250
) -> List[Document]:
    """Split loaded documents into smaller chunks for embedding.

    Parameters
    ----------
    documents: List[Document]
        List of LangChain `Document` instances to split.
    chunk_size: int, optional
        Size of each chunk in characters (default: 1000)
    chunk_overlap: int, optional
        Number of characters of overlap between chunks (default: 250)

    Returns
    -------
    List[Document]
        A list of chunked `Document` objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} chunks")
    return chunks
