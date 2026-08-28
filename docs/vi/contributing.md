# Hướng Dẫn Đóng Góp — Backend for All (BFA)

Cảm ơn bạn đã quan tâm đến việc đóng góp cho Backend for All! BFA chào đón mọi lập trình viên từ tất cả các hệ sinh thái ngôn ngữ, các miền ứng dụng và các cộng đồng trên khắp thế giới.

---

## 1. Mười Nguyên Tắc Cốt Lõi

Mọi đóng góp cho BFA cần tuân thủ **Mười Nguyên Tắc Cốt Lõi**:
1. **Mở mặc định (Open by default)**: Mã nguồn mở, cộng đồng sở hữu, không phụ thuộc nhà cung cấp.
2. **Độc lập ngôn ngữ lập trình (Language independent)**: Bình đẳng giữa các ngôn ngữ (All Languages).
3. **Độc lập loại hệ thống (System independent)**: Khối xây dựng cho mọi miền ứng dụng (All Systems).
4. **Tiếp cận toàn cầu (Developer accessible)**: Tài liệu và trải nghiệm đa ngôn ngữ (All Developers).
5. **Code-first**: Mã nguồn trong text thuần là chân lý tối thượng.
6. **GUI-assisted**: Giao diện hỗ trợ mà không tạo ra cơ chế đóng độc quyền.
7. **Khả năng tương tác cao (Interoperable)**: Giao tiếp xuyên ngôn ngữ không rào cản.
8. **Khả năng mở rộng (Extensible)**: Kiến trúc plugin mở cho hạ tầng.
9. **Cộng đồng dẫn dắt (Community-driven)**: Quản trị minh bạch thông qua RFC và bình duyệt.
10. **Ưu tiên đặc tả (Specification-first)**: Chuẩn hóa đặc tả trước khi code.

---

## 2. Các Hình Thức Đóng Góp

Bạn có thể đóng góp vào BFA theo nhiều cách:
- **Đặc tả & Giao thức cốt lõi**: Đề xuất RFC cho mô hình service, định dạng message, universal schema.
- **Language SDKs**: Xây dựng hoặc cải tiến SDK cho các ngôn ngữ (Python, Go, Rust, Java, TypeScript, v.v.).
- **Runtime & Transport**: Phát triển bộ điều phối runtime, các bộ chuyển đổi HTTP/gRPC transport.
- **Plugins & Tích hợp**: Xây dựng connector cho cơ sở dữ liệu, message queue, hệ thống auth, telemetry.
- **Tài liệu & Hướng dẫn**: Viết hướng dẫn kiến trúc, ví dụ hệ thống theo từng domain thực tế.
- **Dịch thuật & Quốc tế hóa**: Dịch tài liệu sang ngôn ngữ mẹ đẻ của bạn và duy trì tính cập nhật.

---

## 3. Quy Trình Đề Xuất RFC (Specification-First)

> [!IMPORTANT]
> BFA được xây dựng trên một nền tảng dùng chung độc lập với ngôn ngữ. **Các thay đổi đối với đặc tả cốt lõi, giao thức truyền thông, kiến trúc runtime và universal schema phải được thảo luận qua RFC / Issue trước khi tiến hành code.**

---

## 4. Quy Trình Đóng Góp Dịch Thuật

Dành cho người đóng góp dịch tài liệu sang ngôn ngữ khu vực:

1. **Đối chiếu tài liệu gốc**: Luôn dựa trên file tiếng Anh chuẩn trong `docs/en/`.
2. **Bảo toàn thuật ngữ kỹ thuật**: Không dịch tên hàm, tên class, identifier trong code, hay mã lỗi máy (`BFA_SERVICE_NOT_FOUND`).
3. **Đảm bảo độ chuẩn xác**: Ưu tiên thuật ngữ kỹ thuật chuẩn xác, dễ hiểu hơn dịch thô sát nghĩa từng từ.
4. **Cấu trúc thư mục**: Đặt file dịch đúng cấu trúc trong `docs/<lang_code>/` khớp với `docs/en/`.
5. **Cập nhật metadata**: Cập nhật tiến độ dịch thuật trong `docs/languages.json`.

---

## 5. Quy Trình Đóng Góp Chung

1. **Fork Repository**  
   Tạo bản fork của `backend-for-all` trên GitHub.

2. **Clone về máy**  
   ```bash
   git clone https://github.com/<your-username>/backend-for-all.git
   cd backend-for-all
   ```

3. **Tạo nhánh Feature Branch**  
   ```bash
   git checkout -b feature/my-contribution
   ```

4. **Thực hiện thay đổi**  
   - Tuân thủ quy chuẩn viết code và format chuẩn.
   - Tuân thủ nguyên tắc "Standard library first" cho các module cốt lõi.
   - Tránh đưa thêm các dependency bên ngoài không cần thiết.

5. **Chạy kiểm thử**  
   ```bash
   pytest
   ```

6. **Mở Pull Request**  
   - Đẩy nhánh lên fork của bạn.
   - Mở Pull Request hướng về nhánh `main` của repository chính.
   - Ghi rõ nội dung thay đổi và liên kết với Issue / RFC liên quan.
