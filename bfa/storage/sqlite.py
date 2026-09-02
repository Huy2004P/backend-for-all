"""
Deprecated SQLite Module. Replaced by Enterprise Network Database Adapters.
"""

from bfa.storage.memory import MemoryStorage


class SQLiteStorage(MemoryStorage):
    """
    Deprecated legacy alias. Routes to zero-disk in-memory storage buffer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
