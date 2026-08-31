"""
Integration tests for BFA Universal Database-to-API Bridge and Multi-Service Systems.
"""

import json
import time
import urllib.request

from bfa.core.request import Request
from bfa.storage.memory import MemoryStorage
from main import setup_application, start_http_server


def test_ecommerce_multi_service_workflow():
    """Test full multi-service checkout workflow using auto-generated CRUD and RPC methods."""
    storage = MemoryStorage()
    storage.tables.clear()
    storage.counters.clear()

    runtime = setup_application(storage=storage, table_names=["users", "products", "orders"])

    # 1. Insert a new User via auto-generated CRUD API
    reg_req = Request("users", "insert", {
        "username": "alice",
        "email": "alice@bfa.dev",
        "balance": 500000,
    })
    reg_res = runtime.handle_request(reg_req)
    assert reg_res.status == "SUCCESS"
    assert reg_res.data["created"]["id"] == 1
    assert reg_res.data["created"]["balance"] == 500000

    # 2. Insert a Product via auto-generated CRUD API
    prod_req = Request("products", "insert", {
        "name": "Mechanical Keyboard Pro",
        "price": 200000,
        "stock": 5,
    })
    prod_res = runtime.handle_request(prod_req)
    assert prod_res.status == "SUCCESS"
    assert prod_res.data["created"]["id"] == 1
    assert prod_res.data["created"]["stock"] == 5

    # 3. Place an Order for 2 keyboards (Total: 400,000 VND)
    order_req = Request("orders", "place_order", {
        "user_id": 1,
        "product_id": 1,
        "quantity": 2,
    })
    order_res = runtime.handle_request(order_req)
    assert order_res.status == "SUCCESS"
    assert order_res.data["order"]["total_amount"] == 400000
    assert order_res.data["order"]["status"] == "COMPLETED"

    # 4. Verify User Balance via find_by_id: 500,000 - 400,000 = 100,000 VND
    profile_res = runtime.handle_request(Request("users", "find_by_id", {"id": 1}))
    assert profile_res.data["record"]["balance"] == 100000

    # 5. Verify Product Stock via find_all: 5 - 2 = 3
    catalog_res = runtime.handle_request(Request("products", "find_all", {}))
    assert catalog_res.data["records"][0]["stock"] == 3

    # 6. Test Insufficient Funds: try buying 1 more keyboard (200,000 > 100,000 balance)
    overdraft_req = Request("orders", "place_order", {
        "user_id": 1,
        "product_id": 1,
        "quantity": 1,
    })
    overdraft_res = runtime.handle_request(overdraft_req)
    assert overdraft_res.status == "ERROR"
    assert "Insufficient funds" in overdraft_res.error

    # 7. Deposit 300,000 VND and retry
    deposit_res = runtime.handle_request(Request("users", "deposit", {"user_id": 1, "amount": 300000}))
    assert deposit_res.status == "SUCCESS"
    assert deposit_res.data["new_balance"] == 400000

    # 8. Retry order with new balance -> Success
    retry_res = runtime.handle_request(overdraft_req)
    assert retry_res.status == "SUCCESS"
    assert retry_res.data["order"]["total_amount"] == 200000


def test_ecommerce_http_network_order_api():
    """Test the multi-service E-Commerce system over HTTP transport."""
    storage = MemoryStorage()
    runtime = setup_application(storage=storage, table_names=["users", "products", "orders"])
    transport = start_http_server(runtime, host="127.0.0.1", port=8093)

    try:
        time.sleep(0.1)
        url = "http://127.0.0.1:8093/api/users/find_all"
        payload = json.dumps({"limit": 10}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")

        with urllib.request.urlopen(req) as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode("utf-8"))
            assert data["status"] == "SUCCESS"
            assert "records" in data["data"]
    finally:
        transport.server.shutdown()
        transport.server.server_close()
