from datetime import time
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict

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
    model_config = ConfigDict(
        json_encoders={
            Day: lambda d: d.value,
            time: lambda t: t.strftime('%H:%M')
        }
    )

    id: int = Field(default_factory=generate_id)
    day: Day
    schedule_id: int
    start_time: time
    end_time: time
    detail: str
    schedule: Optional['Schedule'] = Field(default=None)

    @classmethod
    @field_validator('end_time')
    def validate_time_range(cls, end_time: time, values: dict) -> time:
        start_time = values.get('start_time')
        if start_time and end_time <= start_time:
            raise ValueError('End time must be after start time')
        return end_time

    def model_dump(self, *args, **kwargs) -> dict:
        data = super().model_dump(*args, **kwargs)
        if 'start_time' in data:
            data['start_time'] = self.start_time.strftime('%H:%M')
        if 'end_time' in data:
            data['end_time'] = self.end_time.strftime('%H:%M')
        if 'day' in data:
            data['day'] = self.day.value
        return data
