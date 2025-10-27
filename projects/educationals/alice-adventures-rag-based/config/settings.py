"""Configuration settings for the RAG system."""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class RAGConfig:
    """Configuration for the RAG system.

    Attributes
    ----------
    data_dir: Path
        Directory containing the source documents
    vectorstore_dir: Path
        Directory to save the FAISS index
    embedding_model: str
        Name of the HuggingFace model to use for embeddings
    llm_model: str
        Name of the OpenAI model to use
    chunk_size: int
        Size of document chunks
    chunk_overlap: int
        Overlap between chunks
    temperature: float
        LLM temperature setting
    max_tokens: int
        Maximum tokens in LLM response
    """

    data_dir: Path
    vectorstore_dir: Path
    embedding_model: str = "sentence-transformers/all-distilroberta-v1"
    llm_model: str = "gpt-4.1-mini"
    chunk_size: int = 1000
    chunk_overlap: int = 250
    temperature: float = 0
    max_tokens: int = 500


def load_config(
    data_dir: Optional[Path] = None, vectorstore_dir: Optional[Path] = None
) -> RAGConfig:
    """Create a configuration with optional custom paths.

    Parameters
    ----------
    data_dir: Optional[Path]
        Override the default data directory
    vectorstore_dir: Optional[Path]
        Override the default vectorstore directory

    Returns
    -------
    RAGConfig
        Configuration instance
    """
    base_dir = Path(__file__).resolve().parent.parent

    return RAGConfig(
        data_dir=data_dir or base_dir / "data",
        vectorstore_dir=vectorstore_dir or base_dir.parent / "faiss_alice_rag",
    )
