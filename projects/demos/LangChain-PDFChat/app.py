"""
Chat with PDF: A Streamlit-based chatbot that allows users to upload PDF files, extract text,
and ask questions about the content using LangChain and Cohere's LLM and embeddings.

Author: Mohammadreza Mohammadi
Github: mohamamdreza-mohammadi94
"""

#----------------------------------#
# Import Libraries & Setup Project #
#----------------------------------#

# Libs
import streamlit as st
from PyPDF2 import PdfReader
from langchain_cohere import ChatCohere
from langchain.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.callbacks import StdOutCallbackHandler
from langchain_cohere.embeddings import CohereEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Setup API
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not found in .env file. Please set it.")
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

# Setup logging
LOG_FILE = "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Save Path of Logger
        logging.StreamHandler()         # Show logs in console
    ]
)
logger = logging.getLogger(__name__)

#------------------------------#
# Implement App and Streamlit  #
#------------------------------#
def main():
    logger.info("Starting the App...")
    st.header("Chat With PDF💬")
    st.sidebar.title("LLM ChatBot Using LangChain.")
    st.sidebar.markdown(
        '''
        This is an LLM powered chatbot built using:
        - [Streamlit](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/)
        - [Cohere](https://cohere.com/) LLM Model
        '''
    )
    
    # Check API key
    if 'COHERE_API_KEY' not in os.environ:
        logger.error("COHERE_API_KEY not set in environment variables")
        st.error("Please set COHERE_API_KEY in environment variables")
        return
    
    # Upload PDF File
    pdf = st.file_uploader("Upload Your PDF File", type='pdf')

    if pdf is not None:
        logger.info(f"PDF File Uploaded: {pdf.name}")
        try:
            pdf_reader = PdfReader(pdf)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text() or ""  # Handle empty pages
                text += page_text
            if not text.strip():
                logger.error("No text extracted from PDF")
                st.error("No text could be extracted from the PDF. Please check the file.")
                return
            logger.info("PDF Text Extracted Successfully...")

            # Split texts to Chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text=text)
            logger.info(f"Text split into {len(chunks)} chunks...")

            # Vector Store
            store_name = pdf.name[:-4]
            st.write(store_name)
            store_path = f"vector_stores/{store_name}"

            # Creating Embeddings
            embeddings = CohereEmbeddings(model="embed-english-v3.0")
            if os.path.exists(store_path):
                try:
                    VectorStore = FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)
                    st.write('Embeddings Loaded from the Disk')
                    logger.info(f"Vector Store loaded from {store_path}")
                except Exception as e:
                    logger.warning(f"Failed to load Vector Store from {store_path}: {str(e)}. Creating new Vector Store.")
                    VectorStore = FAISS.from_texts(chunks, embeddings)
                    VectorStore.save_local(store_path)
                    st.write('New Embeddings Created due to load failure')
                    logger.info(f"New Vector Store created and saved as {store_path}")
            else:
                VectorStore = FAISS.from_texts(chunks, embeddings)
                os.makedirs("vector_stores", exist_ok=True)
                VectorStore.save_local(store_path)
                st.write("Embeddings Created")
                logger.info(f"Vector Store created and saved as {store_path}")

            # User Questions
            query = st.text_input("Ask Question From Your PDF File")
            if query:
                logger.info(f"User query: {query}")
                try:
                    docs = VectorStore.similarity_search(query=query, k=3)
                    logger.info(f"Retrieved {len(docs)} documents for query")

                    llm = ChatCohere(model="command-r-plus")

                    # Define prompt template
                    prompt = ChatPromptTemplate.from_template(
                        """
                        You are a helpful assistant. Answer the question based on the following context from a PDF document.
                        If the answer is not in the context, say so clearly.
                        Context: {context}
                        Question: {question}
                        Answer:
                        """
                    )

                    # Create stuff documents chain
                    chain = create_stuff_documents_chain(llm, prompt)

                    # Run chain with callbacks
                    response = chain.invoke(
                        {"context": docs, "question": query},
                        config={"callbacks": [StdOutCallbackHandler()]}
                    )
                    st.write(response)
                    logger.info(f"Response generated: {response}")

                except Exception as e:
                    logger.error(f"Error processing query: {str(e)}")
                    st.error(f"An Error Occurred: {str(e)}")

        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            st.error(f"An error occurred while processing the PDF: {str(e)}")

# Run main.py
if __name__ == '__main__':
    main()