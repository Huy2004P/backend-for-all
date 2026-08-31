"""
Base Storage abstraction interface for Backend for All.
"""

from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def insert(self, table: str, data: dict) -> dict:
        """Insert a record and return the created record with its ID."""
        pass

    @abstractmethod
    def get(self, table: str, id_value: int | str, id_field: str = "id") -> dict | None:
        """Get a single record by its ID."""
        pass

    @abstractmethod
    def find_all(self, table: str) -> list[dict]:
        """Retrieve all records in a table/collection."""
        pass

    @abstractmethod
    def find(self, table: str, filter_dict: dict) -> list[dict]:
        """Find records matching given filter conditions."""
        pass

    @abstractmethod
    def update(self, table: str, id_value: int | str, updates: dict, id_field: str = "id") -> dict | None:
        """Update fields of an existing record."""
        pass

    @abstractmethod
    def delete(self, table: str, id_value: int | str, id_field: str = "id") -> bool:
        """Delete a record by ID."""
        pass

    @abstractmethod
    def get_stats(self) -> dict:
        """Return statistics on record counts across tables."""
        pass
