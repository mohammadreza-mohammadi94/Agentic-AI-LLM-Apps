# Alice RAG

A Retrieval-Augmented Generation (RAG) system for querying Alice's Adventures in Wonderland using LangChain and FAISS.

## Features

- Document loading and chunking with LangChain
- Semantic search using FAISS and sentence-transformers
- RAG implementation with OpenAI's GPT models
- Configurable parameters for embeddings, chunking, and LLM

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install the package:

```bash
pip install -e .
```

## Configuration

1. Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your-key-here
```

2. Place your text files in the `alice_rag/data` directory.

## Usage

Run the example script:

```bash
python -m alice_rag
```

Or use the components in your own code:

```python
from alice_rag.config.settings import load_config
from alice_rag.core.document_loader import load_documents
# ... import other components as needed

# Load configuration
config = load_config()

# Process documents
docs = load_documents(config.data_dir)
# ... continue with your RAG pipeline
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Format code:

```bash
black .
ruff check --fix .
```
