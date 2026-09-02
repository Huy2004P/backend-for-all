"""
Configuration system for Backend for All (BFA).

Manages server parameters, database connection settings, active blueprint,
and exposed tables persisted in 'bfa_config.json'.
"""

import json
from pathlib import Path

CONFIG_FILE_PATH = Path("bfa_config.json")

DEFAULT_CONFIG = {
    "server": {
        "host": "127.0.0.1",
        "port": 8080,
    },
    "blueprint": "b2c_store",
    "domain": "ecommerce",
    "database": {
        "driver": "json",  # "json", "memory", "postgres", "mysql", "mongodb"
        "data_file": "data/bfa_store.json",
        "host": "localhost",
        "port": 5432,
        "database_name": "bfa_store",
        "username": "postgres",
        "password": "",
    },
    "tables": [
        "users",
        "products",
        "orders",
        "cart_items",
    ],
}


class Settings:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self) -> dict:
        """Đọc file cấu hình bfa_config.json nếu có, nếu chưa thì tạo mặc định."""
        if not CONFIG_FILE_PATH.exists():
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()

        try:
            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                merged = DEFAULT_CONFIG.copy()
                if "server" in data:
                    merged["server"].update(data["server"])
                if "database" in data:
                    merged["database"].update(data["database"])
                if "tables" in data:
                    merged["tables"] = data["tables"]
                if "domain" in data:
                    merged["domain"] = data["domain"]
                if "blueprint" in data:
                    merged["blueprint"] = data["blueprint"]
                return merged
        except Exception:
            return DEFAULT_CONFIG.copy()

    def save_config(self, new_config: dict) -> None:
        """Lưu cấu hình ra file JSON."""
        self.config = new_config
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(new_config, f, indent=2, ensure_ascii=False)

    @property
    def blueprint(self) -> str:
        return self.config.get("blueprint", "b2c_store")

    @property
    def domain(self) -> str:
        return self.config.get("domain", "ecommerce")

    @property
    def database_driver(self) -> str:
        return self.config.get("database", {}).get("driver", "sqlite")

    @property
    def database_config(self) -> dict:
        return self.config.get("database", {})

    @property
    def server_config(self) -> dict:
        return self.config.get("server", {})

    @property
    def exposed_tables(self) -> list[str]:
        return self.config.get("tables", DEFAULT_CONFIG["tables"])


settings = Settings()
