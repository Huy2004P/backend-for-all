# BFA Protocol — Mục Tiêu Giao Thức & Các Khái Niệm

> **Trạng thái**: *Bản phác thảo khái niệm / Working Specification*  
> *Lưu ý: Tài liệu này mô tả các mục tiêu thiết kế và khái niệm dự kiến. Đặc tả giao thức đang được thảo luận và chưa cố định chính thức.*

---

## 1. Mục Tiêu

BFA Protocol là đặc tả truyền thông (wire & messaging protocol) cho phép các backend service đa ngôn ngữ giao tiếp tin cậy, hiệu quả trên **mọi ngôn ngữ lập trình** và phục vụ **mọi loại hệ thống backend**.

Các mục tiêu trọng tâm:
- **Độc lập ngôn ngữ (Language Agnostic)**: Dễ dàng triển khai trên Python, Go, Rust, Java, TypeScript, C++, C#, Kotlin, v.v.
- **Độc lập hệ thống (System Agnostic)**: Đáp ứng tốt RPC giao dịch (E-Commerce, SaaS), streaming tần số cao (IoT, Game), sự kiện pub/sub bất đồng bộ (Social, Enterprise), và xử lý luồng dữ liệu (AI).
- **Độc lập tầng mạng (Transport Agnostic)**: Hoạt động trơn tru qua HTTP/1.1, HTTP/2, gRPC, WebSocket, Unix Domain Sockets, hoặc Message Brokers.
- **Hiệu năng cao & Độ trễ thấp**: Thiết kế vỏ bọc thông điệp (envelope) tối ưu cho cả mã hóa nhị phân lẫn định dạng văn bản (JSON).
- **Ngữ nghĩa phong phú**: Hỗ trợ gọi hàm đồng bộ (unary RPC), streaming hai chiều, sự kiện pub/sub và lan truyền metadata ngữ cảnh.

---

## 2. Các Khái Niệm Giao Thức Cốt Lõi

### Service
Ranh giới logic và đơn vị triển khai chứa các method RPC và event handler liên quan.

### Function / Method
Thủ tục RPC được cung cấp bởi service, có hợp đồng kiểu dữ liệu đầu vào/đầu ra rõ ràng và ngữ nghĩa thực thi (unary, streaming).

### Request & Response Envelopes
Vỏ bọc gói tin wire chuẩn mang:
- `id`: Mã định danh thông điệp duy nhất (UUID / Snowflake).
- `service`: Tên service đích.
- `method`: Tên phương thức / endpoint đích.
- `payload`: Dữ liệu có cấu trúc tuân thủ schema của method.
- `metadata`: Header key-value chứa thông tin trace, thời hạn deadline, tenant ID, và routing.

### Universal Schema
Đặc tả schema độc lập với ngôn ngữ để kiểm tra tính hợp lệ của dữ liệu, định kiểu trường và hỗ trợ tương thích ngược.

### Event
Thông điệp một chiều, phát ra bất đồng bộ để thông báo sự kiện nghiệp vụ mà không yêu cầu phản hồi trực tiếp.

### Error Taxonomy (Phân loại lỗi chuẩn hóa)
Quy chuẩn mã lỗi thống nhất để exception trong ngôn ngữ này (ví dụ: Python `ValueError`, Go `error`, Java `Exception`) được ánh xạ chính xác sang các mã lỗi chuẩn (ví dụ: `INVALID_ARGUMENT`, `NOT_FOUND`, `UNAUTHENTICATED`, `INTERNAL`, `UNAVAILABLE`) cho các service gọi hiểu được.

> [!IMPORTANT]
> **Mã lỗi máy đọc (machine-readable error code) phải giữ nguyên vẹn và độc lập với ngôn ngữ tự nhiên** (ví dụ: `BFA_SERVICE_NOT_FOUND`). Thông báo giải thích lỗi cho con người đọc có thể dịch sang ngôn ngữ địa phương, nhưng mã lỗi máy đọc là bất biến.

### Metadata & Context
Header lan truyền xuyên suốt các cuộc gọi giữa các service, mang trace ID, span ID, deadline và tenant context.

### Authentication & Authorization
Khung ngữ cảnh bảo mật mang thông tin định danh, quyền hạn và token qua ranh giới các service theo định dạng chuẩn.

---

## 3. Lộ Trình Phát Triển Giao Thức

Định dạng framing ở mức byte, danh sách serialization (JSON, Protobuf, MessagePack) và tài liệu RFC chính thức sẽ được định nghĩa theo lộ trình ở các phase tiếp theo.
