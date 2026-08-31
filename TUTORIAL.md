# 📖 HƯỚNG DẪN SỬ DỤNG TOÀN DIỆN BACKEND FOR ALL (BFA)

Chào mừng bạn đến với **Backend for All (BFA)** — Nền tảng Cổng API và 100 Bản Thiết Kế Kiến Trúc Backend tự động hóa hàng đầu!

---

## 📑 MỤC LỤC BÀI HỌC
1. [Bài 1: Tổng Quan & Triết Lý Hoạt Động Của BFA](#bài-1-tổng-quan--triết-lý-hoạt-động-của-bfa)
2. [Bài 2: Sử Dụng 100 Kiến Trúc Mẫu Chỉ Với 1 Click](#bài-2-sử-dụng-100-kiến-trúc-mẫu-chỉ-với-1-click)
3. [Bài 3: Kết Nối Cơ Sở Dữ Liệu Có Sẵn (PostgreSQL, MySQL, SQLite, MongoDB...)](#bài-3-kết-nối-cơ-sở-dữ-liệu-có-sẵn)
4. [Bài 4: Kiểm Thử API Trực Tiếp Trên BFA Studio](#bài-4-kiểm-thử-api-trực-tiếp-trên-bfa-studio)
5. [Bài 5: Tích Hợp Vào Frontend / Mobile App (React, Flutter, Python)](#bài-5-tích-hợp-vào-frontend--mobile-app)
6. [Bài 6: Hướng Dẫn Đóng Góp Kiến Trúc Mới Cho Cộng Đồng](#bài-6-hướng-dẫn-đóng-góp-kiến-trúc-mới-cho-cộng-đồng)

---

## BÀI 1: TỔNG QUAN & TRIẾT LÝ HOẠT ĐỘNG CỦA BFA

BFA hoạt động theo mô hình **Khối Xếp Hình LEGO Độc Lập**:

```text
[Ứng Dụng Client (React, Flutter, Python)]
                  │ (HTTP POST /api/<bảng>/<thao_tác>)
                  ▼
         [HTTP Transport :8080]
                  │ (Giải mã JSON Payload)
                  ▼
            [BFA Runtime]
                  │ (Định tuyến Service & Kiểm tra Schema)
                  ▼
     [Tự Động Sinh CRUD & Nghiệp Vụ]
                  │ (Giao tiếp qua BaseStorage)
                  ▼
[Cơ Sở Dữ Liệu Thật (PostgreSQL / MySQL / SQLite / MongoDB)]
```

- **Không ràng buộc Database**: BFA không ép bạn dùng Database riêng. Bạn có bất kỳ CSDL nào, BFA kết nối vào và tự sinh API cho bảng đó.
- **Không có dữ liệu giả (Zero Mock)**: Mọi thao tác thêm/sửa/xóa đều thực thi trực tiếp vào Database thật.

---

## BÀI 2: SỬ DỤNG 100 KIẾN TRÚC MẪU CHỈ VỚI 1 CLICK

BFA tích hợp sẵn **100 Bản Thiết Kế Kiến Trúc Hoàn Chỉnh** chia thành 10 Khối Ngành:
1. **Thương Mại Điện Tử** (Cửa hàng B2C, Sàn đa người bán, Đấu giá, Đơn hàng định kỳ...)
2. **Tài Chính & Ngân Hàng** (Ví điện tử, Sàn P2P, Sổ cái tài sản số, Cổng thanh toán...)
3. **Mạng Xã Hội** (Đăng bài ngắn, Diễn đàn, Ghép đôi hẹn hò, Kênh livestream...)
4. **Giáo Dục Trực Tuyến** (Khóa học trực tuyến, Gia sư 1-1, Thi trắc nghiệm, Chấm code...)
5. **Du Lịch & Khách Sạn** (Đặt phòng khách sạn, Vé máy bay, Homestay, Thuê xe tự lái...)
6. **Y Tế & Sức Khỏe** (Đặt lịch khám bệnh, Bệnh án điện tử, Tư vấn từ xa, Nhà thuốc...)
7. **Vận Tải & Kho Vận** (Gọi xe công nghệ, Giao hàng COD, Quản lý ô kệ kho, Bãi đỗ xe...)
8. **Phần Mềm Doanh Nghiệp** (Quản lý khách hàng CRM, Bảng công việc Kanban, Chấm công...)
9. **Giải Trí & Truyền Thông** (Xem phim trực tuyến, Nghe nhạc, Bán vé rạp chiếu phim...)
10. **Nhà Thông Minh & IoT** (Điều khiển đèn thông minh, Trạm khí tượng, Giám sát xe GPS...)

### 👉 Cách sử dụng:
1. Mở BFA Studio tại `http://127.0.0.1:8080`.
2. Ở tab **100 Kiến Trúc Mẫu**, nhập từ khóa tìm kiếm (Ví dụ: `gọi xe`, `tiền ảo`, `khách sạn`).
3. Bấm **Khởi Chạy Hệ Thống** $\rightarrow$ Hệ thống tự động tạo bảng và nạp sẵn dữ liệu mẫu thực tế!

---

## BÀI 3: KẾT NỐI CƠ SỞ DỮ LIỆU CÓ SẴN

Nếu bạn đã cài sẵn Database của riêng mình (PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, SQLite, DuckDB, MongoDB, Redis), hãy làm theo **Quy trình 3 Bước**:

1. **Bước 1: Chọn CSDL & Điền Thông Số**:
   - Chọn loại Database $\rightarrow$ Nhập Host, Port, Tên CSDL, Username, Mật khẩu.
   - Bấm **Kiểm Tra Kết Nối CSDL** (hệ thống báo thành công).
2. **Bước 2: Khai Báo Bảng Dữ Liệu**:
   - Bấm nút **Tự Động Quét Bảng Trong CSDL** hoặc nhập danh sách bảng (ví dụ: `users, products, orders`).
3. **Bước 3: Kích Hoạt**:
   - Bấm nút xanh: **Bước 3: Kích Hoạt Cơ Sở Dữ Liệu & Sinh Toàn Bộ API**.
   - BFA tự động phát sinh 6 API chuẩn (`find_all`, `find_by_id`, `insert`, `update`, `delete`, `query`) cho từng bảng!

---

## BÀI 4: KIỂM THỬ API TRỰC TIẾP TRÊN BFA STUDIO

Tại tab **Kiểm Thử API**:
- Cột bên trái hiển thị danh sách toàn bộ Bảng và Thao tác.
- Cột bên phải có sẵn khung soạn thảo JSON Payload.
- Bấm **Thực Thi Yêu Cầu API** $\rightarrow$ Xem kết quả JSON thật trả về cùng thời gian phản hồi (Độ trễ mili-giây).

---

## BÀI 5: TÍCH HỢP VÀO FRONTEND / MOBILE APP

Mọi ngôn ngữ đều gửi request `POST` tới:
`http://127.0.0.1:8080/api/<tên_bảng>/<thao_tác>`

### 1. JavaScript / TypeScript (React, Next.js, Vue, Node.js):
```javascript
const phanHoi = await fetch("http://127.0.0.1:8080/api/products/find_all", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ limit: 10 })
});
const ketQua = await phanHoi.json();
console.log(ketQua.data.records);
```

### 2. Flutter / Dart (Mobile iOS & Android):
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

final phanHoi = await http.post(
  Uri.parse('http://10.0.2.2:8080/api/products/find_all'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'limit': 10}),
);
final ketQua = jsonDecode(phanHoi.body);
```

### 3. Python:
```python
import requests
phan_hoi = requests.post("http://127.0.0.1:8080/api/products/find_all", json={"limit": 10})
print(phan_hoi.json())
```

---

## BÀI 6: HƯỚNG DẪN ĐÓNG GÓP KIẾN TRÚC MỚI CHO CỘNG ĐỒNG

Để đóng góp kiến trúc hệ thống thứ 101, 102 vào BFA:
1. Mở file [bfa/catalog/registry.py](file:///d:/backend-for-all/bfa/catalog/registry.py).
2. Thêm định nghĩa mới vào từ điển `BLUEPRINT_CATALOG`:
```python
"ten_he_thong_moi": {
    "id": 101,
    "category": "ecommerce",
    "name": "Tên Hệ Thống Mới",
    "icon": "shopping-bag",
    "description": "Mô tả nghiệp vụ của hệ thống...",
    "tables": ["bang_1", "bang_2", "bang_3"],
    "seed_data": {
        "bang_1": [{"id": 1, "name": "Dữ liệu mẫu"}],
    }
}
```
3. Tạo Pull Request lên GitHub để cộng đồng cùng sử dụng!
