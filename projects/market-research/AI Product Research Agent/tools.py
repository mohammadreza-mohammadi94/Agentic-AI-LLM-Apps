import config
from openai import OpenAI
from tavily import TavilyClient

# Initialize clients once to be used by all tools
client = OpenAI(api_key=config.OPENAI_API_KEY)
tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)

def define_research_questions(product_idea: str) -> str:
    """
    Generates key strategic questions for market research using OpenAI's GPT model.
    """
    print(f"Tool Executed: define_research_questions (Online) for '{product_idea}'")
    
    prompt = f"""
    Based on the product idea '{product_idea}', generate a concise list of 5-7 critical strategic questions
    that a product manager must answer. These questions should cover market need, target audience,
    value proposition, competition, and technical feasibility.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a world-class product strategist."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def analyze_competitors(product_idea: str) -> str:
    """
    Performs a live web search to find competitors and then uses GPT to analyze them.
    """
    print(f"Tool Executed: analyze_competitors (Online) for '{product_idea}'")

    # Step 1: Use Tavily to search for competitors
    print("--> Performing web search for competitors...")
    search_query = f"competitors and alternatives for '{product_idea}'"
    search_results = tavily_client.search(query=search_query, search_depth="advanced")
    
    # Extract relevant content from search results
    context = "\n".join([result['content'] for result in search_results['results']])

    # Step 2: Use GPT to analyze the search results
    print("--> Analyzing search results with GPT...")
    prompt = f"""
    Based on the following web search results, identify the top 3-4 competitors for the product idea '{product_idea}'.
    For each competitor, provide a brief analysis of their strengths, weaknesses, and primary value proposition.

    Web Search Results:
    ---
    {context}
    ---
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert market analyst. Your analysis is sharp and concise."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def generate_product_report(product_idea: str, research_questions: str, competitor_analysis: str) -> str:
    """
    Generates a final, comprehensive report with strategic recommendations using GPT.
    """
    print(f"Tool Executed: generate_product_report (Online) for '{product_idea}'")
    
    prompt = f"""
    Create a comprehensive product research report for the idea: '{product_idea}'.
    Structure the report with the following sections: Executive Summary, Key Research Questions, Competitive Landscape, and Strategic Recommendations.
    Use the provided information below to fill the relevant sections. Your recommendations should be insightful and actionable.

    Key Research Questions to address:
    ---
    {research_questions}
    ---

    Competitor Analysis:
    ---
    {competitor_analysis}
    ---
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a Senior Product Manager tasked with writing a go-to-market strategy report."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content