from pydantic import BaseModel
from typing import List

class ProjectInfo(BaseModel):
    project_name: str
    technologies: List[str]
    main_goal: str

