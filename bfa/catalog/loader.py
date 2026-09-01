"""
Dynamic Blueprint Loader & Engine for Backend for All.

Takes any of the 100 System Blueprints, automatically provisions tables,
seeds sample demo data into the active storage, and mounts live CRUD & RPC APIs.
"""

from bfa.bridge.crud import generate_services_for_tables
from bfa.catalog.registry import get_blueprint
from bfa.catalog.schema_synthesizer import auto_seed_relational_database
from bfa.domain.presets import apply_domain_tuning
from bfa.runtime.runtime import Runtime
from bfa.storage.base import BaseStorage


def mount_blueprint_to_runtime(
    blueprint_key_or_id: str | int,
    storage: BaseStorage,
    runtime: Runtime | None = None,
) -> tuple[Runtime, dict]:
    """
    Kích hoạt một Blueprint bất kỳ trong số 100 Blueprint:
    1. Lấy thông tin Blueprint từ Registry.
    2. Nạp dữ liệu mẫu ban đầu từ Blueprint.
    3. Tự động phân tích và sinh dữ liệu liên kết quan hệ (Auto-Seed) cho các bảng còn trống.
    4. Tự động sinh CRUD APIs cho tất cả các bảng.
    5. Áp dụng tinh chỉnh nghiệp vụ Domain tương ứng.
    6. Đăng ký tất cả Service vào Runtime.
    """
    bp = get_blueprint(blueprint_key_or_id)
    if not bp:
        raise ValueError(f"Blueprint '{blueprint_key_or_id}' không tồn tại trong danh mục 100 Blueprint.")

    if runtime is None:
        runtime = Runtime()

    tables = bp["tables"]

    # 1. Nạp seed data nếu có trong blueprint
    seed_data = bp.get("seed_data", {})
    for table_name, sample_rows in seed_data.items():
        existing_records = storage.find_all(table_name)
        if not existing_records:
            for row in sample_rows:
                storage.insert(table_name, row)

    # 2. Tự động phân tích và nạp dữ liệu liên kết chuẩn cho các bảng con còn trống
    auto_seed_relational_database(tables, storage)

    # 3. Sinh CRUD APIs cho tất cả các bảng trong Blueprint
    services = generate_services_for_tables(tables, storage)
    services_map = {}
    for service in services:
        services_map[service.name] = service
        runtime.register_service(service)

    # 3. Áp dụng Domain Tuning theo Category
    category = bp["category"]
    apply_domain_tuning(category, services_map, storage)

    return runtime, bp


def load_blueprint_by_key(blueprint_key: str, storage: BaseStorage) -> tuple[Runtime, dict]:
    """Helper nạp nhanh blueprint theo key."""
    return mount_blueprint_to_runtime(blueprint_key, storage)
