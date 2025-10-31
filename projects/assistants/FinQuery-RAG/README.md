# FinQuery-RAG

FinQuery-RAG is a retrieval-augmented generation (RAG) application that allows you to ask questions about financial reports. It uses a language model to understand your questions and retrieves relevant information from a collection of financial documents to provide you with accurate answers.

## Features

- **Load Financial Reports:** Easily load financial reports in PDF format.
- **Document Processing:** Automatically splits large documents into smaller, manageable chunks.
- **Embeddings Generation:** Uses Hugging Face embedding models to create vector representations of the text.
- **Vector Storage:** Stores document embeddings in a Chroma vector store for efficient retrieval.
- **Question Answering:** Leverages a large language model to understand and answer your questions based on the provided documents.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/FinQuery-RAG.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd FinQuery-RAG
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_api_key
    ```

## Usage

1.  Place your financial reports (in PDF format) in the `data` directory.
2.  Run the `main.py` script:
    ```bash
    python src/main.py
    ```
3.  The script will process the documents and create a vector store. You will then be prompted to ask questions about the financial reports.

## Sample Execution

```
==================================================================================
                 Welcome to FinQuery! Ask questions about the financial report.
                 Type 'exit' to quite.
==================================================================================

Your Question: Summarize TESLA business strategy.

Thinking...

2025-11-01 01:00:03,625 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"

=== ANSWER ===

TESLA's business strategy focuses on maintaining and growing the business by sustaining credibility and confidence among customers, suppliers, analysts, investors, ratings agencies, and other stakeholders in its long-term financial viability and business prospects. The company acknowledges challenges such as its limited operating history compared to established competitors, customer unfamiliarity with its products, potential delays in scaling manufacturing, delivery, and service operations, competition, uncertainty regarding the future of electric vehicles and other products, and market expectations of quarterly production and sales performance. TESLA also faces risks related to compliance, residual value, financing, and credit risks connected to its financing programs.

Additionally, Tesla has adopted a patent policy pledging not to initiate lawsuits against parties infringing its patents related to electric vehicles or equipment if such parties act in good faith, encouraging the advancement of a common and rapidly evolving platform for electric vehicles, benefiting Tesla, other companies, and the world.

TESLA's core purpose is to accelerate the world's transition to sustainable energy by addressing both energy generation and consumption. The company designs and manufactures a complete energy and transportation ecosystem. As it expands, Tesla builds each new factory to be more efficient and sustainably designed than the previous one, focusing on per-unit waste reduction, resource consumption (including water and energy), and enhancing sustainability of operations beyond its direct control, including reducing the carbon footprint of its supply chain. Tesla is committed to sourcing responsibly produced materials and requires its suppliers to provide evidence of management systems that support this effort.

=== END OF ANSWER ===
```
