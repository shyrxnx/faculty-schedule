from typing import List, Optional

from pydantic import BaseModel, Field

from .schedule_slot import ScheduleSlot


class Schedule(BaseModel):
    id: int
    employee_id: int
    code: str
    description: str
    details: List[ScheduleSlot] = Field(default=list)
    employee: Optional['Employee'] = None
