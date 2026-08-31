"""
In-Memory Storage Adapter for Backend for All.

Fast, non-persistent RAM storage ideal for automated tests and isolated runs.
"""

from bfa.storage.base import BaseStorage


class MemoryStorage(BaseStorage):
    def __init__(self):
        self.tables = {}
        self.counters = {}
        self._seed_default_data()

    def _seed_default_data(self):
        self.insert("users", {
            "id": 1,
            "username": "vanbaphathuy",
            "email": "huy@bfa.dev",
            "balance": 1000000,
        })
        self.insert("products", {
            "id": 101,
            "name": "Mechanical Keyboard RGB",
            "price": 250000,
            "stock": 8,
        })
        self.insert("products", {
            "id": 102,
            "name": "Wireless Gaming Mouse",
            "price": 150000,
            "stock": 15,
        })

    def insert(self, table: str, data: dict) -> dict:
        if table not in self.tables:
            self.tables[table] = []
            self.counters[table] = 1

        record = data.copy()
        if "id" not in record:
            record["id"] = self.counters[table]
            self.counters[table] += 1
        if "order_id" not in record and table == "orders":
            record["order_id"] = record["id"]

        self.tables[table].append(record)
        return record

    def get(self, table: str, id_value: int | str, id_field: str = "id") -> dict | None:
        records = self.tables.get(table, [])
        for r in records:
            if str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value):
                return r
        return None

    def find_all(self, table: str) -> list[dict]:
        return list(self.tables.get(table, []))

    def find(self, table: str, filter_dict: dict) -> list[dict]:
        records = self.tables.get(table, [])
        matching = []
        for r in records:
            match = True
            for k, v in filter_dict.items():
                if r.get(k) != v:
                    match = False
                    break
            if match:
                matching.append(r)
        return matching

    def update(self, table: str, id_value: int | str, updates: dict, id_field: str = "id") -> dict | None:
        records = self.tables.get(table, [])
        for r in records:
            if str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value):
                r.update(updates)
                return r
        return None

    def delete(self, table: str, id_value: int | str, id_field: str = "id") -> bool:
        records = self.tables.get(table, [])
        for i, r in enumerate(records):
            if str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value):
                records.pop(i)
                return True
        return False

    def get_stats(self) -> dict:
        return {k: len(v) for k, v in self.tables.items()}

    def __repr__(self) -> str:
        return "MemoryStorage(RAM)"
