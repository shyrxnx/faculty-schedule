class DatabaseError(Exception):
    """Base class for database-related exceptions"""


class ForeignKeyError(DatabaseError):
    """Raised when a foreign key constraint is violated"""


class UniqueConstraintError(DatabaseError):
    """Raised when a unique constraint is violated"""


class NotFoundError(DatabaseError):
    """Raised when a record is not found"""


class ValidationError(DatabaseError):
    """Raised when data validation fails"""
