# ArxivHybridSearch

## Overview

ArxivHybridSearch is a Retrieval-Augmented Generation (RAG) project that uses a hybrid search approach to answer questions about AI research papers. It combines the strengths of both dense (FAISS) and sparse (BM25) retrieval methods to provide more accurate and relevant results from a curated collection of scientific documents.

This project is designed to serve as an intelligent AI research assistant, allowing users to ask complex questions and receive synthesized answers based on the provided papers.

## Features

- **Hybrid Search:** Utilizes an ensemble of FAISS (for semantic search) and BM25 (for keyword-based search) to retrieve the most relevant document chunks.
- **RAG Pipeline:** Implements a complete RAG pipeline for question-answering on a custom dataset of research papers.
- **Metadata Enrichment:** Enriches documents with metadata (title, authors, year) to provide more context and enable more informative answers.
- **OpenAI Integration:** Uses OpenAI's GPT models to generate fluent, context-aware answers based on the retrieved information.
- **Hugging Face Embeddings:** Leverages state-of-the-art sentence transformers from Hugging Face for creating high-quality document embeddings.

## How it Works

The system follows these steps to answer a user's question:

1.  **Document Loading:** Loads PDF research papers from the `docs` directory.
2.  **Metadata Enrichment:** Associates each document with its corresponding metadata (title, authors, year) from the `metadata.py` file.
3.  **Text Splitting:** Splits the documents into smaller, overlapping chunks to prepare them for retrieval.
4.  **Embedding and Indexing:**
    -   **Dense Retrieval:** Creates vector embeddings for each chunk using a Hugging Face model and stores them in a FAISS vector store.
    -   **Sparse Retrieval:** Creates a keyword-based index using BM25.
5.  **Hybrid Retrieval:** An `EnsembleRetriever` combines the results from both the FAISS and BM25 retrievers to get a balanced set of relevant chunks.
6.  **Answer Generation:**
    -   The user's question is sent to the `EnsembleRetriever` to find the most relevant document chunks.
    -   The retrieved chunks, along with the user's question, are formatted into a detailed prompt.
    -   The prompt is sent to an OpenAI LLM, which generates a comprehensive answer, citing the sources of its information.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd ArxivHybridSearch
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your OpenAI API key:**
    -   Create a `.env` file in the project's root directory.
    -   Add your OpenAI API key to the `.env` file:
        ```
        OPENAI_API_KEY="your-api-key"
        ```

## Usage

1.  **Add your documents:** Place your PDF research papers in the `docs` directory.

2.  **Update metadata:** Open `src/metadata.py` and add the corresponding metadata for each of your papers. The dictionary key should match the filename of the PDF.

3.  **Run the application:**
    ```bash
    python src/main.py
    ```

4.  The script will build the vector store and enter an interactive loop where you can ask questions about the research papers.

### Example Session

Here is an example of what a session with the AI research assistant looks like:

```
Your Question: Find papers about sequence transduction models written by Sutskever or Vaswani
2025-11-02 20:04:17,434 - INFO - Invoking RAG chain with question: 'Find papers about sequence transduction models written by Sutskever or Vaswani'

Thinking...
2025-11-02 20:04:25,271 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"

--- AI Research Assistant's Answer ---
Two relevant papers about sequence transduction models written by Sutskever or Vaswani are:

1. **"Sequence to Sequence Learning with Neural Networks"** by Ilya Sutskever, Oriol Vinyals, and Quoc V. Le (2014). This paper introduces a general end-to-end approach for sequence learning using multilayered LSTMs for encoding and decoding sequences, demonstrating strong performance on machine translation tasks (Source: Sequence to Sequence Learning with Neural Networks).

2. **"Attention Is All You Need"** by Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin (2017). This work proposes the Transformer architecture, a sequence transduction model based solely on attention mechanisms without recurrent or convolutional layers. It achieves state-of-the-art results in machine translation while offering faster training and better parallelization (Source: Attention Is All You Need).
--- End of Answer ---

Your Question: Which papers from 2017 or 2018 discuss Transformers?
2025-11-02 20:04:41,093 - INFO - Invoking RAG chain with question: 'Which papers from 2017 or 2018 discuss Transformers?'

Thinking...
2025-11-02 20:04:46,766 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"

--- AI Research Assistant's Answer ---
The papers from 2017 or 2018 that discuss Transformers are:

1. **"Attention Is All You Need" (2017)** — This foundational paper introduced the Transformer architecture, proposing to replace recurrent and convolutional networks with self-attention mechanisms for sequence modeling tasks (Source: Attention Is All You Need).

2. **"BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" (2018)** — This paper builds on the Transformer architecture by pre-training deep bidirectional Transformers to improve natural language understanding tasks (Source: BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding).
--- End of Answer ---
```
