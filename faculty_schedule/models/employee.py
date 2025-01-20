from typing import List

from pydantic import BaseModel, Field

from .schedule import Schedule
from ..utils.generators import generate_id


class Employee(BaseModel):
    id: int = Field(default_factory=generate_id)
    name: str
    schedules: List[Schedule] = Field(default_factory=list)
