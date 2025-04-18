"""
Sentiment Analysis Chatbot with Dynamic Few-Shot Prompting

This module implements a sentiment analysis chatbot using LangChain, Cohere, and Chroma.
It dynamically selects relevant examples based on semantic similarity for few-shot prompting
and provides a Streamlit UI for user interaction.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
import chromadb


# Setup API Key
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not found in .env file. Please set it.")
os.environ["COHERE_API_KEY"] = COHERE_API_KEY


# Load Examples
def load_examples():
    """
    Load a predefined list of sentiment analysis examples.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing input sentences and their sentiment labels.
    """
    # list of examples
    return [
        {"input": "This movie was absolutely fantastic!", "output": "Positive"},
        {"input": "The food was terrible and overpriced.", "output": "Negative"},
        {"input": "The weather is okay today.", "output": "Neutral"},
        {"input": "I had an amazing time at the concert!", "output": "Positive"},
        {"input": "The product broke after one use.", "output": "Negative"},
        {"input": "The book was interesting but average.", "output": "Neutral"},
        {"input": "I love this restaurant's atmosphere!", "output": "Positive"},
        {"input": "The service was slow and rude.", "output": "Negative"},
        {"input": "The presentation was neither good nor bad.", "output": "Neutral"},
        {"input": "This is the best vacation I've ever had!", "output": "Positive"}
    ]


def create_example_selector(examples):
    """
    Create a semantic similarity example selector using Cohere embeddings and Chroma.

    Args:
        examples (List[Dict[str, str]]): List of example dictionaries with input and output.

    Returns:
        SemanticSimilarityExampleSelector: Configured example selector for dynamic example selection.
    """
    # define cohere Embeddings
    embeddings = CohereEmbeddings(model="embed-english-v3.0")
    
    # chroma_db with persist directory
    persist_directory = "./chromaDB"
    
    # Define settings for client
    chroma_client = chromadb.PersistentClient(path=persist_directory)

    # build chroma db
    vectorstore = Chroma(
        collection_name="sentiment_examples",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    
    # define selector
    selector = SemanticSimilarityExampleSelector.from_examples(
        examples=examples,
        embeddings=embeddings,
        vectorstore_cls=Chroma,
        k=3,  # انتخاب 3 مثال نزدیک‌ترین از نظر معنایی
        input_keys=["input"]  # کلیدهایی که برای تولید متن استفاده می‌شن
    )
    return selector


def create_prompt_template():
    """
    Create a chat prompt template with dynamic few-shot examples.

    Returns:
        ChatPromptTemplate: Configured prompt template with system message and few-shot examples.
    """
    # Define prompt template
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "Analyze the sentiment of this sentence: {input}"),
        ("assistant", "Sentiment: {output}")
    ])
    # Load examples
    examples = load_examples()
    # Create example selector
    example_selector = create_example_selector(examples)
    # Creating dynamic few-shot promp
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        examples=examples,
        example_prompt=example_prompt
    )

    # Final prompt with messages & dynamic examples
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a sentiment analysis expert. Provide concise and accurate sentiment labels (Positive, Negative, Neutral)."),
        few_shot_prompt,
        ("human", "Analyze the sentiment of this sentence: {input}"),
    ])

    return final_prompt


def build_chain():
    """
    Build a LangChain runnable chain for sentiment analysis.

    Returns:
        RunnableSequence: A chain combining the prompt template and Cohere chat model.
    """
    # Define chat model
    chat_model = ChatCohere(model="command-r-plus", temperature=0.7)
    # create prompt
    prompt = create_prompt_template()
    chain = prompt | chat_model
    return chain

def analyze_sentiment(sentence):
    """
    Analyze the sentiment of a given sentence using the chatbot.

    Args:
        sentence (str): The input sentence to analyze.

    Returns:
        str: The predicted sentiment label (Positive, Negative, Neutral).

    Raises:
        Exception: If the chain execution fails.
    """
    chain = build_chain()
    try:
        # Run chain with user input
        result = chain.invoke({"input": sentence})
        return result.content
    except Exception as e:
        return f"Error: {e}"
    
def main():
    """
    Main function to run the Streamlit web interface for the sentiment analysis chatbot.
    """
    # Set page title
    st.title("Sentiment Analysis Chatbot")
    st.markdown("""
        This chatbot analyzes the sentiment of English sentences using dynamic few-shot prompting.
        Enter a sentence below to get its sentiment (Positive, Negative, or Neutral).
    """)

    # User input
    sentence = st.text_input("Enter a sentence:", placeholder="e.g., This movie was great!")
    
    if sentence:
        # Button to run sentiment analysis
        if st.button("Analyze Sentiment"):
            with st.spinner("Analyzing..."):
                result = analyze_sentiment(sentence)
                # show results
                st.write(f"**Sentiment**: {result}")
    
    # show some examples for user.
    st.markdown("### Example Sentences")
    st.write("- Positive: 'I loved this restaurant!' → Sentiment: Positive")
    st.write("- Negative: 'The service was awful.' → Sentiment: Negative")
    st.write("- Neutral: 'The weather is okay.' → Sentiment: Neutral")

if __name__ == "__main__":
    main()