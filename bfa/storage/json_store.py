"""
JSON File Document Storage Adapter for Backend for All.

Lưu trữ dữ liệu dạng JSON thuần túy (Human-readable JSON Documents),
hoàn toàn KHÔNG dùng SQLite hay tệp nhị phân, đảm bảo trong suốt,
dễ đọc, dễ sao lưu và tương thích 100% với mọi hệ điều hành.
"""

import json
import os
import threading
from pathlib import Path
from typing import Any
from bfa.storage.base import BaseStorage


class JSONStorage(BaseStorage):
    def __init__(self, data_file: str = "data/bfa_store.json"):
        self.data_file = Path(data_file)
        self._lock = threading.Lock()
        self.tables: dict[str, list[dict[str, Any]]] = {}
        self.counters: dict[str, int] = {}
        self._init_storage()

    def _init_storage(self) -> None:
        """Khởi tạo thư mục và nạp dữ liệu từ file JSON nếu đã tồn tại."""
        os.makedirs(self.data_file.parent, exist_ok=True)
        if self.data_file.exists():
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        self.tables = data.get("tables", {})
                        self.counters = data.get("counters", {})
            except Exception:
                self.tables = {}
                self.counters = {}
        else:
            self._save_to_disk()

    def _save_to_disk(self) -> None:
        """Ghi dữ liệu ra file JSON an toàn."""
        try:
            temp_file = self.data_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump({
                    "tables": self.tables,
                    "counters": self.counters
                }, f, ensure_ascii=False, indent=2)
            if temp_file.exists():
                temp_file.replace(self.data_file)
        except Exception as e:
            print(f"[CẢNH BÁO JSONStorage] Không thể ghi file: {e}")

    def insert(self, table: str, data: dict) -> dict:
        with self._lock:
            if table not in self.tables:
                self.tables[table] = []
                self.counters[table] = 1

            record = data.copy()
            if "id" not in record or record["id"] is None:
                record["id"] = self.counters[table]
                self.counters[table] += 1
            else:
                try:
                    num_id = int(record["id"])
                    if num_id >= self.counters[table]:
                        self.counters[table] = num_id + 1
                except (ValueError, TypeError):
                    pass

            # Tự động gán khóa phụ nếu cần
            if table == "orders" and "order_id" not in record:
                record["order_id"] = record["id"]

            self.tables[table].append(record)
            self._save_to_disk()
            return record

    def get(self, table: str, id_value: int | str, id_field: str = "id") -> dict | None:
        records = self.tables.get(table, [])
        for r in records:
            if str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value):
                return r
        return None

    def update(self, table: str, id_value: int | str, data: dict, id_field: str = "id") -> dict | None:
        with self._lock:
            records = self.tables.get(table, [])
            for r in records:
                if str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value):
                    for k, v in data.items():
                        if k != "id":
                            r[k] = v
                    self._save_to_disk()
                    return r
            return None

    def delete(self, table: str, id_value: int | str, id_field: str = "id") -> bool:
        with self._lock:
            if table not in self.tables:
                return False
            initial_len = len(self.tables[table])
            self.tables[table] = [
                r for r in self.tables[table]
                if not (str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value))
            ]
            deleted = len(self.tables[table]) < initial_len
            if deleted:
                self._save_to_disk()
            return deleted

    def find(self, table: str, filters: dict) -> list[dict]:
        records = self.tables.get(table, [])
        if not filters:
            return list(records)

        matched = []
        for r in records:
            match = True
            for k, v in filters.items():
                if str(r.get(k)) != str(v):
                    match = False
                    break
            if match:
                matched.append(r)
        return matched

    def find_all(self, table: str) -> list[dict]:
        return list(self.tables.get(table, []))

    def get_stats(self) -> dict[str, int]:
        return {table: len(records) for table, records in self.tables.items()}

    def clear(self, table: str | None = None) -> None:
        with self._lock:
            if table:
                self.tables[table] = []
                self.counters[table] = 1
            else:
                self.tables.clear()
                self.counters.clear()
            self._save_to_disk()
