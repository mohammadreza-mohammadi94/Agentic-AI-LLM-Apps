# agents/schemas.py
from pydantic import BaseModel, Field
from typing import List

class ExtractedEntities(BaseModel):
    """
    A Pydantic model to structure the named entities extracted from a text.
    [cite_start]The model expects entities to be categorized as persons, organizations, etc[cite: 1].
    """
    persons: List[str] = Field(
        default_factory=list, 
        description="A list of names of people mentioned in the text."
    )
    organizations: List[str] = Field(
        default_factory=list,
        description="A list of organizations, companies, or institutions."
    )
    locations: List[str] = Field(
        default_factory=list,
        description="A list of geographical or physical locations."
    )
    dates: List[str] = Field(
        default_factory=list,
        description="A list of specific dates or date ranges."
    )
    other: List[str] = Field(
        default_factory=list,
        description="A list of other named entities that do not fit in other categories."
    )