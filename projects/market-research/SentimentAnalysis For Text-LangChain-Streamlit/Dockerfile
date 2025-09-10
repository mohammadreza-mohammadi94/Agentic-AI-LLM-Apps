# Use Python 3.10 as the base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a directory for ChromaDB persistence
RUN mkdir -p ./chromaDB

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the Streamlit port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "sentiment_analysis.py", "--server.address=0.0.0.0"]