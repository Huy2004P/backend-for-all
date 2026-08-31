"""
Unit tests for BFA Dynamic Database-to-API Bridge.
"""

from bfa.bridge.crud import create_crud_service_for_table, generate_services_for_tables
from bfa.core.request import Request
from bfa.runtime.runtime import Runtime
from bfa.storage.memory import MemoryStorage


def test_crud_service_generation_and_execution():
    storage = MemoryStorage()
    storage.tables.clear()
    storage.counters.clear()

    # Generate CRUD Service for 'customers'
    customer_service = create_crud_service_for_table("customers", storage)
    runtime = Runtime()
    runtime.register_service(customer_service)

    # 1. Test Insert
    insert_res = runtime.handle_request(Request("customers", "insert", {
        "name": "Acme Corp",
        "industry": "Tech",
        "revenue": 5000000,
    }))
    assert insert_res.status == "SUCCESS"
    assert insert_res.data["created"]["id"] == 1
    assert insert_res.data["created"]["name"] == "Acme Corp"

    # 2. Test Find By ID
    find_res = runtime.handle_request(Request("customers", "find_by_id", {"id": 1}))
    assert find_res.status == "SUCCESS"
    assert find_res.data["record"]["name"] == "Acme Corp"

    # 3. Test Update
    update_res = runtime.handle_request(Request("customers", "update", {
        "id": 1,
        "revenue": 6000000,
    }))
    assert update_res.status == "SUCCESS"
    assert update_res.data["updated"]["revenue"] == 6000000

    # 4. Test Find All
    all_res = runtime.handle_request(Request("customers", "find_all", {"limit": 10}))
    assert all_res.status == "SUCCESS"
    assert all_res.data["total"] == 1

    # 5. Test Delete
    del_res = runtime.handle_request(Request("customers", "delete", {"id": 1}))
    assert del_res.status == "SUCCESS"
    assert storage.find_all("customers") == []


def test_generate_services_for_multiple_tables():
    storage = MemoryStorage()
    tables = ["invoices", "projects", "tasks"]
    services = generate_services_for_tables(tables, storage)

    assert len(services) == 3
    service_names = [s.name for s in services]
    assert "invoices" in service_names
    assert "projects" in service_names
    assert "tasks" in service_names
