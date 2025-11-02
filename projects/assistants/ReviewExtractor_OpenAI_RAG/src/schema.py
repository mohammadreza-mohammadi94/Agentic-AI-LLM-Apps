# src/schemas.py

"""
Defines the Pydantic data models for structured output.

This module contains the data structures that the LLM is expected to return.
Using Pydantic ensures that the output is typed, validated, and easy to work with.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ReviewAnalysis(BaseModel):
    """
    A structured representation of an analysis performed on a single movie review.

    This model defines the exact fields to be extracted from the review text.
    The descriptions for each field act as direct instructions for the LLM.
    """

    sentiment: str = Field(
        description="The overall sentiment of the review. This must be one of the following strings: 'Positive', 'Negative', or 'Neutral'."
    )

    summary: str = Field(
        description="A concise, one to two-sentence summary that captures the main opinion and key points of the reviewer."
    )

    key_themes: Optional[List[str]] = Field(
        description="A list of specific aspects or themes of the movie that the reviewer mentioned. Examples: 'acting', 'plot', 'directing', 'soundtrack', 'cinematography', 'ending'."
    )

    rating_prediction: float = Field(
        description="Based *only* on the text of the review, predict a plausible rating score the user might have given, on a scale of 1.0 to 10.0.",
        ge=1.0,  # 'ge' means 'greater than or equal to'
        le=10.0,  # 'le' means 'less than or equal to'
    )

    is_recommendation: Optional[bool] = Field(
        description="Set to true if the reviewer explicitly recommends watching the movie (e.g., 'I recommend this movie', 'a must-see'). Set to false if they recommend against it. If no explicit recommendation is made, leave it as null."
    )


# You can add more schemas here if your application grows.
# For example, you might want a schema for comparing two reviews.
class ComparativeAnalysis(BaseModel):
    """An example of a more complex schema for future use."""

    review_a_summary: str = Field(description="Summary of the first review.")
    review_b_summary: str = Field(description="Summary of the second review.")
    common_themes: List[str] = Field(description="Themes mentioned in both reviews.")
