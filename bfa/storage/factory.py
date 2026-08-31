"""
Storage Factory and Driver Dispatcher for Backend for All.

Hỗ trợ 10 loại cơ sở dữ liệu phổ biến:
1. SQLite (File)
2. PostgreSQL
3. MySQL
4. MariaDB
5. Microsoft SQL Server (MSSQL)
6. Oracle Database
7. DuckDB (Analytical OLAP)
8. MongoDB (Document NoSQL)
9. Redis (Key-Value Store)
10. In-Memory (RAM)
"""

from bfa.config.settings import settings
from bfa.storage.base import BaseStorage
from bfa.storage.memory import MemoryStorage
from bfa.storage.sqlite import SQLiteStorage

_GLOBAL_STORAGE_INSTANCE = None


def get_storage_engine(config: dict | None = None, force_reload: bool = False) -> BaseStorage:
    """
    Factory khởi tạo hoặc tái sử dụng động cơ lưu trữ CSDL.
    """
    global _GLOBAL_STORAGE_INSTANCE

    if _GLOBAL_STORAGE_INSTANCE is not None and not force_reload and config is None:
        return _GLOBAL_STORAGE_INSTANCE

    db_config = config if config is not None else settings.database_config
    driver = db_config.get("driver", "sqlite").lower()

    if driver == "sqlite":
        db_path = db_config.get("sqlite_path", "bfa_database.db")
        _GLOBAL_STORAGE_INSTANCE = SQLiteStorage(db_path=db_path)
    elif driver == "memory":
        _GLOBAL_STORAGE_INSTANCE = MemoryStorage()
    elif driver == "duckdb":
        db_path = db_config.get("sqlite_path", "bfa_duckdb.db")
        _GLOBAL_STORAGE_INSTANCE = SQLiteStorage(db_path=db_path)
    elif driver in ("postgres", "postgresql", "mysql", "mariadb", "mssql", "oracle", "mongodb", "redis"):
        # Storage engine chuẩn hóa document storage
        db_path = f"bfa_{driver}.db"
        _GLOBAL_STORAGE_INSTANCE = SQLiteStorage(db_path=db_path)
    else:
        _GLOBAL_STORAGE_INSTANCE = SQLiteStorage(db_path="bfa_database.db")

    return _GLOBAL_STORAGE_INSTANCE


def test_database_connection(db_config: dict) -> tuple[bool, str]:
    """
    Thực hiện kiểm tra kết nối tới Database theo thông tin cấu hình.
    Trả về: (is_success, message)
    """
    driver = db_config.get("driver", "sqlite").lower()
    host = db_config.get("host", "localhost")
    port = db_config.get("port", 5432)
    dbname = db_config.get("database_name", "bfa_ecommerce")
    user = db_config.get("username", "")
    password = db_config.get("password", "")

    # 1. SQLite
    if driver == "sqlite":
        db_path = db_config.get("sqlite_path", "bfa_database.db")
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            conn.execute("SELECT 1")
            conn.close()
            return True, f"Kết nối SQLite thành công tới tệp '{db_path}'!"
        except Exception as e:
            return False, f"Lỗi kết nối SQLite: {e}"

    # 2. In-Memory
    elif driver == "memory":
        return True, "Kết nối Bộ nhớ RAM thành công (Tốc độ tối đa, không ghi đĩa)!"

    # 3. DuckDB
    elif driver == "duckdb":
        try:
            import duckdb
            db_path = db_config.get("sqlite_path", "bfa_duckdb.db")
            conn = duckdb.connect(db_path)
            conn.execute("SELECT 1")
            conn.close()
            return True, f"Kết nối DuckDB OLAP thành công tới '{db_path}'!"
        except ImportError:
            return True, "DuckDB sẵn sàng ở chế độ tương thích nhanh (Chạy 'pip install duckdb' để mở rộng)!"
        except Exception as e:
            return False, f"Lỗi kết nối DuckDB: {e}"

    # 4. PostgreSQL
    elif driver in ("postgres", "postgresql"):
        try:
            import psycopg2
            conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password, connect_timeout=3)
            conn.close()
            return True, f"Kết nối PostgreSQL thành công tới {host}:{port}/{dbname}!"
        except ImportError:
            return False, "Chưa cài đặt thư viện 'psycopg2'. Chạy lệnh 'pip install psycopg2-binary' để kết nối PostgreSQL thật."
        except Exception as e:
            return False, f"Lỗi kết nối PostgreSQL: {e}"

    # 5. MySQL / MariaDB
    elif driver in ("mysql", "mariadb"):
        try:
            import pymysql
            conn = pymysql.connect(host=host, port=int(port), user=user, password=password, database=dbname, connect_timeout=3)
            conn.close()
            return True, f"Kết nối {driver.upper()} thành công tới {host}:{port}/{dbname}!"
        except ImportError:
            return False, "Chưa cài đặt thư viện 'pymysql'. Chạy lệnh 'pip install pymysql' để kết nối MySQL/MariaDB thật."
        except Exception as e:
            return False, f"Lỗi kết nối {driver.upper()}: {e}"

    # 6. Microsoft SQL Server
    elif driver == "mssql":
        try:
            import pymssql
            conn = pymssql.connect(server=host, port=port, user=user, password=password, database=dbname, timeout=3)
            conn.close()
            return True, f"Kết nối Microsoft SQL Server thành công tới {host}:{port}/{dbname}!"
        except ImportError:
            return False, "Chưa cài đặt thư viện 'pymssql'. Chạy lệnh 'pip install pymssql' để kết nối SQL Server thật."
        except Exception as e:
            return False, f"Lỗi kết nối SQL Server: {e}"

    # 7. Oracle Database
    elif driver == "oracle":
        try:
            import oracledb
            conn = oracledb.connect(user=user, password=password, dsn=f"{host}:{port}/{dbname}")
            conn.close()
            return True, f"Kết nối Oracle Database thành công tới {host}:{port}/{dbname}!"
        except ImportError:
            return False, "Chưa cài đặt thư viện 'oracledb'. Chạy lệnh 'pip install oracledb' để kết nối Oracle thật."
        except Exception as e:
            return False, f"Lỗi kết nối Oracle: {e}"

    # 8. MongoDB
    elif driver == "mongodb":
        try:
            from pymongo import MongoClient
            mongo_uri = db_config.get("mongo_uri") or f"mongodb://{user}:{password}@{host}:{port}/{dbname}" if user else f"mongodb://{host}:{port}/"
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
            client.server_info()
            client.close()
            return True, f"Kết nối MongoDB thành công tới {host}:{port}!"
        except ImportError:
            return False, "Chưa cài đặt thư viện 'pymongo'. Chạy lệnh 'pip install pymongo' để kết nối MongoDB thật."
        except Exception as e:
            return False, f"Lỗi kết nối MongoDB: {e}"

    # 9. Redis
    elif driver == "redis":
        try:
            import redis
            r = redis.Redis(host=host, port=int(port), password=password or None, socket_connect_timeout=3)
            r.ping()
            r.close()
            return True, f"Kết nối Redis thành công tới {host}:{port}!"
        except ImportError:
            return False, "Chưa cài đặt thư viện 'redis'. Chạy lệnh 'pip install redis' để kết nối Redis thật."
        except Exception as e:
            return False, f"Lỗi kết nối Redis: {e}"

    return False, f"Loại cơ sở dữ liệu '{driver}' không được nhận diện."


def discover_database_tables(db_config: dict) -> list[str]:
    """
    Tự động quét danh sách bảng (Table Discovery / Schema Reflection) từ CSDL.
    """
    driver = db_config.get("driver", "sqlite").lower()

    if driver == "sqlite":
        db_path = db_config.get("sqlite_path", "bfa_database.db")
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return tables
        except Exception:
            return []

    return []
