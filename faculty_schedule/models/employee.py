from typing import List, Optional

from pydantic import BaseModel, Field

from .schedule import Schedule


class Employee(BaseModel):
    id: int
    name: str
    schedules: Optional[List[Schedule]] = Field(default=list)
