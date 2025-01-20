from typing import List, Optional

import pandas as pd

from .base_controller import BaseController
from ..exceptions import NotFoundError, ValidationError
from ..models.employee import Employee


class EmployeeController(BaseController):
    def __init__(self):
        super().__init__()
        self.filename = 'employees.xlsx'

    def create_employee(self, data: dict) -> Employee:
        df = self._load_df(self.filename)
        employee = Employee.model_validate(data)

        try:
            self.get_employee(employee.id)
            raise ValidationError(f'Employee with id {employee.id} already exists')
        except NotFoundError:
            pass

        df = pd.concat([df, pd.DataFrame([employee.model_dump(exclude={'schedules'})])], ignore_index=True)

        self._save_df(df, self.filename)

        return employee

    def get_employee(self, employee_id: int, include_schedules: bool = False) -> Employee:
        df = self._load_df(self.filename)
        if df.empty:
            employee_data = pd.DataFrame(columns=['id', 'name'])
        else:
            employee_data = df[df['id'] == employee_id] if not df.empty else pd.DataFrame(columns=['id', 'name'])

        if employee_data.empty:
            raise NotFoundError(f'Employee with id {employee_id} not found')

        # TODO: Implement the logic to include schedules
        return Employee(
            id=employee_data.iloc[0]['id'],
            name=employee_data.iloc[0]['name'],
            schedules=[]
        )

    def get_employees(self, employee_id: Optional[int] = None, name: Optional[str] = None) -> List[Employee]:
        df = self._load_df(self.filename)
        return [
            Employee(id=row['id'], name=row['name'])
            for _, row in df.iterrows()
            if name is None or name.lower() in row['name'].lower() or employee_id == row['id']
        ]

    def update_employee(self, employee_id: int, data: dict) -> Employee:
        df = self._load_df(self.filename)

        if employee_id not in df['id'].values:
            raise NotFoundError(f'Employee with id {employee_id} not found')

        name = data.get('name')

        df.loc[df['id'] == employee_id, 'name'] = name.strip()
        self._save_df(df, self.filename)

        return Employee(id=employee_id, name=name)

    def delete_employee(self, employee_id: int) -> bool:
        df = self._load_df(self.filename)
        if employee_id not in df['id'].values:
            raise NotFoundError(f'Employee with id {employee_id} not found')

        # Check for existing schedules
        schedules_df = self._load_df('schedules.xlsx')
        if not schedules_df.empty and employee_id in schedules_df['employee_id'].values:
            raise ValidationError('Cannot delete employee with existing schedules')

        df = df[df['id'] != employee_id]
        self._save_df(df, self.filename)
        return True
