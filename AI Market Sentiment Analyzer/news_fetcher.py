"""This module is solely responsible for fetching and parsing 
website text.
"""
# /news_fetcher.py
import requests
from config import NEWS_API_KEY

def fetch_financial_news(query: str, num_articles: int = 10) -> str | None:
    """
    Fetches and concatenates the content of recent financial news articles.

    Args:
        query (str): The company, stock ticker, or topic to search for.
        num_articles (int): The number of articles to fetch.

    Returns:
        str | None: A single string containing the content of all articles,
                    or None if an error occurs.
    """
    url = (f"https://newsapi.org/v2/everything?"
           f"q={query}&"
           f"language=en&"
           f"sortBy=publishedAt&"
           f"pageSize={num_articles}&"
           f"apiKey={NEWS_API_KEY}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok" or not data.get("articles"):
            print(f"Error from NewsAPI: {data.get('message', 'No articles found.')}")
            return None

        # Concatenate content from all articles into one text block
        all_content = ""
        for i, article in enumerate(data["articles"]):
            title = article.get('title', 'No Title')
            content = article.get('content', 'No content available.')
            all_content += f"--- Article {i+1}: {title} ---\n{content}\n\n"
        
        return all_content.strip()

    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return None