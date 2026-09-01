"""
Integration test for BFA Web Studio endpoints.
"""

import json
import time
from urllib.request import Request, urlopen

from bfa.storage.memory import MemoryStorage
from main import setup_application, start_http_server


def test_web_studio_endpoints():
    storage = MemoryStorage()
    runtime = setup_application(storage=storage, blueprint_key="b2c_store")
    transport = start_http_server(runtime, host="127.0.0.1", port=8099)
    time.sleep(0.1)

    try:
        # 1. Test GET / -> Should return Web Studio HTML
        with urlopen("http://127.0.0.1:8099/") as resp:
            html = resp.read().decode("utf-8")
            assert "<title>BFA Studio" in html
            assert "Kiến Trúc Mẫu" in html

        # 1b. Test GET /tutorial -> Should return Dedicated Tutorial Documentation HTML
        with urlopen("http://127.0.0.1:8099/tutorial") as resp:
            tut_html = resp.read().decode("utf-8")
            assert "BFA Docs" in tut_html
            assert "Tài Liệu Hướng Dẫn Sử Dụng Backend for All" in tut_html

        # 2. Test GET /api/bfa/catalog -> Should return 100 blueprints
        with urlopen("http://127.0.0.1:8099/api/bfa/catalog") as resp:
            data = json.loads(resp.read().decode("utf-8"))
            assert data["status"] == "SUCCESS"
            assert len(data["blueprints"]) >= 100
            assert len(data["categories"]) == 10

        # 3. Test POST /api/bfa/custom-system -> Create infinite custom blueprint
        custom_req = Request(
            "http://127.0.0.1:8099/api/bfa/custom-system",
            data=json.dumps({
                "name": "Hệ Thống Bán Vé Máy Bay Tích Hợp",
                "category": "travel",
                "tables": ["flights", "tickets", "passengers"],
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(custom_req) as resp:
            custom_data = json.loads(resp.read().decode("utf-8"))
            assert custom_data["status"] == "SUCCESS"
            assert "flights" in custom_data["active_services"]
            assert "tickets" in custom_data["active_services"]

        # 3b. Test POST /api/bfa/cherry-pick -> Select individual tables
        cherry_req = Request(
            "http://127.0.0.1:8099/api/bfa/cherry-pick",
            data=json.dumps({
                "tables": ["users", "wallets"],
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(cherry_req) as resp:
            cherry_data = json.loads(resp.read().decode("utf-8"))
            assert cherry_data["status"] == "SUCCESS"
            assert cherry_data["active_services"] == ["users", "wallets"]

        # 4. Test POST /api/bfa/launch -> Launch #61 ride_hailing
        req = Request(
            "http://127.0.0.1:8099/api/bfa/launch",
            data=json.dumps({"blueprint_key": "ride_hailing"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(req) as resp:
            launch_data = json.loads(resp.read().decode("utf-8"))
            assert launch_data["status"] == "SUCCESS"
            assert "rides" in launch_data["active_services"]
            assert "drivers" in launch_data["active_services"]

        # 5. Test POST /api/bfa/add-custom-api -> Add a brand new custom API method
        add_api_req = Request(
            "http://127.0.0.1:8099/api/bfa/add-custom-api",
            data=json.dumps({
                "service": "users",
                "method": "change_password",
                "display_name": "Đổi Mật Khẩu Người Dùng",
                "description": "API cập nhật mật khẩu mới.",
                "action_type": "custom",
                "sample_payload": {"user_id": 1, "new_password": "secret"},
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(add_api_req) as resp:
            add_data = json.loads(resp.read().decode("utf-8"))
            assert add_data["status"] == "SUCCESS"
            assert add_data["endpoint"] == "/api/users/change_password"

        # Test executing the newly created custom API
        exec_custom_req = Request(
            "http://127.0.0.1:8099/api/users/change_password",
            data=json.dumps({"user_id": 1, "new_password": "secret"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(exec_custom_req) as resp:
            exec_data = json.loads(resp.read().decode("utf-8"))
            assert exec_data["status"] == "SUCCESS"
            assert "executed_method" in exec_data["data"]

        # 6. Test POST /api/bfa/remove-api -> Delete custom API
        rm_api_req = Request(
            "http://127.0.0.1:8099/api/bfa/remove-api",
            data=json.dumps({"service": "users", "method": "change_password"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(rm_api_req) as resp:
            rm_data = json.loads(resp.read().decode("utf-8"))
            assert rm_data["status"] == "SUCCESS"

        # 7. Test GET /api/bfa/flow-stats -> Live Topology Info
        flow_req = Request("http://127.0.0.1:8099/api/bfa/flow-stats")
        with urlopen(flow_req) as resp:
            flow_data = json.loads(resp.read().decode("utf-8"))
            assert flow_data["status"] == "SUCCESS"
            assert "services" in flow_data
            assert flow_data["services_count"] >= 1
            assert flow_data["status_mode"] == "ACTIVE"

        # 7b. Test GET /api/bfa/openapi.json -> OpenAPI 3.0 Document
        with urlopen("http://127.0.0.1:8099/api/bfa/openapi.json") as resp:
            openapi_data = json.loads(resp.read().decode("utf-8"))
            assert openapi_data["openapi"] == "3.0.0"
            assert "paths" in openapi_data
            assert len(openapi_data["paths"]) > 0

        # 7c. Test GET /api/bfa/android-contract -> Android specific contract
        with urlopen("http://127.0.0.1:8099/api/bfa/android-contract") as resp:
            android_data = json.loads(resp.read().decode("utf-8"))
            assert android_data["status"] == "SUCCESS"
            assert "android_configuration" in android_data
            assert "emulator_base_url" in android_data["android_configuration"]
            assert "tables" in android_data

        # 7d. Test GET /api/bfa/postman.json -> Postman Collection
        with urlopen("http://127.0.0.1:8099/api/bfa/postman.json") as resp:
            pm_data = json.loads(resp.read().decode("utf-8"))
            assert "info" in pm_data
            assert "item" in pm_data

        # 7e. Test POST /api/bfa/snapshot -> One-Shot Composite data for all tables
        snapshot_req = Request(
            "http://127.0.0.1:8099/api/bfa/snapshot",
            data=json.dumps({"tables": ["rides", "drivers"], "limit": 5}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(snapshot_req) as resp:
            snap_data = json.loads(resp.read().decode("utf-8"))
            assert snap_data["status"] == "SUCCESS"
            assert "rides" in snap_data["data"]
            assert "drivers" in snap_data["data"]

        # 7f. Test POST /api/bfa/batch -> Multi-query bundle
        batch_req = Request(
            "http://127.0.0.1:8099/api/bfa/batch",
            data=json.dumps({
                "queries": {
                    "all_rides": {"service": "rides", "method": "find_all", "payload": {"limit": 2}},
                    "all_drivers": {"service": "drivers", "method": "find_all", "payload": {"limit": 2}},
                }
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(batch_req) as resp:
            batch_data = json.loads(resp.read().decode("utf-8"))
            assert batch_data["status"] == "SUCCESS"
            assert "all_rides" in batch_data["data"]
            assert "all_drivers" in batch_data["data"]

        # 7g. Test GET /api/bfa/contract -> Universal Contract Specification
        with urlopen("http://127.0.0.1:8099/api/bfa/contract") as resp:
            contract_data = json.loads(resp.read().decode("utf-8"))
            assert contract_data["status"] == "SUCCESS"
            assert "universal_endpoint" in contract_data

        # 7h. Test POST /api/bfa/call -> Universal Single Invocation Protocol
        uni_req = Request(
            "http://127.0.0.1:8099/api/bfa/call",
            data=json.dumps({
                "service": "rides",
                "action": "find_all",
                "payload": {"limit": 3}
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(uni_req) as resp:
            uni_data = json.loads(resp.read().decode("utf-8"))
            assert uni_data["status"] == "SUCCESS"
            assert "records" in uni_data["data"]

        # 7i. Test POST /api/bfa/call with Snapshot action
        uni_snap_req = Request(
            "http://127.0.0.1:8099/api/bfa/call",
            data=json.dumps({
                "action": "snapshot",
                "payload": {"tables": ["rides", "drivers"], "limit": 2}
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(uni_snap_req) as resp:
            uni_snap_data = json.loads(resp.read().decode("utf-8"))
            assert uni_snap_data["status"] == "SUCCESS"
            assert "rides" in uni_snap_data["data"]

        # 7j. Test GET /api/bfa/schema-relations -> Relational Schema Graph
        with urlopen("http://127.0.0.1:8099/api/bfa/schema-relations") as resp:
            rel_data = json.loads(resp.read().decode("utf-8"))
            assert rel_data["status"] == "SUCCESS"
            assert "table_schemas" in rel_data
            assert "relations" in rel_data

        # 7k. Test POST /api/bfa/auto-seed -> Auto seed relational database
        seed_req = Request(
            "http://127.0.0.1:8099/api/bfa/auto-seed",
            data=json.dumps({"rows_per_table": 2}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(seed_req) as resp:
            seed_data = json.loads(resp.read().decode("utf-8"))
            assert seed_data["status"] == "SUCCESS"

        # 7l. Test POST /api/rides/find_all with expand: ["passenger", "driver"]
        expand_req = Request(
            "http://127.0.0.1:8099/api/rides/find_all",
            data=json.dumps({"expand": ["passenger", "driver"]}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(expand_req) as resp:
            exp_data = json.loads(resp.read().decode("utf-8"))
            assert exp_data["status"] == "SUCCESS"
            assert len(exp_data["data"]["records"]) > 0

        # 8. Test POST /api/bfa/stop -> Stop/Deactivate active system
        stop_req = Request(
            "http://127.0.0.1:8099/api/bfa/stop",
            data=json.dumps({}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(stop_req) as resp:
            stop_data = json.loads(resp.read().decode("utf-8"))
            assert stop_data["status"] == "SUCCESS"
            assert stop_data["active_services"] == []
    finally:
        transport.server.shutdown()
