# chain.py

"""
Module for building the conversational RAG (Retrieval-Augmented Generation) chain.

This module defines the logic for creating a sophisticated chain that can
understand conversational context by reformulating questions based on chat history.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS


def create_conversational_rag_chain(retriever: FAISS.as_retriever, llm: ChatOpenAI):
    """
    Creates and returns the complete conversational RAG chain.

    The chain is composed of two main parts:
    1. A history-aware retriever that reformulates the user's latest question
       to be a standalone question based on the chat history.
    2. A question-answering chain that uses the retrieved context to generate
       a final answer.

    Args:
        retriever: The vector store retriever for fetching relevant documents.
        llm: The language model to power the chain.

    Returns:
        A runnable chain that expects a dictionary with "input" and "chat_history"
        and returns a dictionary with the "answer".
    """
    # This prompt helps the LLM to rephrase the user's follow-up question
    # into a self-contained question.
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is.",
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # This is the prompt for the final answer generation step.
    # It MUST contain a 'context' variable, as expected by 'create_stuff_documents_chain'.
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are an expert AI assistant for LangChain documentation. "
                    "Answer the user's questions concisely and helpfully based on the provided context. "
                    "If the context doesn't contain the answer, state that clearly.\n\n"
                    "Here is the relevant context:\n{context}"
                ),
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # This chain combines the documents into a single string ("stuffs" them)
    # and passes them to the LLM via the 'context' variable in the prompt.
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # --- Part 3: Final Combined Chain (No changes here) ---
    # This is the final chain that orchestrates the entire process.
    # It first calls the history_aware_retriever and then the question_answer_chain.
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain
