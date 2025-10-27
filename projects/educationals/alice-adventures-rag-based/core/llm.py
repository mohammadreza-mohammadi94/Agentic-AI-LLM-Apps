"""Language model configuration and chain building."""

import os
import logging
from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)


def get_chat_model(
    model_name: str = "gpt-4.1-mini", temperature: float = 0, max_tokens: int = 500
) -> ChatOpenAI:
    """Initialize and return a ChatOpenAI model instance.

    Parameters
    ----------
    model_name: str
        Name of the OpenAI model to use
    temperature: float
        Temperature setting for response generation
    max_tokens: int
        Maximum tokens in the response

    Returns
    -------
    ChatOpenAI
        Configured ChatOpenAI model instance

    Raises
    ------
    ValueError
        If OPENAI_API_KEY environment variable is not set
    """
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    model = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    logger.info(f"Chat Model Loaded: {model.model_name}")
    return model


def format_docs(docs: List[Document]) -> str:
    """Format retrieved documents into a single string.

    Parameters
    ----------
    docs: List[Document]
        Retrieved documents to format

    Returns
    -------
    str
        Formatted document string
    """
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(retriever, llm) -> Runnable:
    """Create a RAG chain combining retrieval and generation.

    Parameters
    ----------
    retriever
        Document retriever instance
    llm
        Language model instance

    Returns
    -------
    Runnable
        Complete RAG chain that can be invoked with questions
    """
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the user's question based *only* on the following context.
        If the context does not contain the answer, state that you don't know.

        Context:
        {context}

        Question:
        {question}
    """
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
