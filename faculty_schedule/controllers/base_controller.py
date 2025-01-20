from pathlib import Path

import pandas as pd

from ..exceptions import ValidationError


class BaseExcelController:
    def __init__(self):
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)

    def _save_df(self, df: pd.DataFrame, filename: str):
        filepath = self.data_dir / filename
        df.to_excel(filepath, index=False)

    def _load_df(self, filename: str) -> pd.DataFrame:
        filepath = self.data_dir / filename
        if not filepath.exists():
            return pd.DataFrame()
        return pd.read_excel(filepath)

    def _validate_unique(self, df: pd.DataFrame, column: str, value: any, id_column: str = None, id_value: int = None):
        """Validate that a value is unique in the given column"""
        if id_column and id_value:
            # Exclude current record when updating
            existing = df[(df[column] == value) & (df[id_column] != id_value)]
        else:
            existing = df[df[column] == value]

        if not existing.empty:
            raise ValidationError(f'Value \'{value}\' already exists in {column}')

    def _validate_foreign_key(self, related_df: pd.DataFrame, foreign_key: int, key_name: str):
        """Validate that a foreign key exists in the related table"""
        if foreign_key not in related_df['id'].values:
            raise ValidationError(f'Invalid {key_name}: {foreign_key} does not exist')

    def _validate_required(self, value: any, field_name: str):
        """Validate that a required field is not empty"""
        if pd.isna(value) or value == '':
            raise ValidationError(f'{field_name} is required')
