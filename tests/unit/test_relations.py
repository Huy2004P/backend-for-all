"""
Unit tests for BFA Schema Synthesizer, Relational Seeder, and Foreign Key Expansion.
"""

from bfa.bridge.crud import create_crud_service_for_table, generate_services_for_tables
from bfa.catalog.schema_synthesizer import (
    auto_seed_relational_database,
    infer_system_relations,
    synthesize_table_schema,
)
from bfa.core.request import Request
from bfa.storage.memory import MemoryStorage


def test_synthesize_table_schema():
    orders_schema = synthesize_table_schema("orders")
    assert "user_id" in orders_schema["columns"]
    assert orders_schema["foreign_keys"].get("user_id") == "users"

    cart_schema = synthesize_table_schema("cart_items")
    assert "product_id" in cart_schema["foreign_keys"]
    assert cart_schema["foreign_keys"]["product_id"] == "products"


def test_infer_system_relations():
    tables = ["users", "products", "orders", "order_items"]
    relations = infer_system_relations(tables)
    assert len(relations) >= 3

    # Check orders -> users relation
    order_user_rel = next((r for r in relations if r["from_table"] == "orders" and r["to_table"] == "users"), None)
    assert order_user_rel is not None
    assert order_user_rel["from_column"] == "user_id"


def test_auto_seed_relational_database():
    storage = MemoryStorage()
    storage.tables.clear()  # Clear initial default seed
    tables = ["users", "products", "orders", "order_items"]

    # Initially storage is completely empty for these tables
    assert len(storage.find_all("orders")) == 0

    # Auto-seed
    seeded = auto_seed_relational_database(tables, storage, rows_per_table=2)
    assert seeded["orders"] == 2
    assert seeded["users"] == 2

    # Check seeded records
    users = storage.find_all("users")
    orders = storage.find_all("orders")
    assert len(users) == 2
    assert len(orders) == 2
    assert orders[0]["user_id"] == 1


def test_crud_expand_relations():
    storage = MemoryStorage()
    storage.tables.clear()
    # Seed user & product
    user = storage.insert("users", {"id": 1, "username": "huy_tester", "email": "huy@test.com"})
    product = storage.insert("products", {"id": 1, "name": "Mechanical Keyboard", "price": 200000})

    # Seed order pointing to user 1
    order = storage.insert("orders", {"id": 1, "user_id": 1, "total_amount": 500000, "status": "PAID"})

    # Create CRUD service for orders
    order_service = create_crud_service_for_table("orders", storage)

    # 1. Query with expand: ["user"]
    req = Request(service_name="orders", method_name="find_by_id", payload={"id": 1, "expand": ["user"]})
    resp = order_service.invoke(req)
    assert resp.status.name == "SUCCESS" if hasattr(resp.status, "name") else resp.status == "SUCCESS"
    assert "user" in resp.data["record"]
    assert resp.data["record"]["user"]["username"] == "huy_tester"

    # 2. Query find_all with expand: ["user"]
    req_all = Request(service_name="orders", method_name="find_all", payload={"expand": ["user"]})
    resp_all = order_service.invoke(req_all)
    assert len(resp_all.data["records"]) == 1
    assert "user" in resp_all.data["records"][0]
    assert resp_all.data["records"][0]["user"]["id"] == 1
