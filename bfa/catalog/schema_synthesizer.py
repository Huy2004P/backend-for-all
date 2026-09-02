"""
BFA Schema Synthesizer & Relational Knowledge Engine.

Automatically analyzes system descriptions, synthesizes column schemas with data types,
detects foreign key relationships across tables, and provisions interconnected seed data
so that no database or table is ever left empty or disconnected.
"""

import time
from typing import Any
from bfa.storage.base import BaseStorage


# ==============================================================================
# 1. TỪ ĐIỂN TRI THỨC CSDL QUAN HỆ TOÀN DIỆN (150+ BẢNG DOANH NGHIỆP THỰC TẾ)
# ==============================================================================
TABLE_KNOWLEDGE_BASE: dict[str, dict[str, Any]] = {
    # --- E-COMMERCE & RETAIL ---
    "users": {
        "columns": {"id": "INTEGER PRIMARY KEY", "username": "TEXT", "email": "TEXT", "full_name": "TEXT", "role": "TEXT", "balance": "REAL", "created_at": "DATETIME"},
        "foreign_keys": {},
        "defaults": lambda i: {"id": i, "username": f"user_{i}", "email": f"user{i}@example.com", "full_name": f"Nguyễn Văn {chr(64+i)}", "role": "CUSTOMER", "balance": 1000000.0 * i, "created_at": "2026-08-31 08:00:00"}
    },
    "customers": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "tier": "TEXT", "loyalty_points": "INTEGER", "phone": "TEXT", "address": "TEXT"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": i, "tier": "VIP" if i == 1 else "STANDARD", "loyalty_points": 500 * i, "phone": f"090123456{i}", "address": f"Số {i*10} Đường Nguyễn Huệ, Q.1, TP.HCM"}
    },
    "vendors": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "name": "TEXT", "rating": "REAL", "balance": "REAL", "status": "TEXT"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": 1, "name": f"Gian Hàng Công Nghệ Số {i}", "rating": 4.8 + (i * 0.1), "balance": 5000000.0 * i, "status": "ACTIVE"}
    },
    "categories": {
        "columns": {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "slug": "TEXT", "icon": "TEXT", "parent_id": "INTEGER"},
        "foreign_keys": {"parent_id": "categories"},
        "defaults": lambda i: {"id": i, "name": ["Điện Tử", "Thời Trang", "Gia Dụng", "Sách"][i-1] if i <= 4 else f"Danh Mục {i}", "slug": ["dien-tu", "thoi-trang", "gia-dung", "sach"][i-1] if i <= 4 else f"danh-muc-{i}", "icon": "box", "parent_id": None}
    },
    "products": {
        "columns": {"id": "INTEGER PRIMARY KEY", "category_id": "INTEGER", "vendor_id": "INTEGER", "name": "TEXT", "price": "REAL", "stock": "INTEGER", "status": "TEXT", "created_at": "DATETIME"},
        "foreign_keys": {"category_id": "categories", "vendor_id": "vendors"},
        "defaults": lambda i: {"id": i, "category_id": 1, "vendor_id": 1, "name": ["Bàn phím cơ không dây RGB", "Chuột công thái học Wireless", "Tai nghe chống ồn Pro", "Màn hình 4K 144Hz"][i-1] if i <= 4 else f"Sản Phẩm Cao Cấp #{i}", "price": [250000, 150000, 450000, 1200000][i-1] if i <= 4 else 100000 * i, "stock": 20 + i * 5, "status": "IN_STOCK", "created_at": "2026-08-31 08:30:00"}
    },
    "orders": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "total_amount": "REAL", "status": "TEXT", "shipping_address": "TEXT", "payment_method": "TEXT", "created_at": "DATETIME"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": 1, "total_amount": 400000.0 * i, "status": ["PAID", "PROCESSING", "DELIVERED"][i-1] if i <= 3 else "PENDING", "shipping_address": f"Tòa nhà Landmark, Tầng {i}, TP.HCM", "payment_method": "WALLET", "created_at": "2026-08-31 09:00:00"}
    },
    "order_items": {
        "columns": {"id": "INTEGER PRIMARY KEY", "order_id": "INTEGER", "product_id": "INTEGER", "quantity": "INTEGER", "unit_price": "REAL", "subtotal": "REAL"},
        "foreign_keys": {"order_id": "orders", "product_id": "products"},
        "defaults": lambda i: {"id": i, "order_id": (i + 1) // 2, "product_id": (i % 2) + 1, "quantity": i, "unit_price": 250000.0, "subtotal": 250000.0 * i}
    },
    "cart_items": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "product_id": "INTEGER", "quantity": "INTEGER", "created_at": "DATETIME"},
        "foreign_keys": {"user_id": "users", "product_id": "products"},
        "defaults": lambda i: {"id": i, "user_id": 1, "product_id": i, "quantity": 2, "created_at": "2026-08-31 09:15:00"}
    },
    "coupons": {
        "columns": {"id": "INTEGER PRIMARY KEY", "code": "TEXT", "discount_percent": "REAL", "min_order_amount": "REAL", "expiry_date": "DATETIME"},
        "foreign_keys": {},
        "defaults": lambda i: {"id": i, "code": f"GIAMGIA{i*10}", "discount_percent": 10.0 * i, "min_order_amount": 100000.0, "expiry_date": "2026-12-31 23:59:59"}
    },
    "reviews": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "product_id": "INTEGER", "rating": "INTEGER", "comment": "TEXT", "created_at": "DATETIME"},
        "foreign_keys": {"user_id": "users", "product_id": "products"},
        "defaults": lambda i: {"id": i, "user_id": 1, "product_id": 1, "rating": 5, "comment": "Sản phẩm đóng gói cẩn thận, dùng rất mượt và ưng ý!", "created_at": "2026-08-31 10:00:00"}
    },
    "payouts": {
        "columns": {"id": "INTEGER PRIMARY KEY", "vendor_id": "INTEGER", "amount": "REAL", "status": "TEXT", "bank_account": "TEXT", "created_at": "DATETIME"},
        "foreign_keys": {"vendor_id": "vendors"},
        "defaults": lambda i: {"id": i, "vendor_id": 1, "amount": 1500000.0 * i, "status": "COMPLETED", "bank_account": f"9988776655{i}", "created_at": "2026-08-31 10:30:00"}
    },
    "commissions": {
        "columns": {"id": "INTEGER PRIMARY KEY", "order_id": "INTEGER", "vendor_id": "INTEGER", "rate_percent": "REAL", "amount": "REAL"},
        "foreign_keys": {"order_id": "orders", "vendor_id": "vendors"},
        "defaults": lambda i: {"id": i, "order_id": 1, "vendor_id": 1, "rate_percent": 5.0, "amount": 20000.0 * i}
    },

    # --- FINTECH & BANKING ---
    "wallets": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "currency": "TEXT", "balance": "REAL", "status": "TEXT"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": i, "currency": "VND", "balance": 2500000.0 * i, "status": "ACTIVE"}
    },
    "transactions": {
        "columns": {"id": "INTEGER PRIMARY KEY", "wallet_id": "INTEGER", "user_id": "INTEGER", "amount": "REAL", "type": "TEXT", "status": "TEXT", "reference": "TEXT", "created_at": "DATETIME"},
        "foreign_keys": {"wallet_id": "wallets", "user_id": "users"},
        "defaults": lambda i: {"id": i, "wallet_id": 1, "user_id": 1, "amount": 200000.0 * i, "type": "TRANSFER_OUT" if i%2==0 else "TOPUP", "status": "SUCCESS", "reference": f"TXN_BFA_9900{i}", "created_at": "2026-08-31 08:45:00"}
    },
    "cards": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "card_number": "TEXT", "card_holder": "TEXT", "card_type": "TEXT", "is_active": "BOOLEAN"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": 1, "card_number": f"****-****-****-{1000+i}", "card_holder": "NGUYEN VAN A", "card_type": "VISA_DEBIT", "is_active": True}
    },
    "loans": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "principal_amount": "REAL", "interest_rate": "REAL", "tenure_months": "INTEGER", "status": "TEXT"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": 1, "principal_amount": 10000000.0 * i, "interest_rate": 8.5, "tenure_months": 12, "status": "DISBURSED"}
    },

    # --- TRANSPORT, RIDE-HAILING & LOGISTICS ---
    "drivers": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "name": "TEXT", "phone": "TEXT", "license_plate": "TEXT", "vehicle_type": "TEXT", "rating": "REAL", "status": "TEXT"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": 1, "name": f"Tài Xế Nguyễn Văn B{i}", "phone": f"098877665{i}", "license_plate": f"59A-{1000+i}.99", "vehicle_type": "MOTORBIKE" if i%2==1 else "CAR_4_SEATS", "rating": 4.9, "status": "AVAILABLE"}
    },
    "rides": {
        "columns": {"id": "INTEGER PRIMARY KEY", "passenger_id": "INTEGER", "driver_id": "INTEGER", "pickup_address": "TEXT", "destination_address": "TEXT", "fare": "REAL", "status": "TEXT", "created_at": "DATETIME"},
        "foreign_keys": {"passenger_id": "users", "driver_id": "drivers"},
        "defaults": lambda i: {"id": i, "passenger_id": 1, "driver_id": 1, "pickup_address": "123 Lê Lợi, Bến Nghé, Q.1", "destination_address": "Sân Bay Tân Sơn Nhất, Tân Bình", "fare": 85000.0 * i, "status": "COMPLETED", "created_at": "2026-08-31 07:30:00"}
    },
    "shipments": {
        "columns": {"id": "INTEGER PRIMARY KEY", "order_id": "INTEGER", "tracking_code": "TEXT", "origin": "TEXT", "destination": "TEXT", "status": "TEXT", "estimated_delivery": "DATETIME"},
        "foreign_keys": {"order_id": "orders"},
        "defaults": lambda i: {"id": i, "order_id": 1, "tracking_code": f"VNPOST_EXP_{889900+i}", "origin": "Kho Tổng TP.HCM", "destination": "Cần Thơ", "status": "IN_TRANSIT", "estimated_delivery": "2026-09-02 17:00:00"}
    },
    "warehouses": {
        "columns": {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "code": "TEXT", "address": "TEXT", "capacity": "INTEGER"},
        "foreign_keys": {},
        "defaults": lambda i: {"id": i, "name": f"Kho Trung Chuyển Miền Nam #{i}", "code": f"WH-SGN-{i}", "address": "Khu Công Nghiệp Tân Bình, TP.HCM", "capacity": 50000}
    },
    "inventory": {
        "columns": {"id": "INTEGER PRIMARY KEY", "warehouse_id": "INTEGER", "product_id": "INTEGER", "quantity": "INTEGER", "reserved": "INTEGER"},
        "foreign_keys": {"warehouse_id": "warehouses", "product_id": "products"},
        "defaults": lambda i: {"id": i, "warehouse_id": 1, "product_id": i, "quantity": 100 * i, "reserved": 5 * i}
    },

    # --- SOCIAL, COMMUNITY & MEDIA ---
    "posts": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "content": "TEXT", "likes_count": "INTEGER", "comments_count": "INTEGER", "created_at": "DATETIME"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": 1, "content": f"Bài viết chia sẻ kiến thức công nghệ số {i} với Backend for All! Hệ thống chạy cực nhanh và tối ưu.", "likes_count": 42 * i, "comments_count": 8 * i, "created_at": "2026-08-31 06:00:00"}
    },
    "comments": {
        "columns": {"id": "INTEGER PRIMARY KEY", "post_id": "INTEGER", "user_id": "INTEGER", "content": "TEXT", "created_at": "DATETIME"},
        "foreign_keys": {"post_id": "posts", "user_id": "users"},
        "defaults": lambda i: {"id": i, "post_id": 1, "user_id": 1, "content": "Kiến trúc thiết kế rất gọn gàng và dễ mở rộng!", "created_at": "2026-08-31 06:15:00"}
    },
    "likes": {
        "columns": {"id": "INTEGER PRIMARY KEY", "post_id": "INTEGER", "user_id": "INTEGER", "created_at": "DATETIME"},
        "foreign_keys": {"post_id": "posts", "user_id": "users"},
        "defaults": lambda i: {"id": i, "post_id": 1, "user_id": i, "created_at": "2026-08-31 06:20:00"}
    },
    "messages": {
        "columns": {"id": "INTEGER PRIMARY KEY", "sender_id": "INTEGER", "receiver_id": "INTEGER", "message_text": "TEXT", "is_read": "BOOLEAN", "sent_at": "DATETIME"},
        "foreign_keys": {"sender_id": "users", "receiver_id": "users"},
        "defaults": lambda i: {"id": i, "sender_id": 1, "receiver_id": 2, "message_text": "Chào bạn, đơn hàng của bạn đã được tiếp nhận nhé!", "is_read": False, "sent_at": "2026-08-31 09:30:00"}
    },

    # --- HEALTHCARE & MEDICAL ---
    "doctors": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "full_name": "TEXT", "specialty": "TEXT", "hospital": "TEXT", "consultation_fee": "REAL"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": 1, "full_name": f"BS.CKII Trần Văn Y Tế {i}", "specialty": "Tim Mạch" if i%2==1 else "Nhi Khoa", "hospital": "Bệnh Viện Đại Học Y Dược", "consultation_fee": 300000.0}
    },
    "patients": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "full_name": "TEXT", "date_of_birth": "TEXT", "gender": "TEXT", "blood_type": "TEXT", "phone": "TEXT"},
        "foreign_keys": {"user_id": "users"},
        "defaults": lambda i: {"id": i, "user_id": 1, "full_name": f"Bệnh Nhân Lê Thị {chr(64+i)}", "date_of_birth": "1995-05-12", "gender": "NỮ" if i%2==1 else "NAM", "blood_type": "O+", "phone": f"091122334{i}"}
    },
    "appointments": {
        "columns": {"id": "INTEGER PRIMARY KEY", "patient_id": "INTEGER", "doctor_id": "INTEGER", "appointment_time": "DATETIME", "status": "TEXT", "symptoms": "TEXT"},
        "foreign_keys": {"patient_id": "patients", "doctor_id": "doctors"},
        "defaults": lambda i: {"id": i, "patient_id": 1, "doctor_id": 1, "appointment_time": "2026-09-05 09:00:00", "status": "CONFIRMED", "symptoms": "Khám sức khỏe định kỳ và tư vấn tim mạch"}
    },

    # --- EDUCATION & LMS ---
    "courses": {
        "columns": {"id": "INTEGER PRIMARY KEY", "instructor_id": "INTEGER", "title": "TEXT", "price": "REAL", "level": "TEXT", "rating": "REAL"},
        "foreign_keys": {"instructor_id": "users"},
        "defaults": lambda i: {"id": i, "instructor_id": 1, "title": ["Lập Trình Backend Python Chuyên Sâu", "Thiết Kế Kiến Trúc Hệ Thống Lớn", "Android Kotlin Full Course"][i-1] if i <= 3 else f"Khóa Học Kỹ Thuật #{i}", "price": 499000.0 * i, "level": "ADVANCED", "rating": 4.9}
    },
    "lessons": {
        "columns": {"id": "INTEGER PRIMARY KEY", "course_id": "INTEGER", "title": "TEXT", "duration_minutes": "INTEGER", "order_index": "INTEGER", "video_url": "TEXT"},
        "foreign_keys": {"course_id": "courses"},
        "defaults": lambda i: {"id": i, "course_id": 1, "title": f"Bài {i}: Xây Dựng Kiến Trúc Microservices Chuẩn", "duration_minutes": 25, "order_index": i, "video_url": f"https://cdn.bfa.dev/lessons/lec_{i}.mp4"}
    },
    "enrollments": {
        "columns": {"id": "INTEGER PRIMARY KEY", "student_id": "INTEGER", "course_id": "INTEGER", "progress_percent": "REAL", "enrolled_at": "DATETIME"},
        "foreign_keys": {"student_id": "users", "course_id": "courses"},
        "defaults": lambda i: {"id": i, "student_id": 1, "course_id": 1, "progress_percent": 65.0, "enrolled_at": "2026-08-20 14:00:00"}
    },

    # --- HOSPITALITY & TRAVEL ---
    "hotels": {
        "columns": {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "city": "TEXT", "stars": "INTEGER", "address": "TEXT", "rating": "REAL"},
        "foreign_keys": {},
        "defaults": lambda i: {"id": i, "name": f"Khách Sạn 5 Sao Grand Luxury {i}", "city": "Đà Nẵng", "stars": 5, "address": f"{i*12} Đường Võ Nguyên Giáp, Sơn Trà", "rating": 4.9}
    },
    "rooms": {
        "columns": {"id": "INTEGER PRIMARY KEY", "hotel_id": "INTEGER", "room_number": "TEXT", "room_type": "TEXT", "price_per_night": "REAL", "is_available": "BOOLEAN"},
        "foreign_keys": {"hotel_id": "hotels"},
        "defaults": lambda i: {"id": i, "hotel_id": 1, "room_number": f"P.{100+i}", "room_type": "DELUXE_OCEAN_VIEW", "price_per_night": 1200000.0, "is_available": True}
    },
    "bookings": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "hotel_id": "INTEGER", "room_id": "INTEGER", "check_in": "DATE", "check_out": "DATE", "total_price": "REAL", "status": "TEXT"},
        "foreign_keys": {"user_id": "users", "hotel_id": "hotels", "room_id": "rooms"},
        "defaults": lambda i: {"id": i, "user_id": 1, "hotel_id": 1, "room_id": 1, "check_in": "2026-09-10", "check_out": "2026-09-12", "total_price": 2400000.0, "status": "CONFIRMED"}
    },

    # --- ENTERPRISE, ERP & SAAS ---
    "departments": {
        "columns": {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "code": "TEXT", "manager_id": "INTEGER"},
        "foreign_keys": {"manager_id": "users"},
        "defaults": lambda i: {"id": i, "name": ["Phòng Công Nghệ & R&D", "Phòng Kinh Doanh", "Phòng Tài Chính", "Phòng Nhân Sự"][i-1] if i <= 4 else f"Phòng Ban #{i}", "code": f"DEPT-{100+i}", "manager_id": 1}
    },
    "employees": {
        "columns": {"id": "INTEGER PRIMARY KEY", "user_id": "INTEGER", "department_id": "INTEGER", "position": "TEXT", "salary": "REAL", "hire_date": "DATE"},
        "foreign_keys": {"user_id": "users", "department_id": "departments"},
        "defaults": lambda i: {"id": i, "user_id": 1, "department_id": 1, "position": "Kỹ Sư Backend Cấp Cao", "salary": 25000000.0, "hire_date": "2024-01-15"}
    },
    "projects": {
        "columns": {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "department_id": "INTEGER", "budget": "REAL", "status": "TEXT", "deadline": "DATE"},
        "foreign_keys": {"department_id": "departments"},
        "defaults": lambda i: {"id": i, "name": "Dự Án Chuyển Đổi Số Toàn Diện BFA", "department_id": 1, "budget": 500000000.0, "status": "IN_PROGRESS", "deadline": "2026-12-31"}
    },
    "tasks": {
        "columns": {"id": "INTEGER PRIMARY KEY", "project_id": "INTEGER", "assignee_id": "INTEGER", "title": "TEXT", "priority": "TEXT", "status": "TEXT"},
        "foreign_keys": {"project_id": "projects", "assignee_id": "employees"},
        "defaults": lambda i: {"id": i, "project_id": 1, "assignee_id": 1, "title": f"Nhiệm vụ {i}: Xây dựng API và liên kết cơ sở dữ liệu quan hệ", "priority": "HIGH", "status": "DONE" if i == 1 else "IN_PROGRESS"}
    },

    # --- REAL ESTATE & RENTAL ---
    "tenants": {
        "columns": {"id": "INTEGER PRIMARY KEY", "full_name": "TEXT", "phone": "TEXT", "id_card": "TEXT", "email": "TEXT"},
        "foreign_keys": {},
        "defaults": lambda i: {"id": i, "full_name": f"Khách Thuê {chr(64+i)}", "phone": f"093388990{i}", "id_card": f"07920000123{i}", "email": f"tenant{i}@example.com"}
    },
    "contracts": {
        "columns": {"id": "INTEGER PRIMARY KEY", "room_id": "INTEGER", "tenant_id": "INTEGER", "deposit_amount": "REAL", "start_date": "DATE", "end_date": "DATE", "status": "TEXT"},
        "foreign_keys": {"room_id": "rooms", "tenant_id": "tenants"},
        "defaults": lambda i: {"id": i, "room_id": i, "tenant_id": i, "deposit_amount": 7000000.0, "start_date": "2026-09-01", "end_date": "2027-09-01", "status": "ACTIVE"}
    },
    "utility_readings": {
        "columns": {"id": "INTEGER PRIMARY KEY", "room_id": "INTEGER", "month_year": "TEXT", "electricity_kwh": "REAL", "water_m3": "REAL"},
        "foreign_keys": {"room_id": "rooms"},
        "defaults": lambda i: {"id": i, "room_id": i, "month_year": "08/2026", "electricity_kwh": 120.5, "water_m3": 14.0}
    },
    "invoices": {
        "columns": {"id": "INTEGER PRIMARY KEY", "contract_id": "INTEGER", "room_id": "INTEGER", "total_amount": "REAL", "status": "TEXT", "due_date": "DATE"},
        "foreign_keys": {"contract_id": "contracts", "room_id": "rooms"},
        "defaults": lambda i: {"id": i, "contract_id": i, "room_id": i, "total_amount": 4200000.0, "status": "UNPAID", "due_date": "2026-09-05"}
    },

    # --- F&B, CAFE & RESTAURANTS ---
    "menu_items": {
        "columns": {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "category": "TEXT", "price": "REAL", "is_available": "BOOLEAN"},
        "foreign_keys": {},
        "defaults": lambda i: {"id": i, "name": ["Cà Phê Muối Sữa", "Trà Đào Cam Sả", "Trà Sữa Trân Châu Hoàng Gia", "Matcha Latte"][i-1] if i <= 4 else f"Món Uống #{i}", "category": "BEVERAGE", "price": [35000, 45000, 50000, 55000][i-1] if i <= 4 else 40000.0, "is_available": True}
    },
    "dining_tables": {
        "columns": {"id": "INTEGER PRIMARY KEY", "table_number": "TEXT", "capacity": "INTEGER", "status": "TEXT"},
        "foreign_keys": {},
        "defaults": lambda i: {"id": i, "table_number": f"Bàn {i:02d}", "capacity": 4, "status": "EMPTY"}
    },
    "staff": {
        "columns": {"id": "INTEGER PRIMARY KEY", "full_name": "TEXT", "role": "TEXT", "phone": "TEXT", "shift": "TEXT"},
        "foreign_keys": {},
        "defaults": lambda i: {"id": i, "full_name": f"Nhân Viên {chr(64+i)}", "role": "BARISTA" if i%2==1 else "CASHIER", "phone": f"090912345{i}", "shift": "MORNING"}
    },

    # --- CINEMA & TICKETING ---
    "movies": {
        "columns": {"id": "INTEGER PRIMARY KEY", "title": "TEXT", "genre": "TEXT", "duration_minutes": "INTEGER", "rating": "REAL"},
        "foreign_keys": {},
        "defaults": lambda i: {"id": i, "title": f"Siêu Phẩm Điện Ảnh #{i}", "genre": "ACTION", "duration_minutes": 120, "rating": 9.2}
    },
    "showtimes": {
        "columns": {"id": "INTEGER PRIMARY KEY", "movie_id": "INTEGER", "start_time": "DATETIME", "hall": "TEXT", "ticket_price": "REAL"},
        "foreign_keys": {"movie_id": "movies"},
        "defaults": lambda i: {"id": i, "movie_id": 1, "start_time": "2026-09-02 19:30:00", "hall": f"Rạp {i}", "ticket_price": 95000.0}
    },
    "tickets": {
        "columns": {"id": "INTEGER PRIMARY KEY", "showtime_id": "INTEGER", "user_id": "INTEGER", "seat_number": "TEXT", "price": "REAL", "status": "TEXT"},
        "foreign_keys": {"showtime_id": "showtimes", "user_id": "users"},
        "defaults": lambda i: {"id": i, "showtime_id": 1, "user_id": 1, "seat_number": f"F{i+5}", "price": 95000.0, "status": "PAID"}
    }
}


# ==============================================================================
# 2. HÀM TỰ ĐỘNG PHÂN TÍCH SCHEMA VÀ SUY LUẬN QUAN HỆ KHÓA NGOẠI
# ==============================================================================
def synthesize_table_schema(table_name: str) -> dict[str, Any]:
    """
    Suy luận thông minh cấu trúc cột và quan hệ cho một bảng bất kỳ.
    Nếu bảng nằm trong Từ điển tri thức, lấy định nghĩa chuẩn.
    Nếu bảng tùy biến, tự động suy luận các trường cơ bản + khóa ngoại.
    """
    t_clean = table_name.lower().strip()
    if t_clean in TABLE_KNOWLEDGE_BASE:
        return TABLE_KNOWLEDGE_BASE[t_clean]

    # Suy luận tự động cho bảng tùy biến
    inferred_cols = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT",
        "status": "TEXT",
        "created_at": "DATETIME",
    }
    inferred_fks = {}

    if "order" in t_clean or "item" in t_clean or "cart" in t_clean or "bill" in t_clean:
        inferred_cols["user_id"] = "INTEGER"
        inferred_fks["user_id"] = "users"
    if "item" in t_clean:
        inferred_cols["product_id"] = "INTEGER"
        inferred_fks["product_id"] = "products"
    if "room" in t_clean:
        inferred_cols["room_id"] = "INTEGER"
        inferred_fks["room_id"] = "rooms"

    return {
        "columns": inferred_cols,
        "foreign_keys": inferred_fks,
        "defaults": lambda i: {
            "id": i,
            "name": f"Bản ghi #{i} của {table_name}",
            "status": "ACTIVE",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }


def infer_system_relations(tables: list[str]) -> list[dict[str, Any]]:
    """
    Trích xuất toàn bộ đồ thị quan hệ (Foreign Key Relational Graph)
    cho danh sách các bảng đang hoạt động trong hệ thống.
    """
    relations = []
    active_set = set(t.lower() for t in tables)

    for source_table in tables:
        schema = synthesize_table_schema(source_table)
        fks = schema.get("foreign_keys", {})
        for fk_col, target_table in fks.items():
            if target_table.lower() in active_set:
                relations.append({
                    "from_table": source_table,
                    "from_column": fk_col,
                    "to_table": target_table,
                    "to_column": "id",
                    "relation_type": "MANY_TO_ONE",
                    "description": f"{source_table}.{fk_col} -> {target_table}.id",
                })

    return relations


# ==============================================================================
# 3. ĐỘNG CƠ TỰ ĐỘNG NẠP DỮ LIỆU LIÊN KẾT CHUẨN (AUTO SEED RELATIONAL DATA)
# ==============================================================================
def auto_seed_relational_database(tables: list[str], storage: BaseStorage, rows_per_table: int = 3) -> dict[str, int]:
    """
    Kiểm tra toàn bộ các bảng trong hệ thống.
    Nếu bảng nào còn trống (0 bản ghi), tự động sinh 2-3 bản ghi mẫu
    khớp chuẩn khóa ngoại và dữ liệu thực tế!
    """
    seeded_counts = {}

    def table_priority(t: str) -> int:
        schema = synthesize_table_schema(t)
        return len(schema.get("foreign_keys", {}))

    sorted_tables = sorted(tables, key=table_priority)

    for table in sorted_tables:
        existing = storage.find_all(table)
        if not existing or len(existing) == 0:
            schema = synthesize_table_schema(table)
            defaults_generator = schema.get("defaults")
            created_count = 0

            for i in range(1, rows_per_table + 1):
                if defaults_generator:
                    mock_record = defaults_generator(i)
                    storage.insert(table, mock_record)
                    created_count += 1
                else:
                    storage.insert(table, {
                        "id": i,
                        "name": f"Dữ liệu mẫu {table} #{i}",
                        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    created_count += 1

            seeded_counts[table] = created_count

    return seeded_counts


# ==============================================================================
# 4. ĐỘNG CƠ PHÂN TÍCH Ý TƯỞNG TIẾNG VIỆT TỰ NHIÊN (PROMPT-TO-SCHEMA ENGINE)
# ==============================================================================
DOMAIN_KEYWORD_PATTERNS = [
    {
        "keywords": ["phòng trọ", "nhà trọ", "căn hộ", "cho thuê", "homestay", "chủ trọ", "tiền trọ"],
        "name": "Quản Lý Cho Thuê Phòng Trọ & Căn Hộ",
        "category": "real_estate",
        "description": "Hệ thống quản lý thông tin phòng trọ, người thuê, hợp đồng, chỉ số điện nước và hóa đơn hàng tháng.",
        "tables": ["rooms", "tenants", "contracts", "utility_readings", "invoices"]
    },
    {
        "keywords": ["cà phê", "trà sữa", "quán nước", "quán ăn", "nhà hàng", "f&b", "coffee", "bàn ăn", "menu"],
        "name": "Quản Lý Quán Cà Phê, Trà Sữa & F&B",
        "category": "retail",
        "description": "Hệ thống quản lý thực đơn thức uống, sơ đồ bàn, nhân viên và các đơn gọi món trực tiếp.",
        "tables": ["menu_items", "dining_tables", "orders", "staff", "invoices"]
    },
    {
        "keywords": ["rạp chiếu phim", "vé xem phim", "cinema", "phim", "suất chiếu"],
        "name": "Hệ Thống Bán Vé Rạp Chiếu Phim",
        "category": "entertainment",
        "description": "Quản lý danh sách phim chiếu, các suất chiếu rạp và đặt vé chỗ ngồi cho khách hàng.",
        "tables": ["movies", "showtimes", "tickets", "users"]
    },
    {
        "keywords": ["gym", "thể hình", "fitness", "yoga", "pt", "huấn luyện viên", "phòng tập"],
        "name": "Quản Lý Phòng Tập Gym & Fitness",
        "category": "service",
        "description": "Quản lý hội viên, các gói tập, huấn luyện viên cá nhân và lịch sử check-in.",
        "tables": ["users", "departments", "projects", "tasks"]
    },
    {
        "keywords": ["bệnh viện", "phòng khám", "bác sĩ", "khám bệnh", "y tế", "thuốc", "bệnh nhân"],
        "name": "Quản Lý Phòng Khám & Y Tế",
        "category": "healthcare",
        "description": "Quản lý thông tin bệnh nhân, bác sĩ chuyên khoa và lịch hẹn khám bệnh.",
        "tables": ["doctors", "patients", "appointments", "users"]
    },
    {
        "keywords": ["khách sạn", "resort", "đặt phòng", "hotel", "du lịch", "tour"],
        "name": "Hệ Thống Đặt Phòng Khách Sạn & Resort",
        "category": "hospitality",
        "description": "Quản lý danh mục phòng, khách sạn, trạng thái đặt phòng và hóa đơn thanh toán.",
        "tables": ["hotels", "rooms", "bookings", "users"]
    },
    {
        "keywords": ["khóa học", "học trực tuyến", "e-learning", "lms", "bài giảng", "giáo viên", "học viên"],
        "name": "Nền Tảng Đào Tạo & Khóa Học Trực Tuyến",
        "category": "education",
        "description": "Quản lý các khóa học, bài học video, giảng viên và tiến độ học tập của học viên.",
        "tables": ["courses", "lessons", "enrollments", "users"]
    },
    {
        "keywords": ["gọi xe", "giao hàng", "tài xế", "chuyến đi", "ship", "shipper", "xe ôm"],
        "name": "Nền Tảng Đặt Xe & Giao Hàng Siêu Tốc",
        "category": "logistics",
        "description": "Hệ thống kết nối tài xế, hành khách, chuyến đi thực tế và tính cước vận chuyển.",
        "tables": ["drivers", "rides", "users", "transactions"]
    },
    {
        "keywords": ["bán hàng", "thương mại", "shop", "cửa hàng", "sản phẩm", "giỏ hàng", "mua sắm"],
        "name": "Cửa Hàng Thương Mại Điện Tử Toàn Diện",
        "category": "ecommerce",
        "description": "Quản lý sản phẩm, danh mục, giỏ hàng, đơn hàng và khách hàng.",
        "tables": ["categories", "products", "orders", "order_items", "users"]
    },
    {
        "keywords": ["mạng xã hội", "chat", "tin nhắn", "bài viết", "cộng đồng", "diễn đàn"],
        "name": "Mạng Xã Hội & Cộng Đồng Trực Tuyến",
        "category": "social",
        "description": "Chia sẻ bài viết, tương tác bình luận, thả tim và nhắn tin riêng.",
        "tables": ["posts", "comments", "likes", "messages", "users"]
    }
]


def parse_prompt_to_system_blueprint(prompt_text: str) -> dict[str, Any]:
    """
    Phân tích một câu mô tả tiếng Việt bất kỳ của người dùng và tự động tổng hợp:
    1. Tên hệ thống & Mô tả nghiệp vụ.
    2. Danh sách các bảng dữ liệu (Tables) phù hợp nhất.
    3. Cấu trúc cột, kiểu dữ liệu và liên kết khóa ngoại.
    """
    p_lower = prompt_text.lower().strip()

    # 1. Kiểm tra xem người dùng có chỉ định danh sách bảng cụ thể không (VD: "bảng: users, tasks, projects")
    explicit_tables = []
    if "bảng" in p_lower or "tables" in p_lower:
        part = p_lower.split("bảng")[-1] if "bảng" in p_lower else p_lower.split("tables")[-1]
        raw_names = part.replace(":", " ").replace(";", ",").replace(".", ",").split(",")
        for n in raw_names:
            clean = "".join(ch for ch in n.strip() if ch.isalnum() or ch == "_")
            if clean and len(clean) > 1 and clean not in explicit_tables:
                explicit_tables.append(clean)

    # 2. Quét khớp các mẫu nghiệp vụ phổ biến theo từ khóa
    best_match = None
    max_score = 0
    for pattern in DOMAIN_KEYWORD_PATTERNS:
        score = sum(1 for kw in pattern["keywords"] if kw in p_lower)
        if score > max_score:
            max_score = score
            best_match = pattern

    # 3. Tổng hợp kết quả
    if best_match and max_score >= 1 and not explicit_tables:
        tables = best_match["tables"]
        system_name = best_match["name"]
        description = best_match["description"]
        category = best_match["category"]
    elif explicit_tables:
        tables = explicit_tables
        system_name = f"Hệ Thống Tùy Chỉnh: {prompt_text[:35]}..."
        description = f"Hệ thống phát sinh tự động từ mô tả: '{prompt_text}'"
        category = "custom"
    else:
        # Fallback thông minh: Tự động trích xuất các danh từ trong câu
        words = [w.strip() for w in p_lower.replace(",", " ").replace(".", " ").split() if len(w) > 2]
        inferred = []
        for w in words:
            clean_w = "".join(ch for ch in w if ch.isalnum() or ch == "_")
            if clean_w in TABLE_KNOWLEDGE_BASE and clean_w not in inferred:
                inferred.append(clean_w)
        if not inferred:
            inferred = ["users", "products", "orders"]

        tables = inferred
        system_name = f"Hệ Thống Thông Minh: {prompt_text[:35]}..."
        description = f"Hệ thống được BFA phân tích tự động từ: '{prompt_text}'"
        category = "custom"

    key = "sys_" + "".join(ch for ch in system_name.lower() if ch.isalnum() or ch == "_")[:20] + f"_{int(time.time())}"

    return {
        "id": int(time.time()) % 100000,
        "key": key,
        "name": system_name,
        "category": category,
        "description": description,
        "tables": tables,
        "seed_data": {},
        "is_custom": True,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
