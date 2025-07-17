from agent import ProductResearchAgent
import config

def main():
    """
    Main entry point for the AI Product Research Agent.
    """
    # The initial idea that triggers the research process
    product_idea = "Build an AI agent for medical diagnosis support"
    
    # Initialize and run the agent
    try:
        research_agent = ProductResearchAgent()
        research_agent.run(product_idea)
    except Exception as e:
        print(f"An error occurred during the research process: {e}")

if __name__ == "__main__":
    main()