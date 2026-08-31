"""
Domain Presets & Business Action Orchestrators for Backend for All (BFA).

Bổ sung các hàm nghiệp vụ thực tế (Domain Business RPC Workflows) bên cạnh
6 thao tác CRUD cơ bản cho cả 10 khối ngành kiến trúc.
"""

from bfa.core.method import Method
from bfa.core.request import Request
from bfa.core.schema import Schema
from bfa.core.service import Service
from bfa.storage.base import BaseStorage


# ==============================================================================
# 1. THƯƠNG MẠI ĐIỆN TỬ (E-COMMERCE)
# ==============================================================================
def apply_ecommerce_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    orders_service = services_map.get("orders")
    if orders_service:
        def place_order_handler(req: Request) -> dict:
            user_id = req.payload.get("user_id", 1)
            product_id = req.payload.get("product_id", 1)
            quantity = req.payload.get("quantity", 1)

            product = storage.get("products", product_id)
            if not product:
                raise ValueError(f"Sản phẩm #{product_id} không tồn tại.")
            unit_price = product.get("price", 0)
            total_amount = unit_price * quantity

            user = storage.get("users", user_id)
            if not user:
                raise ValueError(f"Người dùng #{user_id} không tồn tại.")

            if user.get("balance", 0) < total_amount:
                raise ValueError(f"Insufficient funds: Balance is {user.get('balance', 0):,}, total is {total_amount:,}.")
            if product.get("stock", 0) < quantity:
                raise ValueError(f"Out of stock: Only {product.get('stock', 0)} left, requested {quantity}.")

            # Trừ tiền ví & Trừ tồn kho
            storage.update("users", user_id, {"balance": user.get("balance", 0) - total_amount})
            storage.update("products", product_id, {"stock": product.get("stock", 0) - quantity})

            order_data = {
                "user_id": user_id,
                "product_id": product_id,
                "product_name": product.get("name", "Product"),
                "unit_price": unit_price,
                "quantity": quantity,
                "total_amount": total_amount,
                "status": "COMPLETED",
            }
            created_order = storage.insert("orders", order_data)
            return {"order": created_order, "message": f"Đặt hàng thành công đơn #{created_order.get('id', 1)}!"}

        orders_service.add_method(Method("place_order", handler=place_order_handler, input_schema=Schema({"user_id": int, "product_id": int, "quantity": int})))

    users_service = services_map.get("users")
    if users_service:
        def deposit_handler(req: Request) -> dict:
            user_id = req.payload.get("user_id", 1)
            amount = req.payload.get("amount", 100000)
            user = storage.get("users", user_id)
            if not user:
                raise ValueError(f"User #{user_id} not found.")
            new_balance = user.get("balance", 0) + amount
            updated = storage.update("users", user_id, {"balance": new_balance})
            return {"user_id": user_id, "new_balance": updated["balance"], "message": f"Nạp thành công {amount:,} VND vào tài khoản #{user_id}!"}

        users_service.add_method(Method("deposit", handler=deposit_handler, input_schema=Schema({"user_id": int, "amount": int})))


# ==============================================================================
# 2. TÀI CHÍNH & VÍ ĐIỆN TỬ (FINTECH)
# ==============================================================================
def apply_fintech_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    wallets_service = services_map.get("wallets") or services_map.get("accounts")
    if wallets_service:
        def transfer_handler(req: Request) -> dict:
            from_wallet = req.payload.get("from_wallet_id", 1)
            to_wallet = req.payload.get("to_wallet_id", 2)
            amount = req.payload.get("amount", 500000)
            note = req.payload.get("note", "Chuyen tien nhanh")

            tx = storage.insert("transactions", {
                "from_wallet_id": from_wallet,
                "to_wallet_id": to_wallet,
                "amount": amount,
                "note": note,
                "status": "THANH_CONG",
            })
            return {"transaction": tx, "message": f"Đã chuyển thành công {amount:,} VND từ ví #{from_wallet} sang ví #{to_wallet}!"}

        wallets_service.add_method(Method("transfer_money", handler=transfer_handler, input_schema=Schema({"from_wallet_id": int, "to_wallet_id": int, "amount": int})))


# ==============================================================================
# 3. MẠNG XÃ HỘI & CỘNG ĐỒNG (SOCIAL)
# ==============================================================================
def apply_social_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    posts_service = services_map.get("posts")
    if posts_service:
        def like_post_handler(req: Request) -> dict:
            post_id = req.payload.get("post_id", 1)
            user_id = req.payload.get("user_id", 1)
            post = storage.get("posts", post_id) or {"id": post_id, "likes_count": 0}
            new_likes = post.get("likes_count", 0) + 1
            storage.update("posts", post_id, {"likes_count": new_likes})
            return {"post_id": post_id, "likes_count": new_likes, "message": f"Người dùng #{user_id} đã thích bài viết #{post_id}!"}

        posts_service.add_method(Method("like_post", handler=like_post_handler, input_schema=Schema({"post_id": int, "user_id": int})))

    users_service = services_map.get("users")
    if users_service:
        def follow_handler(req: Request) -> dict:
            user_id = req.payload.get("user_id", 1)
            target_id = req.payload.get("target_id", 2)
            return {"user_id": user_id, "target_id": target_id, "message": f"Người dùng #{user_id} đã theo dõi #{target_id}!"}

        users_service.add_method(Method("follow", handler=follow_handler, input_schema=Schema({"user_id": int, "target_id": int})))


# ==============================================================================
# 4. VẬN TẢI & GỌI XE (LOGISTICS / RIDE HAILING)
# ==============================================================================
def apply_logistics_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    rides_service = services_map.get("rides") or services_map.get("shipments")
    if rides_service:
        def book_ride_handler(req: Request) -> dict:
            passenger_id = req.payload.get("passenger_id", 1)
            pickup = req.payload.get("pickup", "123 Le Loi, Q1")
            destination = req.payload.get("destination", "Tan Son Nhat Airport")
            fare = req.payload.get("fare", 120000)

            ride = storage.insert("rides", {
                "passenger_id": passenger_id,
                "driver_id": 1,
                "pickup_location": pickup,
                "dropoff_location": destination,
                "fare": fare,
                "status": "DA_NHAN_CHUYEN",
            })
            return {"ride": ride, "message": f"Đặt chuyến thành công! Tài xế #1 đang đến điểm đón."}

        def complete_trip_handler(req: Request) -> dict:
            ride_id = req.payload.get("ride_id", 1)
            updated = storage.update("rides", ride_id, {"status": "HOAN_THANH"})
            return {"ride": updated, "message": f"Chuyến đi #{ride_id} đã hoàn tất và thanh toán thành công!"}

        rides_service.add_method(Method("book_ride", handler=book_ride_handler, input_schema=Schema({"passenger_id": int, "pickup": str, "destination": str})))
        rides_service.add_method(Method("complete_trip", handler=complete_trip_handler, input_schema=Schema({"ride_id": int})))

    drivers_service = services_map.get("drivers")
    if drivers_service:
        def toggle_online_handler(req: Request) -> dict:
            driver_id = req.payload.get("driver_id", 1)
            is_online = req.payload.get("is_online", True)
            status_text = "SẴN SÀNG ĐÓN KHÁCH" if is_online else "NGOẠI TUYẾN"
            storage.update("drivers", driver_id, {"is_active": is_online})
            return {"driver_id": driver_id, "status": status_text, "message": f"Tài xế #{driver_id} đã chuyển trạng thái sang '{status_text}'."}

        drivers_service.add_method(Method("toggle_online", handler=toggle_online_handler, input_schema=Schema({"driver_id": int, "is_online": bool})))


# ==============================================================================
# 5. Y TẾ & BÁC SĨ (HEALTHCARE)
# ==============================================================================
def apply_healthcare_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    appointments_service = services_map.get("appointments")
    if appointments_service:
        def book_appointment_handler(req: Request) -> dict:
            patient_id = req.payload.get("patient_id", 1)
            doctor_id = req.payload.get("doctor_id", 1)
            date_time = req.payload.get("datetime", "2026-09-01 09:00")
            record = storage.insert("appointments", {
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "datetime": date_time,
                "status": "DA_XAC_NHAN",
            })
            return {"appointment": record, "message": f"Đã đặt lịch hẹn khám với Bác sĩ #{doctor_id} lúc {date_time}!"}

        appointments_service.add_method(Method("book_appointment", handler=book_appointment_handler, input_schema=Schema({"patient_id": int, "doctor_id": int})))


# ==============================================================================
# 6. GIÁO DỤC TRỰC TUYẾN (EDTECH)
# ==============================================================================
def apply_edtech_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    courses_service = services_map.get("courses")
    if courses_service:
        def enroll_handler(req: Request) -> dict:
            student_id = req.payload.get("student_id", 1)
            course_id = req.payload.get("course_id", 1)
            enrollment = storage.insert("enrollments", {
                "student_id": student_id,
                "course_id": course_id,
                "progress": 0,
                "status": "DANG_HOC",
            })
            return {"enrollment": enrollment, "message": f"Học viên #{student_id} đã đăng ký thành công khóa học #{course_id}!"}

        courses_service.add_method(Method("enroll_course", handler=enroll_handler, input_schema=Schema({"student_id": int, "course_id": int})))


# ==============================================================================
# 7. DU LỊCH & KHÁCH SẠN (TRAVEL)
# ==============================================================================
def apply_travel_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    bookings_service = services_map.get("bookings")
    if bookings_service:
        def book_room_handler(req: Request) -> dict:
            customer_id = req.payload.get("customer_id", 1)
            hotel_id = req.payload.get("hotel_id", 1)
            check_in = req.payload.get("check_in", "2026-09-10")
            booking = storage.insert("bookings", {
                "customer_id": customer_id,
                "hotel_id": hotel_id,
                "check_in": check_in,
                "status": "DA_GIU_CHO",
            })
            return {"booking": booking, "message": f"Đặt phòng khách sạn #{hotel_id} thành công cho ngày {check_in}!"}

        bookings_service.add_method(Method("book_room", handler=book_room_handler, input_schema=Schema({"customer_id": int, "hotel_id": int})))


# ==============================================================================
# 8. PHẦN MỀM DOANH NGHIỆP (SAAS)
# ==============================================================================
def apply_saas_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    tenants_service = services_map.get("tenants") or services_map.get("organizations")
    if tenants_service:
        def invite_member_handler(req: Request) -> dict:
            tenant_id = req.payload.get("tenant_id", 1)
            email = req.payload.get("email", "nhanvien@congty.vn")
            role = req.payload.get("role", "Thành Viên")
            membership = storage.insert("memberships", {"tenant_id": tenant_id, "email": email, "role": role})
            return {"membership": membership, "message": f"Đã gửi lời mời tham gia tổ chức #{tenant_id} cho email '{email}'!"}

        tenants_service.add_method(Method("invite_member", handler=invite_member_handler, input_schema=Schema({"tenant_id": int, "email": str})))


# ==============================================================================
# 9. GIẢI TRÍ & TRUYỀN THÔNG (GAMING / MEDIA)
# ==============================================================================
def apply_gaming_media_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    media_service = services_map.get("videos") or services_map.get("tracks") or services_map.get("movies")
    if media_service:
        def play_media_handler(req: Request) -> dict:
            media_id = req.payload.get("media_id", 1)
            user_id = req.payload.get("user_id", 1)
            return {"media_id": media_id, "user_id": user_id, "stream_url": "https://stream.bfa.local/live/1080p.m3u8", "message": f"Bắt đầu phát luồng trực tiếp cho người dùng #{user_id}."}

        media_service.add_method(Method("play_stream", handler=play_media_handler, input_schema=Schema({"media_id": int, "user_id": int})))


# ==============================================================================
# 10. NHÀ THÔNG MINH & IOT (IOT / SMART CITY)
# ==============================================================================
def apply_iot_tuning(services_map: dict[str, Service], storage: BaseStorage, config: dict) -> None:
    devices_service = services_map.get("devices")
    if devices_service:
        def toggle_power_handler(req: Request) -> dict:
            device_id = req.payload.get("device_id", 1)
            power = req.payload.get("power", True)
            state_text = "BẬT (ON)" if power else "TẮT (OFF)"
            storage.update("devices", device_id, {"power_state": power})
            return {"device_id": device_id, "power": power, "message": f"Đã gửi lệnh {state_text} tới thiết bị IoT #{device_id}!"}

        devices_service.add_method(Method("toggle_power", handler=toggle_power_handler, input_schema=Schema({"device_id": int, "power": bool})))


# ==============================================================================
# BẢNG ÁNH XẠ 10 KHỐI NGÀNH
# ==============================================================================
DOMAIN_PRESETS = {
    "ecommerce": {"applier": apply_ecommerce_tuning},
    "fintech": {"applier": apply_fintech_tuning},
    "social": {"applier": apply_social_tuning},
    "logistics": {"applier": apply_logistics_tuning},
    "healthcare": {"applier": apply_healthcare_tuning},
    "edtech": {"applier": apply_edtech_tuning},
    "travel": {"applier": apply_travel_tuning},
    "saas": {"applier": apply_saas_tuning},
    "gaming_media": {"applier": apply_gaming_media_tuning},
    "iot_smart": {"applier": apply_iot_tuning},
    "custom": {"applier": lambda s, db, cfg: None},
}


def apply_domain_tuning(domain_key: str, services_map: dict[str, Service], storage: BaseStorage, config: dict | None = None) -> None:
    """Áp dụng bộ tinh chỉnh nghiệp vụ của Domain vào danh sách Service."""
    preset = DOMAIN_PRESETS.get(domain_key.lower(), DOMAIN_PRESETS["custom"])
    applier_func = preset["applier"]
    applier_func(services_map, storage, config or {})
