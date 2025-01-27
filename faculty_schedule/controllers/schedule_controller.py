from datetime import datetime

import pandas as pd

from .base_controller import BaseController
from ..exceptions import NotFoundError, ValidationError
from ..models import Schedule, ScheduleSlot, Day


class ScheduleController(BaseController):
    def __init__(self):
        super().__init__()
        self.schedules_file = 'schedules.xlsx'
        self.slots_file = 'schedule_slots.xlsx'

    def _validate_schedule_data(self, employee_id: int, code: str, schedule_id: int = None):
        """Validate schedule data before creation/update"""
        schedules_df = self._load_df(self.schedules_file)
        employees_df = self._load_df('employees.xlsx')

        # Validate required fields
        self._validate_required(code, 'Schedule code')

        # Validate foreign key
        self._validate_foreign_key(employees_df, employee_id, 'employee_id')

        # Validate code format and length
        if not code.replace('-', '').isalnum():
            raise ValidationError('Schedule code must contain only letters, numbers, and hyphens')
        if len(code) < 2 or len(code) > 20:
            raise ValidationError('Schedule code must be between 2 and 20 characters')

        # Validate unique code per employee
        code_lower = code.lower()
        if schedule_id:
            existing = schedules_df[
                (schedules_df['employee_id'] == employee_id) &
                (schedules_df['code'].str.lower() == code_lower) &
                (schedules_df['id'] != schedule_id)
                ] if not schedules_df.empty else pd.DataFrame()
        else:
            existing = schedules_df[
                (schedules_df['employee_id'] == employee_id) &
                (schedules_df['code'].str.lower() == code_lower)
                ] if not schedules_df.empty else pd.DataFrame()

        if not existing.empty:
            raise ValidationError(f'Schedule code \'{code}\' already exists for this employee')

    def _validate_schedule_slot(self, schedule_id: int, day: Day, start_time: str, end_time: str, detail: str):
        """Validate schedule slot data"""
        slots_df = self._load_df(self.slots_file)
        schedules_df = self._load_df(self.schedules_file)

        # Validate schedule exists
        self._validate_foreign_key(schedules_df, schedule_id, 'schedule_id')

        # Validate required fields
        self._validate_required(start_time, 'Start time')
        self._validate_required(end_time, 'End time')
        self._validate_required(detail, 'Detail')
        self._validate_required(day, 'Day')
        self._validate_required(schedule_id, 'Schedule ID')
        self._validate_required(detail, 'Detail')

        # Convert times to datetime.time objects
        try:
            start = datetime.strptime(start_time, '%H:%M').time()
            end = datetime.strptime(end_time, '%H:%M').time()
        except ValueError:
            raise ValidationError('Invalid time format. Use HH:MM')

        # Validate time range
        if start >= end:
            raise ValidationError('Start time must be before end time')

        # Check for time slot conflicts
        schedule_data = schedules_df[schedules_df['id'] == schedule_id].iloc[0]
        employee_id = schedule_data['employee_id']

        # Get all schedules for this employee
        employee_schedules = schedules_df[schedules_df['employee_id'] == employee_id]['id'].values

        # Get all slots for this employee's schedules on the same day
        existing_slots = slots_df[
            (slots_df['schedule_id'].isin(employee_schedules)) &
            (slots_df['day'] == day.value)
            ] if not slots_df.empty else pd.DataFrame()

        for _, slot in existing_slots.iterrows():
            slot_start = datetime.strptime(slot['start_time'], '%H:%M').time()
            slot_end = datetime.strptime(slot['end_time'], '%H:%M').time()

            if start < slot_end and end > slot_start:
                raise ValidationError(f'Time slot conflicts with existing schedule on {day.value}')

    def create_schedule(self, data: dict) -> Schedule:
        """Create a new schedule for an employee.

        Args:
            data (dict): Dictionary containing:
                - employee_id: ID of the employee
                - code: Unique schedule code
                - description: Optional schedule description

        Returns:
            Schedule: The created schedule object

        Raises:
            ValidationError: If the schedule data is invalid
        """
        employee_id = data.get('employee_id')
        code = data.get('code')
        description = data.get('description')

        self._validate_schedule_data(employee_id, code)

        df = self._load_df(self.schedules_file)
        schedule = Schedule.model_validate({
            'employee_id': employee_id,
            'code': code.strip(),
            'description': description.strip()
        })

        df = pd.concat([df, pd.DataFrame([schedule.model_dump(exclude={'details', 'employee'})])], ignore_index=True)
        self._save_df(df, self.schedules_file)

        return schedule

    def get_schedule(self, schedule_id: int) -> Schedule:
        """Retrieve a schedule by its ID, including all schedule slots.

        Args:
            schedule_id (int): ID of the schedule to retrieve

        Returns:
            Schedule: The schedule object with its associated slots

        Raises:
            NotFoundError: If the schedule doesn't exist
        """
        schedules_df = self._load_df(self.schedules_file)
        slots_df = self._load_df(self.slots_file)

        schedule_data = schedules_df[schedules_df['id'] == schedule_id]

        if schedule_data.empty:
            raise NotFoundError(f'Schedule with id {schedule_id} not found')

        schedule_data = schedule_data.iloc[0]

        slots_data = slots_df[slots_df['schedule_id'] == schedule_id] if not slots_df.empty else pd.DataFrame()
        slots = [
            ScheduleSlot(
                schedule_id=slot['schedule_id'],
                day=Day(slot['day']),
                start_time=datetime.strptime(slot['start_time'], '%H:%M').time(),
                end_time=datetime.strptime(slot['end_time'], '%H:%M').time(),
                detail=slot['detail']
            )
            for _, slot in slots_data.iterrows()
        ]

        return Schedule(
            id=schedule_data['id'],
            employee_id=schedule_data['employee_id'],
            code=schedule_data['code'],
            description=schedule_data['description'],
            details=slots
        )

    def add_schedule_slot(self, data: dict) -> ScheduleSlot:
        """Add a new time slot to an existing schedule.

        Args:
            data (dict): Dictionary containing:
                - schedule_id: ID of the schedule
                - day: Day enum value
                - start_time: Start time in HH:MM format
                - end_time: End time in HH:MM format
                - detail: Description of the schedule slot

        Returns:
            ScheduleSlot: The created schedule slot object

        Raises:
            ValidationError: If the slot data is invalid or conflicts with existing slots
            NotFoundError: If the schedule doesn't exist
        """
        schedule_id = data.get('schedule_id')
        day = Day(data.get('day'))
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        detail = data.get('detail')

        self._validate_schedule_slot(schedule_id, day, start_time, end_time, detail)

        df = self._load_df(self.slots_file)

        slot = ScheduleSlot.model_validate({
            'schedule_id': schedule_id,
            'day': day,
            'detail': detail,
            'start_time': start_time,
            'end_time': end_time
        })

        slot_data = pd.DataFrame([slot.model_dump(exclude={'schedule'})])

        df = pd.concat([df, slot_data], ignore_index=True)
        self._save_df(df, self.slots_file)

        return slot

    def edit_schedule_slot(self, slot_id: int, data: ScheduleSlot) -> ScheduleSlot:
        """Edit an existing schedule slot.

        Args:
            slot_id (int): ID of the schedule slot to edit
            data (dict): Dictionary containing:
                - day: Day enum value
                - start_time: Start time in HH:MM format
                - end_time: End time in HH:MM format
                - detail: Description of the schedule slot

        Returns:
            ScheduleSlot: The edited schedule slot object

        Raises:
            ValidationError: If the slot data is invalid or conflicts with existing slots
            NotFoundError: If the slot doesn't exist
        """

        slots_df = self._load_df(self.slots_file)

        if slot_id not in slots_df['id'].values:
            raise NotFoundError(f'Schedule slot with id {slot_id} not found')

        slot = ScheduleSlot.model_validate(data)

        slots_df.loc[slots_df['id'] == slot_id, 'day'] = slot.day.value
        slots_df.loc[slots_df['id'] == slot_id, 'start_time'] = slot.start_time.strftime('%H:%M')
        slots_df.loc[slots_df['id'] == slot_id, 'end_time'] = slot.end_time.strftime('%H:%M')
        slots_df.loc[slots_df['id'] == slot_id, 'detail'] = slot.detail

        self._save_df(slots_df, self.slots_file)

        return slot

    def delete_schedule_slot(self, slot_id: int) -> bool:
        """Delete a schedule slot.

        Args:
            slot_id (int): ID of the schedule slot to delete

        Returns:
            bool: True if the slot was successfully deleted

        Raises:
            NotFoundError: If the slot doesn't exist
        """
        slots_df = self._load_df(self.slots_file)

        if slot_id not in slots_df['id'].values:
            raise NotFoundError(f'Schedule slot with id {slot_id} not found')

        slots_df = slots_df[slots_df['id'] != slot_id]
        self._save_df(slots_df, self.slots_file)

        return True

    def delete_schedule(self, schedule_id: int) -> bool:
        """Delete a schedule and all its associated slots.

        Args:
            schedule_id (int): ID of the schedule to delete

        Returns:
            bool: True if the schedule was successfully deleted

        Raises:
            NotFoundError: If the schedule doesn't exist
        """
        schedules_df = self._load_df(self.schedules_file)
        slots_df = self._load_df(self.slots_file)

        if schedule_id not in schedules_df['id'].values:
            raise NotFoundError(f'Schedule with id {schedule_id} not found')

        # Delete associated slots first
        slots_df = slots_df[slots_df['schedule_id'] != schedule_id]
        self._save_df(slots_df, self.slots_file)

        # Delete schedule
        schedules_df = schedules_df[schedules_df['id'] != schedule_id]
        self._save_df(schedules_df, self.schedules_file)

        return True
