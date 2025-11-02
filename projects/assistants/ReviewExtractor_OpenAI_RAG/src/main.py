"""
This script provides a comprehensive solution for analyzing movie reviews using a Retrieval-Augmented Generation (RAG) model.
It leverages various components from the LangChain library to build a sophisticated pipeline that can process a dataset of reviews,
embed them into a vector space, and then use a language model to perform structured analysis on the reviews based on user queries.

The script is organized into several key functions:
- Loading and preprocessing of review data from a CSV file.
- Splitting the review documents into manageable chunks for processing.
- Initializing a sentence-transformer-based embedding model for semantic representation.
- Creating and managing a FAISS vector store for efficient similarity searches.
- Setting up a connection to a large language model (LLM) via an API.
- Constructing a RAG chain that combines retrieval and generation to produce structured output.
- A main execution block that orchestrates the entire process and provides an interactive command-line interface for users.

The core of the script is the RAG chain, which is designed to extract specific, structured information from a movie review.
This is achieved by using a PydanticOutputParser, which ensures that the LLM's output conforms to a predefined data schema.
This structured approach allows for reliable and consistent analysis of the reviews, making the output suitable for further processing or display.

The script is designed to be run from the command line and provides an interactive loop where users can enter queries to find and analyze reviews.
It includes detailed logging to monitor the progress and troubleshoot any issues that may arise.
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import List
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable

from schema import ReviewAnalysis

# Config logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="logs.log",
)


def load_csv_file(file_path: str) -> List[Document]:
    """
    Loads documents from a CSV file, handling both absolute and relative file paths.

    This function is responsible for loading the raw data from a specified CSV file.
    It is designed to be flexible with file paths, automatically resolving relative paths
    based on the script's location. The function uses the CSVLoader from the langchain_community,
    which is configured to treat the "review" column as the main content of the documents.
    To manage memory and processing time, the function currently loads a subset of the total documents.

    Args:
        file_path (str): The path to the CSV file. This can be an absolute path or a relative path.
                         If relative, it is resolved with respect to the script's directory.

    Returns:
        List[Document]: A list of Document objects, where each object represents a review.
                        The list is truncated to the first 1000 documents to ensure efficient processing.
                        Returns an empty list if an error occurs during file loading.
    """
    if not os.path.isabs(file_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_path)

    logging.info(f"=== Loading Documents from {file_path} ===")
    try:
        loader = CSVLoader(
            file_path=file_path,
            source_column="review",
        )
        documents = loader.load()
        docs = documents[:1000]
        logging.info(f"Loaded {len(docs)} documents.\n")
        return docs
    except Exception as e:
        logging.error(f"Error loading CSV file: {e}")
        return []


def inspect_documents(documents: List[Document]):
    """
    Prints the details of the first and last documents in a list
    to help verify their content and metadata.

    This utility function is useful for debugging and ensuring that the data loading
    process has worked as expected. It provides a quick snapshot of the loaded data
    by displaying the initial content and metadata of the first and last documents
    in the provided list. This helps in verifying that the fields are correctly parsed
    and the content is as expected.

    Args:
        documents (List[Document]): A list of Document objects to be inspected.
                                   The function will print details for the first
                                   and last elements of this list.
    """
    if not documents:
        print("The document list is empty. Nothing to inspect.")
        return

    print("=== [INSPECT] First Document Sample ===\n")
    first_doc = documents[0]

    print(f"Content (first 100 chars): \n'{first_doc.page_content[:100]}...'")

    # Print the metadata dictionary
    print(f"\nMetadata: \n{first_doc.metadata}\n\n")

    if len(documents) > 1:
        print(" Last Document Sample ")
        last_doc = documents[-1]

        print(f"Content (first 300 chars): \n'{last_doc.page_content[:300]}...'")
        print(f"\nMetadata: \n{last_doc.metadata}\n\n")


def splitter(documents: List[Document]) -> List[Document]:
    """
        Splits a list of documents into smaller chunks for easier processing by the language model.

        This function uses a RecursiveCharacterTextSplitter to divide the documents into
        chunks of a specified size with some overlap. This is a crucial step in preparing
    n    the data for the RAG model, as it allows the model to process long documents
        that would otherwise exceed its context window. The splitter is configured to
        respect natural text boundaries like paragraphs and sentences, which helps in
        maintaining the semantic integrity of the chunks.

        Args:
            documents (List[Document]): The list of Document objects to be split.

        Returns:
            List[Document]: A new list of Document objects, where each object is a chunk
                            of the original documents. Returns an empty list if an error
                            occurs during the splitting process.
    """
    logging.info("=== Splitting Documents ===")
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=250,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = text_splitter.split_documents(documents)
        logging.info(f"Created {len(chunks)} chunks.\n")
        return chunks
    except Exception as e:
        logging.error(f"Error splitting documents: {e}")
        return []


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Initializes and returns a HuggingFace embedding model for converting text to vectors.

    This function sets up the embedding model that will be used to create numerical
    representations of the text chunks. It uses the "BAAI/bge-base-en-v1.5" model,
    a well-regarded sentence-transformer model. The function configures the model
    to run on the CPU and to normalize the embeddings, which is a common practice
    for improving the performance of similarity searches.

    Returns:
        HuggingFaceEmbeddings: An instance of the HuggingFaceEmbeddings class,
                               ready to be used for embedding text. Returns an
                               empty list if an error occurs during initialization.
    """
    logging.info("=== Initializing Embedding Model ===")
    try:
        MODEL_NAME = "BAAI/bge-base-en-v1.5"
        embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_NAME,
            model_kwargs={"device": "cuda"},
            encode_kwargs={"normalize_embeddings": True},
        )
        logging.info(f"Embedding model: '{MODEL_NAME}' initialized.\n")
        return embeddings
    except Exception as e:
        logging.error(f"Error initializing embeddings: {e}")
        return []


def get_vector_store(
    chunks: List[Document], embeddings: HuggingFaceEmbeddings
) -> FAISS:
    """
    Creates or loads a FAISS vector store for efficient similarity searches.

    This function is responsible for managing the vector store, which is a critical
    component of the RAG pipeline. It first checks if a pre-existing vector store
    is available at a specified directory. If so, it loads it to save time on
    re-computation. If not, it creates a new vector store from the provided document
    chunks and the embedding model. The newly created store is then saved to disk
    for future use.

    Args:
        chunks (List[Document]): The list of document chunks to be stored in the
                                 vector store.
        embeddings (HuggingFaceEmbeddings): The embedding model to be used for
                                            converting the chunks to vectors.

    Returns:
        FAISS: An instance of the FAISS vector store, either loaded from disk or
               newly created. Returns None if an error occurs.
    """
    logging.info("=== Storing Chunks in Vector Store ===")
    persist_directory = os.path.dirname(__file__) + "/faiss_db"

    if os.path.exists(persist_directory):
        logging.info(f"Loading existing vector store from '{persist_directory}'")
        try:
            vectorstore = FAISS.load_local(
                folder_path=persist_directory,
                embeddings=embeddings,
                allow_dangerous_deserialization=True,
            )
            logging.info(f"Loaded existing vector store from '{persist_directory}'")
            return vectorstore
        except Exception as e:
            logging.error(f"Error loading existing vector store: {e}")

    logging.info("Creating a new vectorstore...")
    vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
    vectorstore.save_local(persist_directory)
    logging.info(f"Vectorestore create in persisted to '{persist_directory}'.\n")
    return vectorstore


def get_llm() -> ChatOpenAI:
    """
    Initializes and returns a ChatOpenAI language model instance.

    This function is responsible for setting up the connection to the language model
    that will be used for the generation part of the RAG pipeline. It loads the
    necessary API keys from the environment and initializes the ChatOpenAI model
    with a specific model name. This function is a prerequisite for creating the
    RAG chain, as it provides the generative capabilities.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI class, configured and ready to be
                    used. Returns an empty list if an error occurs during initialization.
    """
    logging.info("=== Initializing LLM ===")
    load_dotenv()
    try:
        llm = ChatOpenAI(
            model="gpt-4.1-mini",
        )
        logging.info(f"LLM initialized: {llm.model_name}\n")
        return llm
    except Exception as e:
        logging.error(f"Error occured: {e}")
        return []


def create_structured_rag_chain(retriever, llm: ChatOpenAI) -> Runnable:
    """
    Creates a RAG chain that extracts structured information from a document.

    This chain uses a PydanticOutputParser to force the LLM to return a JSON
    object that conforms to the specified ReviewAnalysis schema.

    Args:
        retriever: The retriever instance for fetching relevant reviews.
        llm: The initialized language model.

    Returns:
        A runnable chain that takes a user query, finds a relevant review,
        analyzes it, and returns a ReviewAnalysis Pydantic object.
    """
    logging.info("=== Creating Structured RAG Chain with Pydantic Parser ===")
    pydantic_parser = PydanticOutputParser(pydantic_object=ReviewAnalysis)
    prompt_template = """
            You are an expert AI assistant specialized in analyzing user reviews for movies.
            Your task is to analyze the single user review provided in the context below.

            Based *only* on the text of this review, extract the requested information and format your response according to the provided instructions.

            {format_instructions}

            Here is the user review you need to analyze:
            ---
            CONTEXT:
            {context}
            ---
            """
    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={
            "format_instructions": pydantic_parser.get_format_instructions()
        },
    )

    def format_docs(docs: List[Document]) -> str:
        if not docs:
            return "No review Found."
        return docs[0].page_content

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | pydantic_parser
    )
    logging.info("Rag Chain Created Successfully.")
    return rag_chain


def main():
    """
    Main function to run the review analysis pipeline.

    This function orchestrates the entire process of loading data, building the RAG chain,
    and interacting with the user. It serves as the entry point of the script and ties
    together all the different components. The function sets up an interactive loop
    that allows users to repeatedly query the system to get analyses of movie reviews.
    """
    # Load documents from the specified CSV file
    documents = load_csv_file("../data/IMDB Dataset.csv")
    # Inspect the loaded documents to ensure they are correct
    sample_docs = inspect_documents(documents)
    # Split the documents into smaller, more manageable chunks
    chunks = splitter(documents)
    # Initialize the embedding model for vectorization
    embeddings = get_embedding_model()
    # Create or load the FAISS vector store
    vector_store = get_vector_store(chunks, embeddings)
    # Create a retriever from the vector store to fetch relevant documents
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    # Initialize the language model
    llm = get_llm()
    # Create the structured RAG chain for analysis
    rag_chain = create_structured_rag_chain(retriever, llm)

    # Start an interactive loop for user queries
    while True:
        user_query = input(
            "\nEnter a topic to find and analyze a review (e.g., 'a slow and boring movie'): \n \
            (Enter 'quit' to exit)\n"
        )
        if user_query.lower() in ["exit", "quit"]:
            logging.info("User entered 'quit'. Exiting program.")
            print("Exiting program. Goodbye!")
            break

        # Invoke the RAG chain with the user's query
        analysis_result: ReviewAnalysis = rag_chain.invoke(user_query)

        # Print the structured analysis result
        print("\n--- Review Analysis Result ---")
        print(f"Sentiment: {analysis_result.sentiment}")
        print(f"Summary: {analysis_result.summary}")
        print(f"Key Themes: {analysis_result.key_themes}")
        print(f"Predicted Rating: {analysis_result.rating_prediction}")
        print(f"Is a Recommendation: {analysis_result.is_recommendation}")


if __name__ == "__main__":
    main()
