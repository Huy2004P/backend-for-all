# Tài Liệu Đa Ngôn Ngữ & Quốc Tế Hóa (i18n)

Backend for All (BFA) hướng tới mục tiêu giảm thiểu tối đa rào cản ngôn ngữ để lập trình viên trên toàn thế giới có thể hiểu, tiếp cận và đóng góp vào BFA bằng ngôn ngữ mẹ đẻ của mình.

---

## 1. Kiến Trúc Một Nguồn Chân Lý (Single Source of Truth)

Để tránh tình trạng phân mảnh và sai lệch đặc tả giữa các ngôn ngữ, BFA áp dụng mô hình **Single Source of Truth**:

```text
                  BFA Canonical Specification
                               │
                               ▼
               Canonical Documentation (English)
                               │
         ┌─────────────┬───────┴───────┬─────────────┐
         ▼             ▼               ▼             ▼
    Tiếng Việt      日本語           한국어          Español
     (vi)           (ja)            (ko)           (es)
```

1. **Tài liệu gốc (Canonical Docs - `docs/en/`)**: Là nguồn chân lý chính thức duy nhất. Mọi thay đổi đặc tả, cập nhật API và thay đổi kiến trúc đều xuất phát tại đây bằng tiếng Anh.
2. **Bản dịch đồng bộ (`docs/<lang_code>/`)**: Các bộ tài liệu đại diện cho đặc tả gốc được dịch sang ngôn ngữ địa phương.
3. **Phát hiện nội dung lỗi thời (Outdated Detection)**: Khi tài liệu gốc tiếng Anh thay đổi, bản dịch tương ứng sẽ được đánh dấu là *Needs Update* (Cần cập nhật) cho đến khi cộng đồng hoàn tất đồng bộ.

---

## 2. Nguyên Tắc Giữ Nguyên Thuật Ngữ Kỹ Thuật (Technical Identifiers)

> [!CRITICAL]
> **Tên định danh code, class, method, cú pháp API và mã lỗi máy đọc KHÔNG ĐƯỢC PHÉP dịch trong source code và API.**

Bản dịch chỉ địa phương hóa **lời giải thích, hướng dẫn, văn bản mô tả khái niệm**—tuyệt đối không dịch identifier trong code.

| Thành phần | Quy tắc | Ví dụ ĐÚNG | Ví dụ SAI |
| :--- | :--- | :--- | :--- |
| **Code Identifiers** | Giữ nguyên tiếng Anh | `class Service:`, `def handle_request():` | `class DịchVụ:`, `def xử_lý_yêu_cầu():` |
| **BFA Primitives** | Giải thích bằng tiếng Việt, giữ nguyên thuật ngữ | "BFA Service là một đơn vị logic độc lập..." | "BFA BộPhụcVụ là..." |
| **Mã lỗi máy đọc** | Giữ nguyên bất biến | `BFA_SERVICE_NOT_FOUND` | `BFA_KHONG_TIM_THAY_SERVICE` |
| **Thông báo lỗi cho người đọc** | Địa phương hóa tự nhiên | *EN*: "Service 'users' not found."<br>*VI*: "Không tìm thấy service 'users'." | Đổi cả error code lẫn message |

---

## 3. Tiêu Chuẩn Chất Lượng Bản Dịch

- **Độ chính xác kỹ thuật quan trọng hơn dịch sát nghĩa (literal translation)**: Ưu tiên sự mạch lạc, dễ hiểu và chuẩn xác trong ngữ cảnh kỹ thuật phần mềm.
- **Vai trò của AI / Dịch tự động**: Có thể dùng AI/công cụ dịch máy để tạo bản thảo ban đầu, nhưng **bắt buộc phải có kỹ sư bản ngữ review kỹ lưỡng** trước khi merge vào repository.
- **Thuật ngữ không có từ tương đương**: Nếu một thuật ngữ kỹ thuật phổ biến (ví dụ: *middleware*, *broker*, *payload*, *runtime*) không có từ dịch tiếng Việt tương đương chuẩn xác, hãy giữ nguyên từ tiếng Anh và giải thích ngữ cảnh xung quanh.

---

## 4. Cấu Trúc Thư Mục Documentation

```text
docs/
├── README.md               # Cổng thông tin docs & bảng trạng thái dịch thuật
├── languages.json          # Metadata registry các ngôn ngữ được hỗ trợ
├── en/                     # Tài liệu chuẩn (Canonical - Source of Truth)
│   ├── vision.md
│   ├── architecture.md
│   ├── protocol.md
│   ├── contributing.md
│   └── internationalization.md
│
├── vi/                     # Bản dịch Tiếng Việt
│   ├── vision.md
│   ├── architecture.md
│   ├── protocol.md
│   ├── contributing.md
│   └── internationalization.md
│
└── <lang>/                 # Các ngôn ngữ cộng đồng tiếp theo (ja, ko, zh, es, v.v.)
```

---

## 5. Quy Trình Đóng Góp Bản Dịch

1. **Kiểm tra trạng thái**: Xem file `docs/languages.json` và `docs/README.md` để nắm tiến độ của ngôn ngữ.
2. **Đối chiếu tài liệu gốc**: Đọc file tài liệu tương ứng trong thư mục `docs/en/`.
3. **Dịch nội dung**: Dịch phần diễn giải, bảo toàn nguyên vẹn các code block, link markdown và technical identifier.
4. **Tạo Pull Request**: Mở PR trên GitHub với mô tả rõ ràng phần nội dung đã cập nhật.
5. **Duy trì cập nhật**: Theo dõi các thay đổi mới trong `docs/en/` để kịp thời đồng bộ bản dịch.
