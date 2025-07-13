# schemas
from pydantic import BaseModel, Field
from typing import Literal

class AnalysisResult(BaseModel):
    """
    Represents the structured analysis of a customer's feedback.
    This is the output of the FeedbackAnalyzerAgent.
    """
    sentiment: Literal["positive", "negative", 'neutral'] = Field(
        ..., # Make this field required
        description="The oversall sentiment of the feedback"
    )
    problem_summary: str = Field(
        ..., # Makes this field required
        description="A concise, one-sentence summary of the customer's core issue."
    )

class FinalReport(BaseModel):
    """
    Represents the complete, final report containing all information.
    """
    original_feedback: str = Field(
        description="The original, unprocessed text from the customer")
    analysis: AnalysisResult = Field(
        description="The nested analysis object produced by the FeedbackAnalyzerAgent")
    suggested_response: str = Field(
        description="The generated response draft for the customer support agent.")
    