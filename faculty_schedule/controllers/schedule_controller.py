from datetime import datetime

import pandas as pd

from .base_controller import BaseExcelController
from ..exceptions import NotFoundError, ValidationError
from ..models.schedule import Schedule
from ..models.schedule_slot import ScheduleSlot, Day


class ScheduleController(BaseExcelController):
    def __init__(self):
        super().__init__()
        self.schedules_file = "schedules.xlsx"
        self.slots_file = "schedule_slots.xlsx"

    def _validate_schedule_data(self, employee_id: int, code: str, description: str, schedule_id: int = None):
        """Validate schedule data before creation/update"""
        schedules_df = self._load_df(self.schedules_file)
        employees_df = self._load_df("employees.xlsx")

        # Validate required fields
        self._validate_required(code, "Schedule code")
        self._validate_required(description, "Description")

        # Validate foreign key
        self._validate_foreign_key(employees_df, employee_id, "employee_id")

        # Validate code format and length
        if not code.replace("-", "").isalnum():
            raise ValidationError("Schedule code must contain only letters, numbers, and hyphens")
        if len(code) < 2 or len(code) > 20:
            raise ValidationError("Schedule code must be between 2 and 20 characters")

        # Validate unique code per employee
        code_lower = code.lower()
        if schedule_id:
            existing = schedules_df[
                (schedules_df['employee_id'] == employee_id) &
                (schedules_df['code'].str.lower() == code_lower) &
                (schedules_df['id'] != schedule_id)
                ]
        else:
            existing = schedules_df[
                (schedules_df['employee_id'] == employee_id) &
                (schedules_df['code'].str.lower() == code_lower)
                ]

        if not existing.empty:
            raise ValidationError(f"Schedule code '{code}' already exists for this employee")

    def _validate_schedule_slot(self, schedule_id: int, day: Day, start_time: str, end_time: str):
        """Validate schedule slot data"""
        slots_df = self._load_df(self.slots_file)
        schedules_df = self._load_df(self.schedules_file)

        # Validate schedule exists
        if schedule_id not in schedules_df['id'].values:
            raise NotFoundError(f"Schedule with id {schedule_id} not found")

        # Convert times to datetime.time objects
        try:
            start = datetime.strptime(start_time, "%H:%M").time()
            end = datetime.strptime(end_time, "%H:%M").time()
        except ValueError:
            raise ValidationError("Invalid time format. Use HH:MM")

        # Validate time range
        if start >= end:
            raise ValidationError("Start time must be before end time")

        # Check for time slot conflicts
        schedule_data = schedules_df[schedules_df['id'] == schedule_id].iloc[0]
        employee_id = schedule_data['employee_id']

        # Get all schedules for this employee
        employee_schedules = schedules_df[schedules_df['employee_id'] == employee_id]['id'].values

        # Get all slots for this employee's schedules on the same day
        existing_slots = slots_df[
            (slots_df['schedule_id'].isin(employee_schedules)) &
            (slots_df['day'] == day.value)
            ]

        for _, slot in existing_slots.iterrows():
            slot_start = datetime.strptime(slot['start_time'], "%H:%M").time()
            slot_end = datetime.strptime(slot['end_time'], "%H:%M").time()

            if start < slot_end and end > slot_start:
                raise ValidationError(f"Time slot conflicts with existing schedule on {day.value}")

    def create_schedule(self, employee_id: int, code: str, description: str) -> Schedule:
        self._validate_schedule_data(employee_id, code, description)

        df = self._load_df(self.schedules_file)
        new_id = 1 if df.empty else df['id'].max() + 1

        new_schedule = {
            'id': new_id,
            'employee_id': employee_id,
            'code': code.strip(),
            'description': description.strip()
        }

        df = pd.concat([df, pd.DataFrame([new_schedule])], ignore_index=True)
        self._save_df(df, self.schedules_file)

        return Schedule(
            id=new_id,
            employee_id=employee_id,
            code=code,
            description=description,
            details=[]
        )

    def add_schedule_slot(self, schedule_id: int, day: Day, start_time: str, end_time: str) -> ScheduleSlot:
        self._validate_schedule_slot(schedule_id, day, start_time, end_time)

        df = self._load_df(self.slots_file)
        new_id = 1 if df.empty else df['id'].max() + 1

        new_slot = {
            'id': new_id,
            'schedule_id': schedule_id,
            'day': day.value,
            'start_time': start_time,
            'end_time': end_time
        }

        df = pd.concat([df, pd.DataFrame([new_slot])], ignore_index=True)
        self._save_df(df, self.slots_file)

        return ScheduleSlot(
            id=new_id,
            schedule_id=schedule_id,
            day=day,
            start_time=datetime.strptime(start_time, "%H:%M").time(),
            end_time=datetime.strptime(end_time, "%H:%M").time()
        )

    def delete_schedule(self, schedule_id: int) -> bool:
        schedules_df = self._load_df(self.schedules_file)
        slots_df = self._load_df(self.slots_file)

        if schedule_id not in schedules_df['id'].values:
            raise NotFoundError(f"Schedule with id {schedule_id} not found")

        # Delete associated slots first
        slots_df = slots_df[slots_df['schedule_id'] != schedule_id]
        self._save_df(slots_df, self.slots_file)

        # Delete schedule
        schedules_df = schedules_df[schedules_df['id'] != schedule_id]
        self._save_df(schedules_df, self.schedules_file)

        return True
