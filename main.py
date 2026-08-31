"""
Backend for All (BFA) — Nền Tảng 100 Bản Thiết Kế Kiến Trúc Backend & Bảng Điều Khiển Web Studio.

Khởi chạy Cổng Dịch Vụ API Backend trên cổng mạng 8080 và phục vụ giao diện BFA Studio.
"""

import sys
import threading
import time
import webbrowser

from bfa.catalog.loader import mount_blueprint_to_runtime
from bfa.config.settings import settings
from bfa.protocol.decoder import JSONDecoder
from bfa.protocol.encoder import JSONEncoder
from bfa.runtime.runtime import Runtime
from bfa.storage.factory import get_storage_engine
from bfa.transport.http import HTTPTransport


# ==============================================================================
# 1. KHỞI TẠO ỨNG DỤNG TỪ DANH MỤC 100 BẢN THIẾT KẾ
# ==============================================================================
def setup_application(storage=None, blueprint_key=None, table_names=None) -> Runtime:
    """
    Khởi tạo BFA Runtime bằng cách nạp một trong 100 Bản Thiết Kế từ Danh Mục
    hoặc tự động sinh API từ danh sách bảng tùy chọn.
    """
    if storage is None:
        storage = get_storage_engine()

    runtime = Runtime()

    if table_names is not None:
        from bfa.bridge.crud import generate_services_for_tables
        from bfa.domain.presets import apply_domain_tuning
        services = generate_services_for_tables(table_names, storage)
        services_map = {}
        for s in services:
            services_map[s.name] = s
            runtime.register_service(s)
        apply_domain_tuning("ecommerce", services_map, storage)
        return runtime

    if blueprint_key is None:
        blueprint_key = settings.blueprint

    if blueprint_key == "idle" or not blueprint_key:
        return runtime

    try:
        runtime, bp_info = mount_blueprint_to_runtime(blueprint_key, storage, runtime)
    except Exception as e:
        print(f"[THÔNG BÁO] Hệ thống đang ở trạng thái dừng hoặc chưa nạp: {e}")

    return runtime


# ==============================================================================
# 2. MÁY CHỦ HTTP & ĐIỂM VÀO BFA WEB STUDIO
# ==============================================================================
def start_http_server(runtime: Runtime, host: str = "127.0.0.1", port: int = 8080) -> HTTPTransport:
    encoder = JSONEncoder()
    decoder = JSONDecoder()
    transport = HTTPTransport(
        runtime=runtime,
        host=host,
        port=port,
        encoder=encoder,
        decoder=decoder,
    )
    server_thread = threading.Thread(target=transport.server.serve_forever, daemon=True)
    server_thread.start()
    return transport


def main() -> None:
    host = settings.server_config.get("host", "127.0.0.1")
    port = settings.server_config.get("port", 8080)
    url = f"http://{host}:{port}"

    runtime = setup_application()
    start_http_server(runtime, host=host, port=port)

    print("=" * 72)
    print(f"[BFA] Cổng Dịch Vụ Backend ĐANG CHẠY tại: {url}")
    print(f"[BẢNG ĐIỀU KHIỂN] Giao Diện BFA Web Studio: {url}")
    print(f"[TÀI LIỆU] Hướng Dẫn Chi Tiết: {url}/tutorial")
    print(f"[KIẾN TRÚC] Hệ Thống Đang Kích Hoạt: #{settings.blueprint} ({settings.domain.upper()})")
    print(f"[LƯU TRỮ] Động Cơ Dữ Liệu Đang Kết Nối: {get_storage_engine()}")
    print(f"[DỊCH VỤ] Danh Sách API Đang Mở: {list(runtime.services.keys())}")
    print("=" * 72)
    print("[HƯỚNG DẪN] Nhấn phím Ctrl+C trong Terminal để dừng máy chủ.")

    # Tự động mở giao diện Web Studio trên trình duyệt mặc định
    if "--no-browser" not in sys.argv:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[THÔNG BÁO] Máy chủ BFA đã dừng hoạt động. Tạm biệt!")


if __name__ == "__main__":
    main()