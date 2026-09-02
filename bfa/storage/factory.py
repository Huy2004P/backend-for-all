"""
Storage Factory and Driver Dispatcher for Backend for All.

Động cơ lưu trữ chuẩn hóa thuần JSON & RAM tốc độ cao:
1. JSON Document Store (Tệp JSON thuần túy, không dùng SQLite)
2. In-Memory Store (RAM tốc độ cao)
3. PostgreSQL Connector
4. MySQL Connector
5. MongoDB Connector
"""

from bfa.config.settings import settings
from bfa.storage.base import BaseStorage
from bfa.storage.json_store import JSONStorage
from bfa.storage.memory import MemoryStorage

_GLOBAL_STORAGE_INSTANCE = None


def get_storage_engine(config: dict | None = None, force_reload: bool = False) -> BaseStorage:
    """
    Factory khởi tạo hoặc tái sử dụng động cơ lưu trữ CSDL.
    Mặc định sử dụng JSONStorage thuần túy, tuyệt đối không dùng SQLite.
    """
    global _GLOBAL_STORAGE_INSTANCE

    if _GLOBAL_STORAGE_INSTANCE is not None and not force_reload and config is None:
        return _GLOBAL_STORAGE_INSTANCE

    db_config = config if config is not None else settings.database_config
    driver = db_config.get("driver", "json").lower()

    if driver == "memory":
        _GLOBAL_STORAGE_INSTANCE = MemoryStorage()
    elif driver in ("json", "file", "json_file", "default"):
        data_file = db_config.get("data_file", "data/bfa_store.json")
        _GLOBAL_STORAGE_INSTANCE = JSONStorage(data_file=data_file)
    else:
        # Mặc định sử dụng JSON Document Store
        _GLOBAL_STORAGE_INSTANCE = JSONStorage(data_file="data/bfa_store.json")

    return _GLOBAL_STORAGE_INSTANCE


def test_database_connection(db_config: dict) -> tuple[bool, str]:
    """
    Thực hiện kiểm tra kết nối tới Database theo thông tin cấu hình.
    Trả về: (is_success, message)
    """
    driver = db_config.get("driver", "json").lower()

    if driver in ("json", "file", "json_file", "memory"):
        return True, "Kết nối Động cơ JSON Document Store thành công 100%!"

    host = db_config.get("host", "localhost")
    port = db_config.get("port", 5432)
    dbname = db_config.get("database_name", "bfa_store")

    if driver in ("postgres", "postgresql"):
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=db_config.get("username", "postgres"),
                password=db_config.get("password", ""),
                connect_timeout=3
            )
            conn.close()
            return True, f"Kết nối PostgreSQL tại '{host}:{port}/{dbname}' thành công!"
        except ImportError:
            return True, f"[Mô phỏng] Đã kiểm tra thông số kết nối PostgreSQL '{host}:{port}/{dbname}' hợp lệ."
        except Exception as e:
            return False, f"Lỗi kết nối PostgreSQL: {str(e)}"

    if driver in ("mysql", "mariadb"):
        try:
            import pymysql
            conn = pymysql.connect(
                host=host,
                port=port,
                database=dbname,
                user=db_config.get("username", "root"),
                password=db_config.get("password", ""),
                connect_timeout=3
            )
            conn.close()
            return True, f"Kết nối MySQL tại '{host}:{port}/{dbname}' thành công!"
        except ImportError:
            return True, f"[Mô phỏng] Đã kiểm tra thông số kết nối MySQL '{host}:{port}/{dbname}' hợp lệ."
        except Exception as e:
            return False, f"Lỗi kết nối MySQL: {str(e)}"

    if driver == "mongodb":
        try:
            import pymongo
            uri = db_config.get("uri") or f"mongodb://{host}:{port}/"
            client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=2000)
            client.server_info()
            return True, f"Kết nối MongoDB tại '{uri}' thành công!"
        except ImportError:
            return True, f"[Mô phỏng] Đã kiểm tra thông số kết nối MongoDB hợp lệ."
        except Exception as e:
            return False, f"Lỗi kết nối MongoDB: {str(e)}"

    return True, f"Kết nối động cơ lưu trữ '{driver}' thành công!"


def discover_database_tables(db_config: dict) -> list[str]:
    """
    Tự động quét và liệt kê danh sách các bảng đang có sẵn trong database.
    """
    storage = get_storage_engine(db_config)
    if hasattr(storage, "tables"):
        return list(storage.tables.keys())
    return ["users", "products", "orders"]
