# Movie Review Analysis with RAG

This project is a command-line application that uses a Retrieval-Augmented Generation (RAG) model to analyze movie reviews. It leverages the LangChain library to build a pipeline that can process a dataset of reviews, embed them into a vector space, and then use a large language model (LLM) to perform structured analysis on the reviews based on user queries.

## Features

- **Structured Review Analysis**: Extracts sentiment, summary, key themes, predicted rating, and recommendation status from a movie review.
- **RAG Pipeline**: Uses a RAG model to find relevant reviews based on user queries and generate a structured analysis.
- **Interactive CLI**: Allows users to enter queries and receive real-time analysis of movie reviews.
- **Persistent Vector Store**: Uses FAISS to store document embeddings, allowing for faster startup times after the initial setup.
- **Powered by LangChain**: Built using the LangChain library, which simplifies the development of LLM-powered applications.

## Technologies Used

- **Python**: The core programming language for the application.
- **LangChain**: The framework used to build the RAG pipeline.
- **Hugging Face Transformers**: For sentence embeddings (BAAI/bge-base-en-v1.5).
- **FAISS**: For efficient similarity search in the vector store.
- **OpenAI**: For the language model (GPT-4.1-mini).
- **Pydantic**: For data validation and structured output.

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**

   Create a `.env` file in the root of the project and add your OpenAI API key:

   ```
   OPENAI_API_KEY="your-api-key"
   ```

## Usage

To run the application, navigate to the `src` directory and run the `main.py` script:

```bash
python src/main.py
```

Once the application is running, you will be prompted to enter a topic to find and analyze a review. For example:

```
Enter a topic to find and analyze a review (e.g., 'a slow and boring movie'):
a beautifully shot film with a weak plot
```

The application will then find a relevant review and display a structured analysis:

```
--- Review Analysis Result ---
Sentiment: Negative
Summary: The reviewer acknowledges the film's visual appeal but is ultimately disappointed by the weak plot and lack of emotional depth.
Key Themes: ['cinematography', 'plot']
Predicted Rating: 4.5
Is a Recommendation: false
```

To exit the application, type `quit` or `exit`.

## Project Structure

```
ReviewExtractor_OpenAI_RAG/
├── data/
│   └── IMDB Dataset.csv
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── schema.py
├── .env.example
├── README.md
└── requirements.txt
```

- **data/**: Contains the dataset used for the application.
- **src/**: Contains the source code for the application.
  - **main.py**: The main entry point for the application.
  - **schema.py**: Defines the Pydantic models for the structured output.
- **.env.example**: An example of the environment variables file.
- **README.md**: This file.
- **requirements.txt**: A list of the Python dependencies for the project.
