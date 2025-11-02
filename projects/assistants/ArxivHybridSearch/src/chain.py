# src/chain.py
"""
Module for building the LLM and the final RAG chain.
"""
import logging
from typing import List

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import config

logger = logging.getLogger(__name__)


def get_llm() -> ChatOpenAI:
    """Initializes and returns the language model."""
    logger.info("Initializing LLM...")
    llm = ChatOpenAI(model_name=config.LLM_MODEL_NAME, temperature=0)
    logger.info(f"LLM initialized: {llm.model_name}")
    return llm


def create_rag_chain(retriever: Runnable, llm: ChatOpenAI) -> Runnable:
    """Creates the complete RAG chain using LCEL."""
    logger.info("Creating the RAG chain...")

    prompt_template = """
                        You are an expert AI research assistant. Your task is to answer the user's question based on the context provided, which consists of abstracts from scientific papers.

                        Please follow these instructions carefully:
                        1.  Synthesize the information from all provided abstracts to form a comprehensive answer.
                        2.  When you use information from a paper, cite it using its title. For example: "(Source: Attention Is All You Need)".
                        3.  If the provided abstracts do not contain enough information to answer the question, clearly state that the answer cannot be found in the provided sources. Do not use external knowledge.

                        CONTEXT FROM PAPER ABSTRACTS:
                        {context}

                        USER'S QUESTION:
                        {question}

                        YOUR ANSWER:
                        """
    prompt = ChatPromptTemplate.from_template(prompt_template)

    def format_docs(docs: List[Document]) -> str:
        # (The formatting function from the previous answer)
        formatted_docs = []
        for doc in docs:
            header = f"--- Paper Information ---\nTitle: {doc.metadata.get('title', 'N/A')}\n"
            header += f"Authors: {doc.metadata.get('authors', 'N/A')}\n"
            header += f"Year: {doc.metadata.get('year', 'N/A')}\n"
            formatted_docs.append(f"{header}\nAbstract:\n{doc.page_content}")
        return "\n\n".join(formatted_docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    logger.info("RAG chain created successfully.")
    return rag_chain
