from pydantic import BaseModel, Field
from typing import List, Optional
from .schedule import Schedule


class Employee(BaseModel):
    id: int
    name: str
    schedules: Optional[List[Schedule]] = Field(default=list)
