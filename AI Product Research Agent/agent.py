import tools
from report_generator import create_html_report, send_report_by_email

class ProductResearchAgent:
    """
    An agent that orchestrates the product research process using live, online tools.
    """
    def __init__(self):
        print("Product Research Agent (Online Edition) is initialized.")

    def run(self, product_idea: str):
        """
        Executes the entire research workflow using online tools.
        """
        print(f"\n🚀 Starting LIVE research for idea: '{product_idea}'")

        # Step 1: Define Research Questions using an LLM
        print("\nStep 1: Defining research questions...")
        research_questions = tools.define_research_questions(product_idea)
        print("✅ Research questions defined.")
        print(f"Generated Questions:\n{research_questions}\n")


        # Step 2: Analyze Competitors using Web Search and LLM
        print("\nStep 2: Analyzing competitors...")
        competitor_analysis = tools.analyze_competitors(product_idea)
        print("✅ Competitor analysis complete.")
        print(f"Generated Analysis:\n{competitor_analysis}\n")


        # Step 3: Generate Final Report using an LLM
        print("\nStep 3: Generating final report and recommendations...")
        final_report_content = tools.generate_product_report(
            product_idea,
            research_questions,
            competitor_analysis
        )
        print("✅ Final report generated.")


        # Step 4: Create and Send Report
        print("\nStep 4: Creating HTML report and sending email...")
        report_file = create_html_report(final_report_content, product_idea)
        send_report_by_email(report_file, product_idea)
        
        print("\n🏁 Research process finished successfully!")