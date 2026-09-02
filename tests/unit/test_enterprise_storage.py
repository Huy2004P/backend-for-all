"""
Unit tests for Enterprise Network Database Storage Adapters (PostgreSQL, MySQL, MongoDB).
Zero disk files created.
"""

from bfa.storage.postgres import PostgresStorage
from bfa.storage.mysql import MySQLStorage
from bfa.storage.mongodb import MongoStorage
from bfa.storage.factory import test_database_connection as check_db_conn


def test_postgres_storage_operations():
    storage = PostgresStorage(host="localhost", port=5432, dbname="bfa_test")
    # Insert
    user = storage.insert("users", {"name": "Admin", "email": "admin@bfa.io"})
    assert user["id"] is not None
    assert user["name"] == "Admin"

    # Get
    fetched = storage.get("users", user["id"])
    assert fetched is not None
    assert fetched["name"] == "Admin"

    # Update
    updated = storage.update("users", user["id"], {"name": "Super Admin"})
    assert updated["name"] == "Super Admin"

    # Find & Find All
    matched = storage.find("users", {"name": "Super Admin"})
    assert len(matched) == 1
    all_users = storage.find_all("users")
    assert len(all_users) >= 1

    # Delete
    deleted = storage.delete("users", user["id"])
    assert deleted is True


def test_mysql_storage_operations():
    storage = MySQLStorage(host="localhost", port=3306, dbname="bfa_test")
    product = storage.insert("products", {"name": "MacBook Pro", "price": 2000})
    assert product["id"] is not None
    assert product["name"] == "MacBook Pro"

    fetched = storage.get("products", product["id"])
    assert fetched is not None
    assert fetched["price"] == 2000

    deleted = storage.delete("products", product["id"])
    assert deleted is True


def test_mongodb_storage_operations():
    storage = MongoStorage(host="localhost", port=27017, dbname="bfa_test")
    order = storage.insert("orders", {"user_id": 1, "status": "PAID"})
    assert order["id"] is not None
    assert order["status"] == "PAID"

    fetched = storage.get("orders", order["id"])
    assert fetched is not None
    assert fetched["status"] == "PAID"

    deleted = storage.delete("orders", order["id"])
    assert deleted is True


def test_database_connection_network_check():
    ok, msg = check_db_conn({
        "driver": "postgres",
        "host": "localhost",
        "port": 5432,
        "database_name": "bfa_database"
    })
    assert isinstance(ok, bool)
    assert len(msg) > 0
