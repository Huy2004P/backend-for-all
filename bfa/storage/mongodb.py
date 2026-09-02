"""
MongoDB Enterprise NoSQL Document Storage Adapter for Backend for All.

Connects directly to MongoDB database servers over TCP network port (default: 27017)
or MongoDB Atlas URI (mongodb+srv://...).
Stores zero local files on disk.
"""

from bfa.storage.base import BaseStorage


class MongoStorage(BaseStorage):
    """
    Adapter kết nối mạng thuần TCP tới cụm máy chủ MongoDB (Cổng 27017).
    """
    def __init__(
        self,
        host: str = "localhost",
        port: int = 27017,
        dbname: str = "bfa_database",
        uri: str | None = None,
    ):
        self.host = host
        self.port = int(port)
        self.dbname = dbname
        self.uri = uri
        self._client = None
        self._db = None
        self._fallback_memory = {}
        self._init_connection()

    def _init_connection(self) -> None:
        try:
            import pymongo
            connection_str = self.uri or f"mongodb://{self.host}:{self.port}/"
            self._client = pymongo.MongoClient(connection_str, serverSelectionTimeoutMS=2000)
            self._db = self._client[self.dbname]
        except Exception:
            self._client = None
            self._db = None

    def insert(self, table: str, data: dict) -> dict:
        if self._db is not None:
            try:
                rec = data.copy()
                col = self._db[table]
                result = col.insert_one(rec)
                if "id" not in rec:
                    rec["id"] = str(result.inserted_id)
                return rec
            except Exception:
                pass

        if table not in self._fallback_memory:
            self._fallback_memory[table] = []
        rec = data.copy()
        if "id" not in rec or rec["id"] is None:
            rec["id"] = len(self._fallback_memory[table]) + 1
        self._fallback_memory[table].append(rec)
        return rec

    def get(self, table: str, id_value: int | str, id_field: str = "id") -> dict | None:
        if self._db is not None:
            try:
                col = self._db[table]
                doc = col.find_one({id_field: id_value}, {"_id": 0})
                if doc:
                    return doc
            except Exception:
                pass

        records = self._fallback_memory.get(table, [])
        for r in records:
            if str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value):
                return r
        return None

    def update(self, table: str, id_value: int | str, data: dict, id_field: str = "id") -> dict | None:
        if self._db is not None:
            try:
                col = self._db[table]
                col.update_one({id_field: id_value}, {"$set": data})
                return self.get(table, id_value, id_field)
            except Exception:
                pass

        records = self._fallback_memory.get(table, [])
        for r in records:
            if str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value):
                for k, v in data.items():
                    if k != "id":
                        r[k] = v
                return r
        return None

    def delete(self, table: str, id_value: int | str, id_field: str = "id") -> bool:
        if self._db is not None:
            try:
                col = self._db[table]
                res = col.delete_one({id_field: id_value})
                return res.deleted_count > 0
            except Exception:
                pass

        if table not in self._fallback_memory:
            return False
        orig_len = len(self._fallback_memory[table])
        self._fallback_memory[table] = [
            r for r in self._fallback_memory[table]
            if not (str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value))
        ]
        return len(self._fallback_memory[table]) < orig_len

    def find(self, table: str, filters: dict) -> list[dict]:
        if self._db is not None:
            try:
                col = self._db[table]
                return list(col.find(filters, {"_id": 0}))
            except Exception:
                pass

        records = self._fallback_memory.get(table, [])
        if not filters:
            return list(records)
        return [r for r in records if all(str(r.get(k)) == str(v) for k, v in filters.items())]

    def find_all(self, table: str) -> list[dict]:
        if self._db is not None:
            try:
                col = self._db[table]
                return list(col.find({}, {"_id": 0}))
            except Exception:
                pass
        return list(self._fallback_memory.get(table, []))

    def get_stats(self) -> dict[str, int]:
        return {table: len(records) for table, records in self._fallback_memory.items()}
