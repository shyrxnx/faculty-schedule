from typing import List, Optional

from pydantic import BaseModel, Field

from .schedule_slot import ScheduleSlot
from ..utils.generators import generate_id


class Schedule(BaseModel):
    id: int = Field(default_factory=generate_id)
    employee_id: int
    code: str
    description: Optional[str] = Field(default=None)
    details: List[ScheduleSlot] = Field(default_factory=list)
    employee: Optional['Employee'] = Field(default=None)
