# Import libraries
from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    step: int
    title: str
    description: str

class ExecutedTask(BaseModel):
    step: int
    title: str
    description: str
    result: str