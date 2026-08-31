"""
HTTP Transport adapter for Backend for All.

Bridges external HTTP network requests (cURL, Postman, Web clients) to internal
BFA Runtime invocations, and serves the BFA Studio Web Dashboard and Tutorial Documentation.
"""

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

from bfa.bridge.crud import generate_services_for_tables
from bfa.catalog.loader import mount_blueprint_to_runtime
from bfa.catalog.registry import CATEGORIES, list_all_blueprints
from bfa.config.settings import settings
from bfa.core.method import Method
from bfa.core.request import Request
from bfa.core.service import Service
from bfa.protocol.decoder import JSONDecoder
from bfa.protocol.encoder import JSONEncoder
from bfa.runtime.runtime import Runtime
from bfa.storage.factory import discover_database_tables, get_storage_engine, test_database_connection
from bfa.transport.base import BaseTransport

WEB_INDEX_PATH = Path(__file__).parent.parent / "web" / "index.html"
WEB_TUTORIAL_PATH = Path(__file__).parent.parent / "web" / "tutorial.html"


def create_bfa_http_handler(runtime: Runtime, encoder: JSONEncoder, decoder: JSONDecoder):
    """
    Factory function to create a BaseHTTPRequestHandler bound to a specific
    BFA Runtime, Encoder, and Decoder.
    """

    class BFAHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            clean_path = parsed.path.rstrip("/")

            # 1. Phục vụ giao diện BFA Studio
            if clean_path in ("", "/", "/dashboard", "/studio", "/index.html"):
                self._serve_web_studio()
                return

            # 2. Phục vụ trang Hướng Dẫn & Tài Liệu Riêng Biệt: GET /tutorial
            if clean_path in ("/tutorial", "/docs", "/huong-dan", "/tutorial.html"):
                self._serve_web_tutorial()
                return

            # 3. Danh mục 100 Bản thiết kế: GET /api/bfa/catalog
            if clean_path == "/api/bfa/catalog":
                self._send_encoded_response(200, {
                    "status": "SUCCESS",
                    "active_blueprint": settings.blueprint,
                    "active_driver": settings.database_driver,
                    "categories": CATEGORIES,
                    "blueprints": list_all_blueprints(),
                })
                return

            # 4. Danh sách dịch vụ đang mở: GET /api/bfa/services
            if clean_path == "/api/bfa/services":
                services_info = {}
                for s_name, s_obj in runtime.services.items():
                    methods_list = []
                    for m_name, m_obj in s_obj.methods.items():
                        schema_fields = {}
                        if m_obj.input_schema and hasattr(m_obj.input_schema, "fields"):
                            schema_fields = {k: v.__name__ for k, v in m_obj.input_schema.fields.items()}
                        sample_p = getattr(m_obj, "sample_payload", None)
                        disp_name = getattr(m_obj, "display_name", None)
                        m_type = getattr(m_obj, "type", None)
                        m_desc = getattr(m_obj, "description", None)

                        if disp_name is None:
                            disp_name = m_name
                            m_type = "crud"
                            m_desc = f"Thao tác dữ liệu trên bảng '{s_name}'."

                            if m_name == "find_all":
                                disp_name = f"Xem Danh Sách ({s_name})"
                                m_type = "crud"
                                m_desc = f"Lấy danh sách tất cả các dòng dữ liệu trong bảng '{s_name}' để hiển thị lên màn hình danh sách hoặc trang quản trị (hỗ trợ phân trang limit, offset)."
                                sample_p = sample_p or {"limit": 10, "offset": 0}
                            elif m_name == "find_by_id":
                                disp_name = "Xem Chi Tiết Theo ID"
                                m_type = "crud"
                                m_desc = f"Lấy toàn bộ thông tin chi tiết của 1 bản ghi trong bảng '{s_name}' khi người dùng bấm vào xem hồ sơ/chi tiết."
                                sample_p = sample_p or {"id": 1}
                            elif m_name == "insert":
                                disp_name = "Thêm Mới Bản Ghi"
                                m_type = "crud"
                                m_desc = f"Tạo và lưu 1 dòng dữ liệu mới vào bảng '{s_name}'."
                                sample_p = sample_p or {"name": "Bản ghi mới", "status": "DANG_HOAT_DONG"}
                            elif m_name == "update":
                                disp_name = "Cập Nhật / Sửa"
                                m_type = "crud"
                                m_desc = f"Chỉnh sửa các trường thông tin của bản ghi trong bảng '{s_name}' theo ID."
                                sample_p = sample_p or {"id": 1, "data": {"status": "DA_CAP_NHAT"}}
                            elif m_name == "delete":
                                disp_name = "Xóa Bản Ghi"
                                m_type = "crud"
                                m_desc = f"Xóa hẳn bản ghi khỏi bảng '{s_name}' theo ID."
                                sample_p = sample_p or {"id": 1}
                            elif m_name == "query":
                                disp_name = "Tìm Kiếm & Lọc"
                                m_type = "crud"
                                m_desc = f"Tìm kiếm và lọc các bản ghi trong bảng '{s_name}' theo điều kiện tùy chọn."
                                sample_p = sample_p or {"filters": {"status": "DANG_HOAT_DONG"}}
                            elif m_name == "book_ride":
                                disp_name = "Đặt Chuyến Đi Mới"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Đặt Xe: Khi hành khách bấm 'Đặt Chuyến' trên App, API tự động tính cước, tìm tài xế gần nhất và tạo chuyến đi."
                                sample_p = sample_p or {"passenger_id": 1, "pickup": "123 Lê Lợi, Q1", "destination": "Sân Bay Tân Sơn Nhất"}
                            elif m_name == "complete_trip":
                                disp_name = "Hoàn Thành Chuyến Đi"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Kết Thúc Cuốc Xe: Tài xế bấm 'Đã đến nơi' -> Cập nhật chuyến đi thành công và tiến hành thanh toán cước."
                                sample_p = sample_p or {"ride_id": 1}
                            elif m_name == "toggle_online":
                                disp_name = "Bật/Tắt Trạng Thái Đón Khách"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Tài Xế: Bật hoặc tắt trạng thái sẵn sàng nhận cuốc xe của tài xế trên App tài xế."
                                sample_p = sample_p or {"driver_id": 1, "is_online": True}
                            elif m_name == "place_order":
                                disp_name = "Đặt Hàng & Trừ Tiền Ví"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Mua Hàng: Kiểm tra tồn kho, kiểm tra số dư ví người mua, trừ tiền ví, trừ tồn kho và xuất đơn hàng."
                                sample_p = sample_p or {"user_id": 1, "product_id": 1, "quantity": 2}
                            elif m_name == "transfer_money":
                                disp_name = "Chuyển Tiền Liên Ví"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Chuyển Tiền: Kiểm tra số dư ví gửi, chuyển tiền sang ví nhận và ghi nhật ký giao dịch ngân hàng."
                                sample_p = sample_p or {"from_wallet_id": 1, "to_wallet_id": 2, "amount": 500000}
                            elif m_name == "like_post":
                                disp_name = "Thích Bài Viết (Thả Tim)"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Tương Tác: Tăng số lượt like của bài viết và bắn thông báo đẩy cho tác giả."
                                sample_p = sample_p or {"post_id": 1, "user_id": 1}
                            elif m_name == "book_appointment":
                                disp_name = "Đặt Lịch Khám Bác Sĩ"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Đặt Lịch: Bệnh nhân chọn bác sĩ và khung giờ khám bệnh trực tuyến."
                                sample_p = sample_p or {"patient_id": 1, "doctor_id": 1, "datetime": "2026-09-01 09:00"}
                            elif m_name == "book_room":
                                disp_name = "Đặt Phòng Khách Sạn"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Du Lịch: Khách đặt phòng và giữ chỗ khách sạn theo ngày nhận phòng."
                                sample_p = sample_p or {"customer_id": 1, "hotel_id": 1, "check_in": "2026-09-10"}
                            elif m_name == "enroll_course":
                                disp_name = "Đăng Ký Khóa Học"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Học Tập: Ghi danh học viên vào khóa học và khởi tạo tiến độ học 0%."
                                sample_p = sample_p or {"student_id": 1, "course_id": 1}
                            elif m_name == "toggle_power":
                                disp_name = "Bật/Tắt Nguồn Thiết Bị"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Nhà Thông Minh: Gửi lệnh BẬT/TẮT nguồn điện tới thiết bị IoT từ xa qua điện thoại."
                                sample_p = sample_p or {"device_id": 1, "power": True}
                            elif m_name == "play_stream":
                                disp_name = "Phát Luồng Trực Tuyến"
                                m_type = "workflow"
                                m_desc = "Nghiệp vụ Truyền Thông: Khởi tạo luồng phát video hoặc âm thanh trực tuyến."
                                sample_p = sample_p or {"media_id": 1, "user_id": 1}
                            else:
                                sample_p = sample_p or {"id": 1}

                        methods_list.append({
                            "name": m_name,
                            "display_name": disp_name,
                            "type": m_type,
                            "description": m_desc,
                            "schema": schema_fields,
                            "sample_payload": sample_p,
                        })
                    services_info[s_name] = {"methods": methods_list}

                self._send_encoded_response(200, {
                    "status": "SUCCESS",
                    "services": services_info,
                })
                return

            # 5. Thống kê sơ đồ luồng hệ thống: GET /api/bfa/flow-stats
            if clean_path == "/api/bfa/flow-stats":
                self._send_encoded_response(200, {
                    "status": "SUCCESS",
                    "active_blueprint": settings.blueprint,
                    "active_driver": settings.database_driver,
                    "services_count": len(runtime.services),
                    "services": list(runtime.services.keys()),
                    "status_mode": "ACTIVE" if len(runtime.services) > 0 else "IDLE",
                    "host": settings.server_config.get("host", "127.0.0.1"),
                    "port": settings.server_config.get("port", 8080),
                })
                return

            # 6. Tài liệu chuẩn OpenAPI 3.0: GET /api/bfa/openapi.json
            if clean_path in ("/api/bfa/openapi.json", "/openapi.json", "/api/openapi.json"):
                paths = {}
                for s_name, s_obj in runtime.services.items():
                    for m_name, m_obj in s_obj.methods.items():
                        ep = f"/api/{s_name}/{m_name}"
                        disp_name = getattr(m_obj, "display_name", f"{s_name}_{m_name}")
                        desc = getattr(m_obj, "description", f"Thao tác {m_name} trên bảng {s_name}")
                        sample_p = getattr(m_obj, "sample_payload", {}) or {}

                        paths[ep] = {
                            "post": {
                                "summary": disp_name,
                                "description": desc,
                                "tags": [s_name],
                                "requestBody": {
                                    "required": True,
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "type": "object",
                                                "example": sample_p
                                            }
                                        }
                                    }
                                },
                                "responses": {
                                    "200": {
                                        "description": "Thành công (SUCCESS)",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "type": "object",
                                                    "properties": {
                                                        "status": {"type": "string", "example": "SUCCESS"},
                                                        "data": {"type": "object"},
                                                        "message": {"type": "string"}
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "400": {
                                        "description": "Lỗi dữ liệu (ERROR)",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "type": "object",
                                                    "properties": {
                                                        "status": {"type": "string", "example": "ERROR"},
                                                        "error": {"type": "string"}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }

                self._send_encoded_response(200, {
                    "openapi": "3.0.0",
                    "info": {
                        "title": f"BFA API Contract - {settings.blueprint or 'Hệ Thống Tùy Chỉnh'}",
                        "version": "1.0.0",
                        "description": "Tài liệu kỹ thuật API chuẩn hóa từ Backend for All (BFA) dành cho lập trình viên Android (Kotlin/Retrofit/Flutter) & Frontend."
                    },
                    "servers": [
                        {"url": "http://10.0.2.2:8080", "description": "Android Emulator (Máy Ảo Android)"},
                        {"url": "http://127.0.0.1:8080", "description": "Localhost (Web / iOS Simulator)"}
                    ],
                    "paths": paths
                })
                return

            # 7. Hợp đồng API chi tiết cho Android & Retrofit: GET /api/bfa/android-contract
            if clean_path == "/api/bfa/android-contract":
                tables_meta = {}
                for s_name, s_obj in runtime.services.items():
                    methods_list = []
                    for m_name, m_obj in s_obj.methods.items():
                        methods_list.append({
                            "endpoint": f"/api/{s_name}/{m_name}",
                            "http_method": "POST",
                            "name": m_name,
                            "display_name": getattr(m_obj, "display_name", m_name),
                            "type": getattr(m_obj, "type", "crud"),
                            "description": getattr(m_obj, "description", ""),
                            "sample_payload": getattr(m_obj, "sample_payload", {}),
                            "retrofit_signature": f'@POST("api/{s_name}/{m_name}")\nsuspend fun {m_name}(@Body req: Map<String, Any>): Response<BfaResponse<Any>>'
                        })
                    tables_meta[s_name] = methods_list

                self._send_encoded_response(200, {
                    "status": "SUCCESS",
                    "active_blueprint": settings.blueprint,
                    "android_configuration": {
                        "emulator_base_url": "http://10.0.2.2:8080/",
                        "real_device_base_url": "http://<IP_LAN_MAY_TINH>:8080/",
                        "manifest_permissions": [
                            '<uses-permission android:name="android.permission.INTERNET" />',
                            '<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />'
                        ],
                        "manifest_application_attr": 'android:usesCleartextTraffic="true"'
                    },
                    "response_format": {
                        "status": "SUCCESS | ERROR",
                        "data": "Đối tượng dữ liệu (records, record, deleted_id)",
                        "error": "Mô tả lỗi chi tiết nếu có"
                    },
                    "tables": tables_meta
                })
                return

            # 8. Postman Collection Export: GET /api/bfa/postman.json
            if clean_path in ("/api/bfa/postman.json", "/postman.json"):
                pm_items = []
                for s_name, s_obj in runtime.services.items():
                    sub_items = []
                    for m_name, m_obj in s_obj.methods.items():
                        disp_name = getattr(m_obj, "display_name", f"{s_name}_{m_name}")
                        sample_p = getattr(m_obj, "sample_payload", {}) or {}
                        sub_items.append({
                            "name": disp_name,
                            "request": {
                                "method": "POST",
                                "header": [
                                    {"key": "Content-Type", "value": "application/json"}
                                ],
                                "body": {
                                    "mode": "raw",
                                    "raw": json.dumps(sample_p, indent=2, ensure_ascii=False)
                                },
                                "url": {
                                    "raw": f"{{{{base_url}}}}/api/{s_name}/{m_name}",
                                    "host": ["{{base_url}}"],
                                    "path": ["api", s_name, m_name]
                                }
                            }
                        })
                    pm_items.append({
                        "name": f"Bảng: {s_name}",
                        "item": sub_items
                    })

                self._send_encoded_response(200, {
                    "info": {
                        "name": f"BFA API Collection - {settings.blueprint or 'Custom'}",
                        "_postman_id": "bfa-collection-v1",
                        "description": "Tập hợp toàn bộ endpoint API đang chạy trên BFA Backend.",
                        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
                    },
                    "item": pm_items,
                    "variable": [
                        {"key": "base_url", "value": "http://10.0.2.2:8080", "type": "string"}
                    ]
                })
                return

            # 9. HỢP ĐỒNG NHẤT THỂ TOÀN CẦU (Universal Invocation Contract): GET /api/bfa/contract
            if clean_path in ("/api/bfa/contract", "/api/contract", "/contract"):
                self._send_encoded_response(200, {
                    "status": "SUCCESS",
                    "title": "BFA Universal Single Contract (Hợp Đồng Nhất Thể Duy Nhất)",
                    "description": "1 hợp đồng duy nhất dùng cho TẤT CẢ các ngôn ngữ (Android, Flutter, iOS, React, Python, Java, C#, PHP).",
                    "universal_endpoint": {
                        "url": "http://127.0.0.1:8080/api/bfa/call",
                        "emulator_url": "http://10.0.2.2:8080/api/bfa/call",
                        "method": "POST",
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    },
                    "request_schema": {
                        "service": "Tên bảng hoặc dịch vụ (Ví dụ: 'users', 'products', 'rides')",
                        "action": "Tên thao tác ('find_all', 'find_by_id', 'insert', 'update', 'delete', 'query', 'snapshot', 'batch', hoặc nghiệp vụ custom)",
                        "payload": "Đối tượng tham số truyền vào ({ limit, id, filters, data... })"
                    },
                    "response_schema": {
                        "status": "SUCCESS | ERROR",
                        "data": "Dữ liệu trả về (records, record, deleted_id, snapshot...)",
                        "message": "Thông điệp phản hồi",
                        "error": "Chi tiết lỗi nếu status == ERROR"
                    },
                    "active_services": list(runtime.services.keys()),
                    "active_blueprint": settings.blueprint,
                })
                return

            # 10. Kiểm tra sức khỏe: GET /health
            if clean_path == "/health":
                self._send_encoded_response(200, {
                    "status": "SUCCESS",
                    "platform": "Backend for All (BFA)",
                    "message": "Cổng Dịch Vụ Đang Hoạt Động Bình Thường",
                    "active_blueprint": settings.blueprint,
                    "registered_services": list(runtime.services.keys()),
                })
                return

            # 404
            self._send_encoded_response(404, {
                "status": "ERROR",
                "error": "BFA_DIEM_CUOI_KHONG_TON_TAI",
            })

        def do_POST(self):
            parsed = urlparse(self.path)
            clean_path = parsed.path.rstrip("/")

            content_length = int(self.headers.get("Content-Length", 0))
            raw_bytes = self.rfile.read(content_length) if content_length > 0 else b""

            try:
                payload = decoder.decode(raw_bytes)
            except ValueError as err:
                self._send_encoded_response(400, {"status": "ERROR", "error": f"BFA_DECODER_ERROR: {err}"})
                return

            # 1. Kích hoạt nhanh Bản thiết kế: POST /api/bfa/launch
            if clean_path == "/api/bfa/launch":
                bp_key = payload.get("blueprint_key", "b2c_store")
                try:
                    storage = get_storage_engine()
                    runtime.services.clear()
                    mount_blueprint_to_runtime(bp_key, storage, runtime)

                    full_cfg = settings.config.copy()
                    full_cfg["blueprint"] = bp_key
                    settings.save_config(full_cfg)

                    self._send_encoded_response(200, {
                        "status": "SUCCESS",
                        "message": f"Đã nạp kiến trúc '{bp_key}' thành công!",
                        "active_services": list(runtime.services.keys()),
                    })
                    return
                except Exception as e:
                    self._send_encoded_response(500, {"status": "ERROR", "error": str(e)})
                    return

            # 1a. Dừng / Tắt hệ thống đang chạy: POST /api/bfa/stop
            if clean_path == "/api/bfa/stop":
                runtime.services.clear()
                full_cfg = settings.config.copy()
                full_cfg["blueprint"] = "idle"
                settings.save_config(full_cfg)
                self._send_encoded_response(200, {
                    "status": "SUCCESS",
                    "message": "Đã dừng và giải phóng toàn bộ dịch vụ!",
                    "active_services": [],
                })
                return

            # 1b. Tạo & Khởi chạy Hệ Thống Kiến Trúc Tùy Chỉnh Không Giới Hạn: POST /api/bfa/custom-system
            if clean_path == "/api/bfa/custom-system":
                from bfa.catalog.registry import register_custom_blueprint
                try:
                    bp_record = register_custom_blueprint(payload)
                    storage = get_storage_engine()
                    runtime.services.clear()
                    mount_blueprint_to_runtime(bp_record["key"], storage, runtime)

                    full_cfg = settings.config.copy()
                    full_cfg["blueprint"] = bp_record["key"]
                    settings.save_config(full_cfg)

                    self._send_encoded_response(200, {
                        "status": "SUCCESS",
                        "message": f"Đã khởi tạo và kích hoạt hệ thống tùy chỉnh '{bp_record['name']}'!",
                        "blueprint": bp_record,
                        "active_services": list(runtime.services.keys()),
                    })
                    return
                except Exception as e:
                    self._send_encoded_response(500, {"status": "ERROR", "error": str(e)})
                    return

            # 1c. Kích hoạt chọn riêng lẻ từng bảng (Modular Table Cherry-Pick): POST /api/bfa/cherry-pick
            if clean_path == "/api/bfa/cherry-pick":
                tables = payload.get("tables", [])
                if not tables:
                    tables = ["users"]

                try:
                    storage = get_storage_engine()
                    runtime.services.clear()
                    services = generate_services_for_tables(tables, storage)
                    services_map = {}
                    for s in services:
                        services_map[s.name] = s
                        runtime.register_service(s)

                    from bfa.domain.presets import apply_domain_tuning
                    apply_domain_tuning("custom", services_map, storage)

                    full_cfg = settings.config.copy()
                    full_cfg["blueprint"] = "modular_cherry_pick"
                    full_cfg["tables"] = tables
                    settings.save_config(full_cfg)

                    self._send_encoded_response(200, {
                        "status": "SUCCESS",
                        "message": f"Đã kích hoạt thành công {len(tables)} bảng riêng lẻ: {', '.join(tables)}!",
                        "active_services": list(runtime.services.keys()),
                    })
                    return
                except Exception as e:
                    self._send_encoded_response(500, {"status": "ERROR", "error": str(e)})
                    return

            # 1d. Thêm API tùy chỉnh khi thấy thiếu: POST /api/bfa/add-custom-api
            if clean_path == "/api/bfa/add-custom-api":
                s_name = payload.get("service", "custom_service").strip()
                m_name = payload.get("method", "custom_method").strip()
                disp_name = payload.get("display_name") or m_name
                m_desc = payload.get("description") or f"API tùy chỉnh '{m_name}' của dịch vụ '{s_name}'."
                sample_p = payload.get("sample_payload") or {"message": "Dữ liệu mẫu"}
                action_type = payload.get("action_type", "custom")
                success_msg = payload.get("success_message") or f"Thực thi thành công API '{m_name}'!"

                try:
                    storage = get_storage_engine()
                    # Lấy hoặc tạo Service mới
                    if s_name not in runtime.services:
                        new_svc = Service(s_name)
                        runtime.register_service(new_svc)
                    
                    target_svc = runtime.services[s_name]

                    # Gắn handler động theo action_type
                    def custom_api_handler(req: Request) -> dict:
                        p = req.payload or {}
                        if action_type == "insert":
                            res = storage.insert(s_name, p)
                            return {"record": res, "message": success_msg}
                        elif action_type == "update":
                            rec_id = p.get("id") or p.get("user_id") or 1
                            res = storage.update(s_name, rec_id, p)
                            return {"updated": res, "message": success_msg}
                        elif action_type == "query":
                            res = storage.query(s_name, p.get("filters", {}))
                            return {"records": res, "total": len(res), "message": success_msg}
                        else:
                            return {
                                "executed_method": f"/api/{s_name}/{m_name}",
                                "received_payload": p,
                                "message": success_msg,
                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            }

                    new_method = Method(m_name, handler=custom_api_handler)
                    new_method.display_name = disp_name
                    new_method.type = "workflow"
                    new_method.description = m_desc
                    new_method.sample_payload = sample_p

                    target_svc.add_method(new_method)

                    self._send_encoded_response(200, {
                        "status": "SUCCESS",
                        "message": f"Đã thêm và mở cổng API: POST /api/{s_name}/{m_name} thành công!",
                        "endpoint": f"/api/{s_name}/{m_name}",
                        "service": s_name,
                        "method": m_name,
                    })
                    return
                except Exception as e:
                    self._send_encoded_response(500, {"status": "ERROR", "error": str(e)})
                    return

            # 1e. Xóa API riêng lẻ: POST /api/bfa/remove-api
            if clean_path == "/api/bfa/remove-api":
                s_name = payload.get("service", "").strip()
                m_name = payload.get("method", "").strip()
                if s_name in runtime.services and m_name in runtime.services[s_name].methods:
                    del runtime.services[s_name].methods[m_name]
                    self._send_encoded_response(200, {
                        "status": "SUCCESS",
                        "message": f"Đã xóa API '/api/{s_name}/{m_name}'!",
                    })
                else:
                    self._send_encoded_response(404, {"status": "ERROR", "error": f"API '/api/{s_name}/{m_name}' không tồn tại."})
                return

            # 1f. Gộp yêu cầu đa năng (Batch Query Aggregate): POST /api/bfa/batch
            if clean_path in ("/api/bfa/batch", "/api/batch", "/batch"):
                queries = payload.get("queries", {})
                results = {}
                for key, q_spec in queries.items():
                    s_name = q_spec.get("service")
                    m_name = q_spec.get("method", "find_all")
                    p_data = q_spec.get("payload", {})
                    req = Request(service_name=s_name, method_name=m_name, payload=p_data)
                    resp = runtime.handle_request(req)
                    results[key] = resp.data if resp.status == "SUCCESS" else {"error": resp.error}

                self._send_encoded_response(200, {
                    "status": "SUCCESS",
                    "data": results,
                    "count": len(results),
                })
                return

            # 1g. Gom dữ liệu nhanh toàn bộ hoặc nhiều bảng (One-Shot Snapshot): POST /api/bfa/snapshot
            if clean_path in ("/api/bfa/snapshot", "/api/snapshot", "/snapshot"):
                target_tables = payload.get("tables")
                limit = int(payload.get("limit", 10))
                if not target_tables:
                    target_tables = list(runtime.services.keys())
                elif isinstance(target_tables, str):
                    target_tables = [t.strip() for t in target_tables.split(",") if t.strip()]

                snapshot_data = {}
                for table in target_tables:
                    if table in runtime.services:
                        req = Request(service_name=table, method_name="find_all", payload={"limit": limit})
                        resp = runtime.handle_request(req)
                        if resp.status == "SUCCESS":
                            records = resp.data.get("records", []) if isinstance(resp.data, dict) else resp.data
                            snapshot_data[table] = records
                        else:
                            snapshot_data[table] = []

                self._send_encoded_response(200, {
                    "status": "SUCCESS",
                    "data": snapshot_data,
                    "tables_count": len(snapshot_data),
                })
                return

            # 1h. HỢP ĐỒNG NHẤT THỂ TOÀN CẦU (Universal Unified Execution Protocol): POST /api/bfa/call
            if clean_path in ("/api/bfa/call", "/api/call", "/api/v1", "/call"):
                service_name = payload.get("service") or payload.get("table") or ""
                action_name = payload.get("action") or payload.get("method") or "find_all"
                inner_payload = payload.get("payload")
                if inner_payload is None:
                    inner_payload = {k: v for k, v in payload.items() if k not in ("service", "table", "action", "method")}

                # 1. Nếu là yêu cầu gom toàn bộ dữ liệu (Snapshot)
                if action_name in ("snapshot", "all_tables") or service_name in ("snapshot", "bfa_snapshot"):
                    target_tables = inner_payload.get("tables")
                    limit = int(inner_payload.get("limit", 10))
                    if not target_tables:
                        target_tables = list(runtime.services.keys())
                    elif isinstance(target_tables, str):
                        target_tables = [t.strip() for t in target_tables.split(",") if t.strip()]

                    snap_res = {}
                    for tbl in target_tables:
                        if tbl in runtime.services:
                            r = runtime.handle_request(Request(service_name=tbl, method_name="find_all", payload={"limit": limit}))
                            snap_res[tbl] = r.data.get("records", []) if (r.status == "SUCCESS" and isinstance(r.data, dict)) else []
                    self._send_encoded_response(200, {
                        "status": "SUCCESS",
                        "data": snap_res,
                        "message": "Đã gom toàn bộ dữ liệu thành công",
                    })
                    return

                # 2. Nếu là yêu cầu gộp nhiều API khác nhau (Batch)
                if action_name in ("batch", "multi") or service_name in ("batch", "bfa_batch"):
                    queries = inner_payload.get("queries", {})
                    batch_res = {}
                    for q_key, q_val in queries.items():
                        s = q_val.get("service") or q_val.get("table")
                        m = q_val.get("action") or q_val.get("method", "find_all")
                        p = q_val.get("payload", {})
                        r = runtime.handle_request(Request(service_name=s, method_name=m, payload=p))
                        batch_res[q_key] = r.data if r.status == "SUCCESS" else {"error": r.error}
                    self._send_encoded_response(200, {
                        "status": "SUCCESS",
                        "data": batch_res,
                        "message": "Đã thực thi toàn bộ yêu cầu batch thành công",
                    })
                    return

                # 3. Yêu cầu bình thường cho 1 bảng / hàm bất kỳ
                if not service_name:
                    self._send_encoded_response(400, {
                        "status": "ERROR",
                        "error": "Thiếu tham số 'service' hoặc 'table' (Ví dụ: 'users', 'products', 'rides').",
                    })
                    return

                if service_name not in runtime.services:
                    self._send_encoded_response(404, {
                        "status": "ERROR",
                        "error": f"Bảng/Dịch vụ '{service_name}' không tồn tại hoặc chưa được kích hoạt.",
                    })
                    return

                req = Request(service_name=service_name, method_name=action_name, payload=inner_payload)
                resp = runtime.handle_request(req)
                if resp.status == "SUCCESS":
                    self._send_encoded_response(200, {
                        "status": "SUCCESS",
                        "data": resp.data,
                        "message": getattr(resp, "message", "Thực thi thành công"),
                    })
                else:
                    self._send_encoded_response(400, {
                        "status": "ERROR",
                        "error": resp.error or "Lỗi xử lý yêu cầu",
                    })
                return

            # 2. Kiểm tra kết nối CSDL: POST /api/bfa/db-test
            if clean_path == "/api/bfa/db-test":
                is_ok, msg = test_database_connection(payload)
                if is_ok:
                    self._send_encoded_response(200, {"status": "SUCCESS", "message": msg})
                else:
                    self._send_encoded_response(400, {"status": "ERROR", "error": msg})
                return

            # 3. Quét danh sách bảng tự động: POST /api/bfa/db-discover
            if clean_path == "/api/bfa/db-discover":
                discovered = discover_database_tables(payload)
                self._send_encoded_response(200, {"status": "SUCCESS", "tables": discovered})
                return

            # 4. Lưu CSDL & Tự động phát sinh API: POST /api/bfa/db-connect-and-mount
            if clean_path == "/api/bfa/db-connect-and-mount":
                db_cfg = payload.get("database", {})
                tables = payload.get("tables", [])
                if not tables:
                    tables = ["users", "products", "orders"]

                try:
                    full_cfg = settings.config.copy()
                    full_cfg["database"] = db_cfg
                    full_cfg["tables"] = tables
                    full_cfg["blueprint"] = "custom"
                    settings.save_config(full_cfg)

                    storage = get_storage_engine(db_cfg, force_reload=True)
                    runtime.services.clear()
                    services = generate_services_for_tables(tables, storage)
                    for s in services:
                        runtime.register_service(s)

                    self._send_encoded_response(200, {
                        "status": "SUCCESS",
                        "message": f"Đã kết nối {db_cfg.get('driver', 'sqlite').upper()} và sinh thành công API cho {len(tables)} bảng!",
                        "active_services": list(runtime.services.keys()),
                    })
                    return
                except Exception as e:
                    self._send_encoded_response(500, {"status": "ERROR", "error": str(e)})
                    return

            # 5. Gọi API nghiệp vụ chuẩn: POST /api/<service>/<method>
            path_segments = [seg for seg in clean_path.strip("/").split("/") if seg]
            if len(path_segments) >= 3 and path_segments[0] == "api":
                service_name = path_segments[1]
                method_name = path_segments[2]
            elif len(path_segments) == 2:
                service_name = path_segments[0]
                method_name = path_segments[1]
            else:
                self._send_encoded_response(400, {
                    "status": "ERROR",
                    "error": "BFA_DINH_DANG_URL_KHONG_HOP_LE: Cần gửi tới '/api/<service>/<method>'",
                })
                return

            bfa_request = Request(service_name=service_name, method_name=method_name, payload=payload)
            bfa_response = runtime.handle_request(bfa_request)
            self._send_encoded_response(200, bfa_response.to_dict())

        def _serve_web_studio(self):
            """Phục vụ mã HTML của BFA Studio."""
            if WEB_INDEX_PATH.exists():
                with open(WEB_INDEX_PATH, "r", encoding="utf-8") as f:
                    html_content = f.read().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html_content)))
                self.end_headers()
                self.wfile.write(html_content)
            else:
                self._send_encoded_response(404, {"status": "ERROR", "error": "Khong tim thay tep index.html cua Studio"})

        def _serve_web_tutorial(self):
            """Phục vụ trang HTML Hướng Dẫn & Tài Liệu BFA."""
            if WEB_TUTORIAL_PATH.exists():
                with open(WEB_TUTORIAL_PATH, "r", encoding="utf-8") as f:
                    html_content = f.read().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html_content)))
                self.end_headers()
                self.wfile.write(html_content)
            else:
                self._send_encoded_response(404, {"status": "ERROR", "error": "Khong tim thay tep tutorial.html"})

        def _send_encoded_response(self, status_code: int, data_dict: dict):
            response_bytes = encoder.encode(data_dict)
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            self.wfile.write(response_bytes)

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def log_message(self, format, *args):
            pass

    return BFAHTTPRequestHandler


class HTTPTransport(BaseTransport):
    def __init__(
        self,
        runtime: Runtime,
        host: str = "127.0.0.1",
        port: int = 8080,
        encoder: JSONEncoder | None = None,
        decoder: JSONDecoder | None = None,
    ):
        super().__init__(runtime, encoder=encoder, decoder=decoder)
        self.host = host
        self.port = port
        handler_class = create_bfa_http_handler(self.runtime, self.encoder, self.decoder)
        self.server = HTTPServer((self.host, self.port), handler_class)

    def serve_forever(self) -> None:
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()
