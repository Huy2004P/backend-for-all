"""
Deprecated SQLite Storage Module - Replaced by pure JSONStorage.

SQLite is completely removed. Any legacy reference safely routes to JSONStorage.
"""

from bfa.storage.json_store import JSONStorage


class SQLiteStorage(JSONStorage):
    """
    SQLiteStorage đã được thay thế hoàn toàn bằng JSONStorage thuần túy.
    Tuyệt đối không sử dụng tệp SQLite nhị phân hay thư viện sqlite3.
    """
    def __init__(self, db_path: str = "data/bfa_store.json"):
        clean_path = "data/bfa_store.json" if str(db_path).endswith(".db") else str(db_path)
        super().__init__(data_file=clean_path)
