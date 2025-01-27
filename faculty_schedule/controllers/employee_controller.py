from typing import List, Optional

import pandas as pd

from .base_controller import BaseController
from ..exceptions import NotFoundError, ValidationError
from ..models import Schedule
from ..models.employee import Employee


class EmployeeController(BaseController):
    def __init__(self):
        super().__init__()
        self.filename = 'employees.xlsx'

    def create_employee(self, data: dict) -> Employee:
        """Create a new employee record.

        Args:
            data (dict): Dictionary containing employee data with 'id' and 'name' fields.

        Returns:
            Employee: The newly created employee object.

        Raises:
            ValidationError: If an employee with the given ID already exists.
        """
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

    def get_employee(self, employee_id: int) -> Employee:
        """Retrieve a specific employee by their ID.

        Args:
            employee_id (int): The ID of the employee to retrieve.

        Returns:
            Employee: The employee object with the specified ID.

        Raises:
            NotFoundError: If no employee with the given ID exists.
        """
        df = self._load_df(self.filename)
        if df.empty:
            employee_data = pd.DataFrame(columns=['id', 'name'])
        else:
            employee_data = df[df['id'] == employee_id] if not df.empty else pd.DataFrame(columns=['id', 'name'])

        if employee_data.empty:
            raise NotFoundError(f'Employee with id {employee_id} not found')

        schedules_df = self._load_df('schedules.xlsx')
        schedules = [
            Schedule(**{
                'id': row['id'],
                'employee_id': row['employee_id'],
                'code': str(row['code']),
                'description': row['description']
            })
            for _, row in schedules_df[schedules_df['employee_id'] == employee_id].iterrows()
        ]

        return Employee(
            id=employee_data.iloc[0]['id'],
            name=employee_data.iloc[0]['name'],
            schedules=schedules
        )

    def get_employees(self, employee_id: Optional[int] = None, name: Optional[str] = None) -> List[Employee]:
        """Retrieve a list of employees, optionally filtered by ID or name.

        Args:
            employee_id (Optional[int], optional): Filter by employee ID. Defaults to None.
            name (Optional[str], optional): Filter by employee name (case-insensitive partial match). Defaults to None.

        Returns:
            List[Employee]: List of employee objects matching the filter criteria.
        """
        df = self._load_df(self.filename)
        return [
            Employee(id=row['id'], name=row['name'])
            for _, row in df.iterrows()
            if name is None or name.lower() in row['name'].lower() or employee_id == row['id']
        ]

    def update_employee(self, employee_id: int, data: dict) -> Employee:
        """Update an existing employee's information.

        Args:
            employee_id (int): The ID of the employee to update.
            data (dict): Dictionary containing updated employee data (currently supports 'name' field).

        Returns:
            Employee: The updated employee object.

        Raises:
            NotFoundError: If no employee with the given ID exists.
        """
        df = self._load_df(self.filename)

        if employee_id not in df['id'].values:
            raise NotFoundError(f'Employee with id {employee_id} not found')

        name = data.get('name')

        df.loc[df['id'] == employee_id, 'name'] = name.strip()
        self._save_df(df, self.filename)

        return Employee(id=employee_id, name=name)

    def delete_employee(self, employee_id: int) -> bool:
        """Delete an employee record.

        Args:
            employee_id (int): The ID of the employee to delete.

        Returns:
            bool: True if the employee was successfully deleted.

        Raises:
            NotFoundError: If no employee with the given ID exists.
            ValidationError: If the employee has existing schedules.
        """
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
