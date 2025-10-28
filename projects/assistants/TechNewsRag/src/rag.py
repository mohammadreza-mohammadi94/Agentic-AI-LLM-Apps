"""
RAG Chain Module

This module defines the core logic of the RAG (Retrieval-Augmented Generation) chain.
It combines a retriever and a language model to answer questions based on retrieved
documents. The module includes a prompt template and a function to format documents
for the language model.
"""

from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def create_rag_chain(retriever, llm) -> Runnable:
    """
    Create a RAG chain combining retrieval and generation.

    Parameters
    ----------
    retriever
        Document retriever instance
    llm
        Language model instance

    Returns
    -------
    Runnable
    """
    prompt = ChatPromptTemplate.from_template(
        """
            You are an intelligent assistant. Answer the user's question based only on the provided context.
            If the answer is not in the context, say that you cannot find the answer in the provided sources.

            Context:
            {context}

            Question:
            {question}
            """
    )

    def format_docs(docs: List[Document]) -> str:
        return "\n\n".join(
            f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
            for doc in docs
        )

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
