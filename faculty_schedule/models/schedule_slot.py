from datetime import time
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from ..utils.generators import generate_id


class Day(str, Enum):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'


class ScheduleSlot(BaseModel):
    id: int = Field(default_factory=generate_id)
    day: Day
    schedule_id: int
    start_time: time
    end_time: time
    schedule: Optional['Schedule'] = Field(default=None)
