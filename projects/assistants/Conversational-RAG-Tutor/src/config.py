"""
Central configuration file for the Conversational LangChain Docs Assistant.

This file contains constants for model names, file paths, and other
configuration parameters to make the application easier to manage and modify.
"""

# Model configuration
# define models for embeddings and LM
EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME: str = "gpt-4.1-mini"

# Vectorstore configuration
# define the local path to store FAISS index
VECTORSTORE_DIR: str = "/Conversational-RAG-Tutor/faiss"
