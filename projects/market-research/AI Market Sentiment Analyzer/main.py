"""
This script ties everything together and runs the agent.
"""

# /main.py
from config import FINANCIAL_TOPIC
from news_fetcher import fetch_financial_news
from market_analyst_agent import MarketAnalystAgent

def main():
    """
    Main function to run the financial market research agent.
    """
    print(f"--- Starting Financial Market Research for: {FINANCIAL_TOPIC} ---")

    # 1. Fetch recent financial news
    print("📰 Fetching financial news...")
    news_text = fetch_financial_news(FINANCIAL_TOPIC)
    
    if not news_text:
        print("Failed to fetch news. Exiting.")
        return

    print("✅ News fetched successfully.")
    
    # 2. Initialize and run the agent
    agent = MarketAnalystAgent()
    agent.analyze(news_text, FINANCIAL_TOPIC)
    
    print("\n--- Financial Market Research Complete ---")

if __name__ == "__main__":
    main()