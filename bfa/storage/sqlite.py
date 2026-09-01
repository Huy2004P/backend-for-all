"""
SQLite Storage Adapter for Backend for All.

Implements BaseStorage using Python's built-in sqlite3 standard library.
Stores data persistently in a local .db file.
"""

import json
import sqlite3
from pathlib import Path
from bfa.storage.base import BaseStorage


class SQLiteStorage(BaseStorage):
    def __init__(self, db_path: str = "bfa_database.db"):
        self.db_path = str(Path(db_path))
        self._init_tables()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self) -> None:
        """Tự động khởi tạo cấu trúc bảng SQLite nếu chưa tồn tại."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Bảng generic document store: (id, table_name, data_json)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bfa_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT NOT NULL,
                    data_json TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_bfa_table ON bfa_documents(table_name)
            """)
            conn.commit()

    def _seed_default_data_if_empty(self) -> None:
        """Nạp dữ liệu mẫu ban đầu nếu database hoàn toàn trống."""
        stats = self.get_stats()
        if stats.get("users", 0) == 0 and stats.get("products", 0) == 0:
            # Seed 1 user
            self.insert("users", {
                "username": "vanbaphathuy",
                "email": "huy@bfa.dev",
                "balance": 1000000,
            })
            # Seed 2 products
            self.insert("products", {
                "name": "Mechanical Keyboard RGB",
                "price": 250000,
                "stock": 8,
            })
            self.insert("products", {
                "name": "Wireless Gaming Mouse",
                "price": 150000,
                "stock": 15,
            })

    def insert(self, table: str, data: dict) -> dict:
        record = data.copy()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Insert temporary to get AUTOINCREMENT id if 'id' not provided
            cursor.execute(
                "INSERT INTO bfa_documents (table_name, data_json) VALUES (?, ?)",
                (table, json.dumps(record, ensure_ascii=False)),
            )
            generated_id = cursor.lastrowid
            if "id" not in record:
                record["id"] = generated_id
            if "order_id" not in record and table == "orders":
                record["order_id"] = generated_id

            # Update with final id included
            cursor.execute(
                "UPDATE bfa_documents SET data_json = ? WHERE id = ?",
                (json.dumps(record, ensure_ascii=False), generated_id),
            )
            conn.commit()
        return record

    def get(self, table: str, id_value: int | str, id_field: str = "id") -> dict | None:
        records = self.find_all(table)
        for r in records:
            if str(r.get(id_field)) == str(id_value) or str(r.get("id")) == str(id_value):
                return r
        return None

    def find_all(self, table: str) -> list[dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, data_json FROM bfa_documents WHERE table_name = ? ORDER BY id ASC",
                (table,),
            )
            rows = cursor.fetchall()
            results = []
            for row in rows:
                try:
                    data = json.loads(row["data_json"])
                    if "id" not in data:
                        data["id"] = row["id"]
                    results.append(data)
                except Exception:
                    continue
            return results

    def find(self, table: str, filter_dict: dict) -> list[dict]:
        all_records = self.find_all(table)
        matching = []
        for r in all_records:
            match = True
            for k, v in filter_dict.items():
                if r.get(k) != v:
                    match = False
                    break
            if match:
                matching.append(r)
        return matching

    def update(self, table: str, id_value: int | str, updates: dict, id_field: str = "id") -> dict | None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, data_json FROM bfa_documents WHERE table_name = ?",
                (table,),
            )
            rows = cursor.fetchall()
            for row in rows:
                doc = json.loads(row["data_json"])
                if str(doc.get(id_field)) == str(id_value) or str(doc.get("id")) == str(id_value) or str(row["id"]) == str(id_value):
                    doc.update(updates)
                    cursor.execute(
                        "UPDATE bfa_documents SET data_json = ? WHERE id = ?",
                        (json.dumps(doc, ensure_ascii=False), row["id"]),
                    )
                    conn.commit()
                    return doc
        return None

    def delete(self, table: str, id_value: int | str, id_field: str = "id") -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, data_json FROM bfa_documents WHERE table_name = ?",
                (table,),
            )
            rows = cursor.fetchall()
            for row in rows:
                doc = json.loads(row["data_json"])
                if str(doc.get(id_field)) == str(id_value) or str(row["id"]) == str(id_value):
                    cursor.execute("DELETE FROM bfa_documents WHERE id = ?", (row["id"],))
                    conn.commit()
                    return True
        return False

    def get_stats(self) -> dict:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT table_name, COUNT(*) as count FROM bfa_documents GROUP BY table_name")
            rows = cursor.fetchall()
            return {row["table_name"]: row["count"] for row in rows}

    def __repr__(self) -> str:
        return f"SQLiteStorage(path='{self.db_path}')"
