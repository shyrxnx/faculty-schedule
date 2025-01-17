from typing import List

import pandas as pd

from .base_controller import BaseExcelController
from ..exceptions import NotFoundError, ValidationError
from ..models.employee import Employee


class EmployeeController(BaseExcelController):
    def __init__(self):
        super().__init__()
        self.filename = "employees.xlsx"

    def _validate_employee_data(self, name: str, employee_id: int = None):
        """Validate employee data before creation/update"""
        df = self._load_df(self.filename)

        # Validate required fields
        self._validate_required(name, "Employee name")

        # Validate name length
        if len(name) < 2 or len(name) > 100:
            raise ValidationError("Employee name must be between 2 and 100 characters")

        # Check for unique name (case-insensitive)
        name_lower = name.lower()
        if employee_id:
            existing = df[(df['name'].str.lower() == name_lower) & (df['id'] != employee_id)]
        else:
            existing = df[df['name'].str.lower() == name_lower]

        if not existing.empty:
            raise ValidationError(f"An employee with the name '{name}' already exists")

    def create_employee(self, name: str) -> Employee:
        self._validate_employee_data(name)

        df = self._load_df(self.filename)
        new_id = 1 if df.empty else df['id'].max() + 1

        new_employee = {
            'id': new_id,
            'name': name.strip()
        }

        df = pd.concat([df, pd.DataFrame([new_employee])], ignore_index=True)
        self._save_df(df, self.filename)

        return Employee(id=new_id, name=name, schedules=[])

    def get_employee(self, employee_id: int) -> Employee:
        df = self._load_df(self.filename)
        employee_data = df[df['id'] == employee_id]

        if employee_data.empty:
            raise NotFoundError(f"Employee with id {employee_id} not found")

        return Employee(
            id=employee_data.iloc[0]['id'],
            name=employee_data.iloc[0]['name'],
            schedules=[]
        )

    def get_all_employees(self) -> List[Employee]:
        df = self._load_df(self.filename)
        return [
            Employee(id=row['id'], name=row['name'], schedules=[])
            for _, row in df.iterrows()
        ]

    def update_employee(self, employee_id: int, name: str) -> Employee:
        df = self._load_df(self.filename)
        if employee_id not in df['id'].values:
            raise NotFoundError(f"Employee with id {employee_id} not found")

        self._validate_employee_data(name, employee_id)

        df.loc[df['id'] == employee_id, 'name'] = name.strip()
        self._save_df(df, self.filename)

        return Employee(id=employee_id, name=name, schedules=[])

    def delete_employee(self, employee_id: int) -> bool:
        df = self._load_df(self.filename)
        if employee_id not in df['id'].values:
            raise NotFoundError(f"Employee with id {employee_id} not found")

        # Check for existing schedules
        schedules_df = self._load_df("schedules.xlsx")
        if not schedules_df.empty and employee_id in schedules_df['employee_id'].values:
            raise ValidationError("Cannot delete employee with existing schedules")

        df = df[df['id'] != employee_id]
        self._save_df(df, self.filename)
        return True
