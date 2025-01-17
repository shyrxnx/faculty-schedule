from datetime import time
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Day(str, Enum):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'


class ScheduleSlot(BaseModel):
    id: int
    day: Day
    schedule_id: int
    start_time: time
    end_time: time
    schedule: Optional['Schedule'] = None
