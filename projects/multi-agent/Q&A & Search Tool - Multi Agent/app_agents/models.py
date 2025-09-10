from pydantic import BaseModel, validator

class SearchDecision(BaseModel):
    decision: str

    @validator('decision')
    def validate_decision(cls, v):
        if v.upper() not in ("YES", "NO"):
            raise ValueError("Decision must be 'YES' or 'NO'.")
        return v.upper()

