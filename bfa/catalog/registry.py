"""
BFA Master Catalog Registry — Danh Mục 100 Bản Thiết Kế Kiến Trúc Backend Toàn Diện.

Phân loại thành 10 Khối Ngành Công Nghiệp (Mỗi ngành có 10 hệ thống hoàn chỉnh):
1. Thương Mại Điện Tử & Bán Lẻ (1-10)
2. Tài Chính & Ngân Hàng Số (11-20)
3. Mạng Xã Hội & Cộng Đồng (21-30)
4. Giáo Dục & Học Trực Tuyến (31-40)
5. Du Lịch & Khách Sạn (41-50)
6. Y Tế & Chăm Sóc Sức Khỏe (51-60)
7. Vận Tải & Quản Lý Kho Vận (61-70)
8. Phần Mềm Doanh Nghiệp SaaS (71-80)
9. Giải Trí, Phim Ảnh & Game (81-90)
10. Nhà Thông Minh & Đô Thị IoT (91-100)
"""

CATEGORIES = [
    {"key": "ecommerce", "name": "Thương Mại Điện Tử", "count": 10, "icon": "shopping-bag"},
    {"key": "fintech", "name": "Tài Chính & Ngân Hàng", "count": 10, "icon": "credit-card"},
    {"key": "social", "name": "Mạng Xã Hội", "count": 10, "icon": "message-square"},
    {"key": "edtech", "name": "Giáo Dục Trực Tuyến", "count": 10, "icon": "book-open"},
    {"key": "travel", "name": "Du Lịch & Khách Sạn", "count": 10, "icon": "map-pin"},
    {"key": "healthcare", "name": "Y Tế & Sức Khỏe", "count": 10, "icon": "activity"},
    {"key": "logistics", "name": "Vận Tải & Kho Vận", "count": 10, "icon": "truck"},
    {"key": "saas", "name": "Phần Mềm Doanh Nghiệp", "count": 10, "icon": "layers"},
    {"key": "media", "name": "Giải Trí & Truyền Thông", "count": 10, "icon": "play-circle"},
    {"key": "iot", "name": "Nhà Thông Minh & IoT", "count": 10, "icon": "cpu"},
]

BLUEPRINT_CATALOG = {
    # ==========================================================================
    # 1. THƯƠNG MẠI ĐIỆN TỬ & BÁN LẺ (1-10)
    # ==========================================================================
    "b2c_store": {
        "id": 1,
        "category": "ecommerce",
        "name": "Cửa Hàng Bán Lẻ Trực Tuyến",
        "icon": "shopping-cart",
        "description": "Cửa hàng bán lẻ trực tuyến tiêu chuẩn: Giỏ hàng, Đơn hàng, Quản lý tồn kho và Thanh toán số dư ví.",
        "tables": ["users", "products", "orders", "cart_items"],
        "seed_data": {
            "products": [{"id": 1, "name": "Bàn phím cơ RGB", "price": 250000, "stock": 10}],
            "users": [{"id": 1, "username": "huy_dev", "balance": 1000000}],
        },
    },
    "marketplace": {
        "id": 2,
        "category": "ecommerce",
        "name": "Sàn Giao Dịch Nhiều Người Bán",
        "icon": "store",
        "description": "Sàn thương mại điện tử đa người bán: Quản lý gian hàng, Tỷ lệ hoa hồng và Đối soát rút tiền.",
        "tables": ["vendors", "products", "orders", "payouts", "commissions"],
        "seed_data": {
            "vendors": [{"id": 1, "name": "Cửa hàng Công nghệ VN", "rating": 4.9, "balance": 5000000}],
            "products": [{"id": 1, "vendor_id": 1, "name": "Chuột không dây", "price": 150000, "stock": 20}],
        },
    },
    "flash_sale_bidding": {
        "id": 3,
        "category": "ecommerce",
        "name": "Săn Sale Chớp Nhoáng & Đấu Giá",
        "icon": "zap",
        "description": "Hệ thống săn ưu đãi giới hạn thời gian và Đấu giá trực tuyến với bước giá thời gian thực.",
        "tables": ["auctions", "bids", "flash_items", "winners"],
        "seed_data": {
            "auctions": [{"id": 1, "item_name": "Máy ảnh cổ điển", "current_bid": 500000, "highest_bidder_id": 1}],
        },
    },
    "subscription_box": {
        "id": 4,
        "category": "ecommerce",
        "name": "Giao Hàng Định Kỳ Theo Tháng",
        "icon": "package",
        "description": "Dịch vụ giao hộp quà/thực phẩm định kỳ hàng tháng kèm tự động gia hạn hóa đơn thanh toán.",
        "tables": ["subscribers", "box_plans", "deliveries", "billing_cycles"],
        "seed_data": {
            "box_plans": [{"id": 1, "name": "Hộp Khám Phá Cà Phê", "monthly_fee": 300000}],
        },
    },
    "digital_goods": {
        "id": 5,
        "category": "ecommerce",
        "name": "Bán Sản Phẩm Số & Mã Bản Quyền",
        "icon": "key",
        "description": "Bán key phần mềm, sách điện tử, tài liệu số và Tự động phát hành mã kích hoạt sau thanh toán.",
        "tables": ["software_keys", "licenses", "customers", "downloads"],
        "seed_data": {
            "software_keys": [{"id": 1, "product_name": "Khóa Bản Quyền Windows", "key_code": "XXXX-YYYY-ZZZZ", "is_used": 0}],
        },
    },
    "pos_retail": {
        "id": 6,
        "category": "ecommerce",
        "name": "Máy Bán Hàng Tại Quầy Siêu Thị",
        "icon": "printer",
        "description": "Hệ thống máy thu ngân siêu thị: Quét mã vạch, In phiếu thanh toán và Kiểm kê ca làm việc.",
        "tables": ["cashiers", "shifts", "pos_receipts", "barcode_items"],
        "seed_data": {
            "barcode_items": [{"id": 1, "barcode": "89300123", "name": "Nước tăng lực Sting 330ml", "price": 12000}],
        },
    },
    "grocery_delivery": {
        "id": 7,
        "category": "ecommerce",
        "name": "Đi Chợ Hộ & Giao Thực Phẩm Tươi",
        "icon": "shopping-bag",
        "description": "Ứng dụng đi chợ trực tuyến: Danh mục thực phẩm tươi sống, Khung giờ nhận hàng và Người nhặt hàng.",
        "tables": ["grocery_items", "supermarkets", "grocery_orders", "pickers"],
        "seed_data": {
            "grocery_items": [{"id": 1, "name": "Thịt ba chỉ heo 500g", "price": 85000, "weight_kg": 0.5}],
        },
    },
    "rental_marketplace": {
        "id": 8,
        "category": "ecommerce",
        "name": "Sàn Cho Thuê Thiết Bị & Đồ Dùng",
        "icon": "camera",
        "description": "Sàn cho thuê máy ảnh, thiết bị sự kiện và trang phục kèm cơ chế giữ tiền đặt cọc bảo đảm.",
        "tables": ["rental_items", "rental_contracts", "security_deposits", "inspections"],
        "seed_data": {
            "rental_items": [{"id": 1, "name": "Máy ảnh Sony A7IV Ống kính 24-70", "daily_rate": 400000, "deposit_required": 5000000}],
        },
    },
    "voucher_hub": {
        "id": 9,
        "category": "ecommerce",
        "name": "Trung Tâm Mã Giảm Giá & Tích Điểm",
        "icon": "tag",
        "description": "Hệ thống phát hành mã khuyến mãi, Giới hạn lượt sử dụng, Giảm theo phần trăm và Điểm thưởng.",
        "tables": ["vouchers", "voucher_claims", "promo_campaigns", "redemptions"],
        "seed_data": {
            "vouchers": [{"id": 1, "code": "GIAM50K", "discount_amount": 50000, "min_order_value": 200000, "usage_left": 100}],
        },
    },
    "dropshipping_hub": {
        "id": 10,
        "category": "ecommerce",
        "name": "Tự Động Hóa Đơn Hàng Nhà Cung Cấp",
        "icon": "globe",
        "description": "Tự động đẩy đơn hàng sang kho cung ứng bên thứ ba và Cập nhật mã vận đơn theo dõi lộ trình.",
        "tables": ["suppliers", "supplier_products", "dropship_orders", "sync_logs"],
        "seed_data": {
            "suppliers": [{"id": 1, "name": "Tổng Kho Cung Ứng Toàn Cầu", "api_endpoint": "https://api.supplier.com"}],
        },
    },

    # ==========================================================================
    # 2. TÀI CHÍNH & NGÂN HÀNG SỐ (11-20)
    # ==========================================================================
    "digital_wallet": {
        "id": 11,
        "category": "fintech",
        "name": "Ví Điện Tử Cá Nhân",
        "icon": "credit-card",
        "description": "Hệ thống ví điện tử: Nạp tiền, Rút tiền, Chuyển tiền người sang người và Đối soát số dư hai phía.",
        "tables": ["wallets", "transactions", "beneficiaries", "bank_links"],
        "seed_data": {
            "wallets": [{"id": 1, "user_id": 101, "balance": 2500000, "currency": "VND"}],
        },
    },
    "p2p_lending": {
        "id": 12,
        "category": "fintech",
        "name": "Sàn Cho Vay Ngang Hàng",
        "icon": "users",
        "description": "Kết nối người cần vay và nhà đầu tư: Chấm điểm tín nhiệm, Hợp đồng vay vốn và Lịch thu hồi nợ.",
        "tables": ["borrowers", "investors", "loan_applications", "repayment_schedules"],
        "seed_data": {
            "loan_applications": [{"id": 1, "borrower_id": 1, "amount": 20000000, "interest_rate": 12.5, "status": "DA_DUYET"}],
        },
    },
    "crypto_ledger": {
        "id": 13,
        "category": "fintech",
        "name": "Sổ Cái Tài Sản Kỹ Thuật Số",
        "icon": "circle",
        "description": "Sổ cái quản lý tài sản số: Quản lý số dư mã token, Lịch sử nạp rút và Báo cáo lãi lỗ danh mục.",
        "tables": ["crypto_accounts", "token_balances", "ledger_entries", "gas_fees"],
        "seed_data": {
            "token_balances": [{"id": 1, "symbol": "BTC", "amount": 0.5, "symbol_usd": 65000}],
        },
    },
    "payment_gateway": {
        "id": 14,
        "category": "fintech",
        "name": "Cổng Trung Gian Thanh Toán",
        "icon": "shield",
        "description": "Cổng thanh toán điện tử: Tạo mã QR thanh toán, Xác thực chữ ký số bảo mật và Gửi thông báo tự động.",
        "tables": ["merchants", "payment_intents", "webhook_logs", "chargebacks"],
        "seed_data": {
            "merchants": [{"id": 1, "merchant_name": "Công ty Trò Chơi X", "api_key": "sec_key_live_999"}],
        },
    },
    "expense_splitter": {
        "id": 15,
        "category": "fintech",
        "name": "Quản Lý & Chia Tiền Nhóm",
        "icon": "pie-chart",
        "description": "Quản lý chi tiêu chuyến đi du lịch / bạn cùng phòng và Thuật toán tối ưu hóa số lần hoàn trả tiền.",
        "tables": ["groups", "expenses", "expense_shares", "debt_settlements"],
        "seed_data": {
            "groups": [{"id": 1, "name": "Chuyến Đi Đà Lạt", "total_spent": 4500000}],
        },
    },
    "payroll_system": {
        "id": 16,
        "category": "fintech",
        "name": "Tính Lương & Thuế Tự Động",
        "icon": "dollar-sign",
        "description": "Tính toán bảng lương hàng tháng, Thuế thu nhập cá nhân, Bảo hiểm xã hội và Xuất phiếu lương điện tử.",
        "tables": ["employees", "salary_structures", "payslips", "tax_deductions"],
        "seed_data": {
            "employees": [{"id": 1, "name": "Nguyễn Văn A", "base_salary": 25000000, "allowance": 2000000}],
        },
    },
    "invoice_factoring": {
        "id": 17,
        "category": "fintech",
        "name": "Hóa Đơn Điện Tử & Ứng Vốn",
        "icon": "file-text",
        "description": "Phát hành hóa đơn điện tử doanh nghiệp và Dịch vụ ứng vốn hóa đơn thương mại cho công ty nhỏ.",
        "tables": ["invoices", "invoice_items", "factoring_deals", "debtors"],
        "seed_data": {
            "invoices": [{"id": 1, "invoice_no": "HD-2026-001", "amount": 120000000, "status": "DA_UNG_VON"}],
        },
    },
    "stock_broker": {
        "id": 18,
        "category": "fintech",
        "name": "Sàn Khớp Lệnh Chứng Khoán",
        "icon": "trending-up",
        "description": "Khớp lệnh mua bán cổ phiếu, Quản lý tài khoản ký quỹ đòn bẩy và Bảng giá giao dịch trực tuyến.",
        "tables": ["investor_accounts", "order_book", "trade_executions", "stock_symbols"],
        "seed_data": {
            "stock_symbols": [{"id": 1, "symbol": "VNM", "current_price": 72000, "ceil_price": 77000}],
        },
    },
    "loyalty_points_bank": {
        "id": 19,
        "category": "fintech",
        "name": "Ngân Hàng Điểm Tích Lũy Đổi Quà",
        "icon": "award",
        "description": "Hệ thống quản lý điểm thưởng hội viên: Tích lũy điểm, Đổi quà tặng và Nâng hạng thành viên VIP.",
        "tables": ["members", "points_ledger", "rewards_catalog", "claims"],
        "seed_data": {
            "members": [{"id": 1, "name": "Trần Thị B", "tier": "HANG_VANG", "points": 1450}],
        },
    },
    "micro_insurance": {
        "id": 20,
        "category": "fintech",
        "name": "Bảo Hiểm Vi Mô Tự Động Bồi Thường",
        "icon": "umbrella",
        "description": "Bảo hiểm vi mô theo chuyến đi/ngày: Mua gói nhanh chóng và Tự động bồi thường khi phát hiện sự cố.",
        "tables": ["policies", "coverage_plans", "claims", "payout_logs"],
        "seed_data": {
            "coverage_plans": [{"id": 1, "title": "Bảo Hiểm Trễ Chuyến Bay", "premium": 35000, "payout": 500000}],
        },
    },

    # ==========================================================================
    # 3. MẠNG XÃ HỘI & CỘNG ĐỒNG (21-30)
    # ==========================================================================
    "microblogging": {
        "id": 21,
        "category": "social",
        "name": "Mạng Xã Hội Bài Viết Ngắn",
        "icon": "feather",
        "description": "Mạng xã hội đăng trạng thái ngắn, Chia sẻ lại bài viết, Gắn thẻ từ khóa, Dòng thời gian và Theo dõi.",
        "tables": ["users", "tweets", "retweets", "follows", "hashtags"],
        "seed_data": {
            "tweets": [{"id": 1, "author_id": 1, "content": "Xin chào Backend for All! #BFA", "likes": 42}],
        },
    },
    "community_forum": {
        "id": 22,
        "category": "social",
        "name": "Diễn Đàn Thảo Luận Cộng Đồng",
        "icon": "message-circle",
        "description": "Diễn đàn chia sẻ chủ đề: Chuyên mục con, Bỏ phiếu tán thành/phản đối và Bình luận phân cấp cây.",
        "tables": ["subreddits", "posts", "comments", "votes", "moderators"],
        "seed_data": {
            "subreddits": [{"id": 1, "name": "chuyen-muc-backend", "description": "Tất cả về kiến trúc máy chủ"}],
        },
    },
    "qa_stackoverflow": {
        "id": 23,
        "category": "social",
        "name": "Hỏi Đáp Kỹ Thuật & Điểm Uy Tín",
        "icon": "help-circle",
        "description": "Nền tảng hỏi đáp lập trình: Đặt câu hỏi, Trả lời, Đánh dấu giải pháp chuẩn và Tích lũy huy hiệu uy tín.",
        "tables": ["questions", "answers", "tags", "reputations", "badges"],
        "seed_data": {
            "questions": [{"id": 1, "title": "Cách kết nối BFA với cơ sở dữ liệu PostgreSQL?", "views": 128}],
        },
    },
    "dating_matchmaking": {
        "id": 24,
        "category": "social",
        "name": "Ghép Đôi & Hẹn Hò Trực Tuyến",
        "icon": "heart",
        "description": "Ứng dụng kết bạn theo sở thích: Vuốt bày tỏ yêu thích, Ghép đôi thành công và Phòng nhắn tin riêng.",
        "tables": ["profiles", "swipes", "matches", "conversations"],
        "seed_data": {
            "profiles": [{"id": 1, "name": "Bảo Ngọc", "age": 24, "bio": "Thích nghe nhạc và đi du lịch"}],
        },
    },
    "professional_network": {
        "id": 25,
        "category": "social",
        "name": "Mạng Lưới Tuyển Dụng Nghề Nghiệp",
        "icon": "briefcase",
        "description": "Mạng xã hội việc làm: Hồ sơ năng lực ứng viên, Đăng tin tuyển dụng và Nộp hồ sơ ứng tuyển trực tuyến.",
        "tables": ["candidates", "job_postings", "job_applications", "skill_endorsements"],
        "seed_data": {
            "job_postings": [{"id": 1, "title": "Kỹ Sư Backend Cao Cấp", "salary_range": "35-50 Triệu VNĐ"}],
        },
    },
    "instant_messaging": {
        "id": 26,
        "category": "social",
        "name": "Máy Chủ Nhắn Tin Thời Gian Thực",
        "icon": "message-square",
        "description": "Hệ thống trò chuyện tức thì: Nhắn tin trực tiếp đôi, Nhóm thảo luận và Đếm tin nhắn chưa đọc.",
        "tables": ["channels", "members", "messages", "attachments", "reactions"],
        "seed_data": {
            "channels": [{"id": 1, "name": "Kênh Thảo Luận Chung", "is_group": 1}],
        },
    },
    "short_video_feed": {
        "id": 27,
        "category": "social",
        "name": "Nền Tảng Video Ngắn Đề Xuất",
        "icon": "video",
        "description": "Ứng dụng video ngắn: Luồng video đề xuất thông minh, Thả tim, Chia sẻ và Kho âm thanh nhạc nền.",
        "tables": ["videos", "sounds", "likes", "shares", "creators"],
        "seed_data": {
            "videos": [{"id": 1, "title": "Xây dựng hệ thống Backend trong 5 phút", "duration_sec": 45, "views": 1500}],
        },
    },
    "livestream_hub": {
        "id": 28,
        "category": "social",
        "name": "Kênh Phát Trực Tiếp & Quà Ảo",
        "icon": "radio",
        "description": "Trung tâm phát sóng trực tiếp: Khóa luồng phát, Bình luận trực tiếp và Tặng vật phẩm quà ảo.",
        "tables": ["streams", "streamers", "live_comments", "virtual_gifts", "donations"],
        "seed_data": {
            "streams": [{"id": 1, "title": "Lập trình trực tiếp cùng BFA Studio", "viewer_count": 350, "status": "DANG_PHAT"}],
        },
    },
    "event_meetup": {
        "id": 29,
        "category": "social",
        "name": "Tổ Chức Sự Kiện & Soát Vé QR",
        "icon": "calendar",
        "description": "Hệ thống quản lý sự kiện cộng đồng: Đăng ký vé tham dự, Mã vé điện tử và Điểm danh quét mã tại cửa.",
        "tables": ["events", "attendees", "tickets", "checkins", "speakers"],
        "seed_data": {
            "events": [{"id": 1, "title": "Hội Nghị Công Nghệ Backend 2026", "location": "TP. Hồ Chí Minh", "capacity": 500}],
        },
    },
    "gaming_guild": {
        "id": 30,
        "category": "social",
        "name": "Quản Lý Bang Hội Game Thủ",
        "icon": "shield",
        "description": "Nền tảng bang hội trò chơi: Lịch phối hợp sự kiện, Phân chia chiến lợi phẩm và Xếp hạng cống hiến.",
        "tables": ["guilds", "guild_members", "boss_raids", "loot_distributions"],
        "seed_data": {
            "guilds": [{"id": 1, "guild_name": "Chiến Binh Rồng", "level": 10, "leader_id": 1}],
        },
    },

    # ==========================================================================
    # 4. GIÁO DỤC & HỌC TRỰC TUYẾN (31-40)
    # ==========================================================================
    "online_course_lms": {
        "id": 31,
        "category": "edtech",
        "name": "Hệ Thống Khóa Học Trực Tuyến",
        "icon": "book-open",
        "description": "Nền tảng học trực tuyến: Quản lý khóa học, Bài giảng video, Tiến độ học và Cấp chứng chỉ điện tử.",
        "tables": ["courses", "lessons", "enrollments", "certificates", "instructors"],
        "seed_data": {
            "courses": [{"id": 1, "title": "Làm Chủ Kiến Trúc Backend Hiện Đại", "price": 499000, "rating": 5.0}],
        },
    },
    "live_tutoring": {
        "id": 32,
        "category": "edtech",
        "name": "Đặt Lịch Gia Sư Trực Tuyến 1-1",
        "icon": "user-check",
        "description": "Kết nối học sinh và gia sư: Chọn khung giờ rảnh, Phòng học trực tuyến và Đánh giá chất lượng dạy.",
        "tables": ["tutors", "students", "sessions", "reviews", "time_slots"],
        "seed_data": {
            "tutors": [{"id": 1, "name": "Thầy Nam", "subject": "Toán Học & Lập Trình", "hourly_rate": 200000}],
        },
    },
    "online_examination": {
        "id": 33,
        "category": "edtech",
        "name": "Thi Trắc Nghiệm & Chấm Điểm Tự Động",
        "icon": "edit-3",
        "description": "Tổ chức thi trực tuyến: Ngân hàng câu hỏi trắc nghiệm, Xáo trộn đề thi và Chấm điểm kết quả tự động.",
        "tables": ["exams", "questions", "question_options", "submissions", "results"],
        "seed_data": {
            "exams": [{"id": 1, "title": "Kỳ Thi Đánh Giá Năng Lực Lập Trình", "duration_mins": 60, "total_points": 100}],
        },
    },
    "student_information": {
        "id": 34,
        "category": "edtech",
        "name": "Quản Lý Đào Tạo & Tín Chỉ Đại Học",
        "icon": "clipboard",
        "description": "Hệ thống quản lý trường học: Hồ sơ sinh viên, Đăng ký tín chỉ môn học và Bảng điểm tổng kết học kỳ.",
        "tables": ["students", "majors", "classes", "course_registrations", "grade_records"],
        "seed_data": {
            "students": [{"id": 1, "student_code": "SV202601", "name": "Lê Hoàng", "gpa": 3.8}],
        },
    },
    "flashcard_spaced_repetition": {
        "id": 35,
        "category": "edtech",
        "name": "Thẻ Ghi Nhớ Lặp Lại Ngắt Quãng",
        "icon": "layers",
        "description": "Học từ vựng và kiến thức bằng thẻ nhớ hai mặt kết hợp thuật toán tối ưu hóa trí nhớ dài hạn.",
        "tables": ["decks", "cards", "review_logs", "retention_stats"],
        "seed_data": {
            "cards": [{"id": 1, "front": "Tính chất Idempotent là gì?", "back": "Một thao tác gọi nhiều lần vẫn tạo ra cùng một kết quả trạng thái"}],
        },
    },
    "language_learning": {
        "id": 36,
        "category": "edtech",
        "name": "Lộ Trình Học Ngoại Ngữ Theo Cấp Độ",
        "icon": "globe",
        "description": "Ứng dụng học ngoại ngữ: Cây bài học theo cấp độ, Điểm kinh nghiệm và Chuỗi ngày học liên tục.",
        "tables": ["languages", "skill_trees", "units", "user_streaks", "quizzes"],
        "seed_data": {
            "languages": [{"id": 1, "name": "Tiếng Anh", "code": "en", "learners_count": 12000}],
        },
    },
    "digital_credentials": {
        "id": 37,
        "category": "edtech",
        "name": "Phát Hành & Tra Cứu Chứng Chỉ Số",
        "icon": "award",
        "description": "Cấp phát và xác thực văn bằng, chứng chỉ kỹ thuật số toàn cầu kèm mã xác minh trực tuyến.",
        "tables": ["issuers", "credential_types", "issued_credentials", "verification_logs"],
        "seed_data": {
            "credential_types": [{"id": 1, "title": "Chứng Chỉ Kiến Trúc Sư Backend BFA", "validity_years": 3}],
        },
    },
    "online_code_judge": {
        "id": 38,
        "category": "edtech",
        "name": "Hệ Thống Chấm Bài Lập Trình Tự Động",
        "icon": "code",
        "description": "Nền tảng luyện thuật toán: Bài tập lập trình, Bộ kiểm thử đầu vào/đầu ra và Giới hạn thời gian bộ nhớ.",
        "tables": ["problems", "test_cases", "code_submissions", "leaderboards"],
        "seed_data": {
            "problems": [{"id": 1, "title": "Tổng Hai Số Trong Mảng", "difficulty": "DE", "time_limit_ms": 1000}],
        },
    },
    "academic_archive": {
        "id": 39,
        "category": "edtech",
        "name": "Kho Lưu Trữ Luận Văn & Bài Báo",
        "icon": "book",
        "description": "Thư viện lưu trữ luận văn khoa học: Danh mục tác giả, Trích dẫn học thuật và Tìm kiếm toàn văn.",
        "tables": ["papers", "authors", "citations", "categories", "downloads"],
        "seed_data": {
            "papers": [{"id": 1, "title": "Nền Tảng Backend Đa Ngôn Ngữ Hóa Toàn Diện", "year": 2026}],
        },
    },
    "library_management": {
        "id": 40,
        "category": "edtech",
        "name": "Quản Lý Mượn Trả Sách Thư Viện",
        "icon": "archive",
        "description": "Hệ thống thư viện sách: Danh mục đầu sách, Thẻ mượn độc giả, Hạn hoàn trả và Phí trễ hạn.",
        "tables": ["books", "borrowers", "borrow_records", "fines"],
        "seed_data": {
            "books": [{"id": 1, "title": "Thiết Kế Ứng Dụng Dữ Liệu Lớn", "isbn": "9781449373320", "copies_available": 3}],
        },
    },

    # ==========================================================================
    # 5. DU LỊCH & KHÁCH SẠN (41-50)
    # ==========================================================================
    "hotel_reservation": {
        "id": 41,
        "category": "travel",
        "name": "Đặt Phòng Khách Sạn & Khu Nghỉ Dưỡng",
        "icon": "home",
        "description": "Hệ thống khách sạn: Quản lý loại phòng, Kiểm tra phòng trống theo ngày và Thủ tục nhận/trả phòng.",
        "tables": ["hotels", "room_types", "rooms", "bookings", "guests"],
        "seed_data": {
            "room_types": [{"id": 1, "name": "Phòng Cao Cấp Hướng Biển", "price_per_night": 1200000, "capacity": 2}],
        },
    },
    "flight_booking": {
        "id": 42,
        "category": "travel",
        "name": "Đặt Vé Máy Bay & Chọn Ghế Ngồi",
        "icon": "navigation",
        "description": "Đặt vé chuyến bay: Tuyến bay nội địa/quốc tế, Hạng vé, Sơ đồ chọn chỗ ngồi và Thẻ lên máy bay.",
        "tables": ["flights", "airports", "seat_maps", "passengers", "tickets"],
        "seed_data": {
            "flights": [{"id": 1, "flight_code": "VN123", "origin": "HAN", "destination": "SGN", "price": 1500000}],
        },
    },
    "homestay_rental": {
        "id": 43,
        "category": "travel",
        "name": "Đặt Căn Hộ Nghỉ Dưỡng & Homestay",
        "icon": "home",
        "description": "Cho thuê căn hộ và biệt thự: Lịch đón khách của chủ nhà, Đánh giá sao và Quy định hủy phòng.",
        "tables": ["properties", "hosts", "reservations", "reviews", "amenities"],
        "seed_data": {
            "properties": [{"id": 1, "title": "Biệt Thự Rừng Thông Đà Lạt", "price_per_night": 2500000, "bedrooms": 3}],
        },
    },
    "tour_booking": {
        "id": 44,
        "category": "travel",
        "name": "Đặt Tour Du Lịch & Trải Nghiệm",
        "icon": "map",
        "description": "Tour du lịch trọn gói: Lịch trình chi tiết từng ngày, Hướng dẫn viên và Số lượng chỗ còn nhận.",
        "tables": ["tours", "itineraries", "tour_departures", "tour_guides", "bookings"],
        "seed_data": {
            "tours": [{"id": 1, "name": "Tour Khám Phá Vịnh Hạ Long 2 Ngày 1 Đêm", "price": 2200000, "seats_left": 8}],
        },
    },
    "vehicle_rental": {
        "id": 45,
        "category": "travel",
        "name": "Thuê Xe Tự Lái & Xe Máy Du Lịch",
        "icon": "truck",
        "description": "Cho thuê phương tiện di chuyển: Bảng giá theo ngày, Giữ tiền đặt cọc và Biên bản bàn giao xe.",
        "tables": ["vehicles", "rental_orders", "damage_reports", "deposit_holds"],
        "seed_data": {
            "vehicles": [{"id": 1, "model": "VinFast VF8", "daily_rate": 1100000, "license_plate": "51K-12345"}],
        },
    },
    "restaurant_table_booking": {
        "id": 46,
        "category": "travel",
        "name": "Đặt Bàn Nhà Hàng & Chọn Món Trước",
        "icon": "coffee",
        "description": "Đặt bàn ăn trước: Sơ đồ vị trí bàn, Chọn trước thực đơn món ăn và Tiền đặt cọc giữ chỗ tiệc.",
        "tables": ["restaurants", "dining_tables", "table_reservations", "preorder_menus"],
        "seed_data": {
            "dining_tables": [{"id": 1, "table_no": "BAN-VIP-01", "capacity": 6, "is_available": 1}],
        },
    },
    "travel_itinerary": {
        "id": 47,
        "category": "travel",
        "name": "Lên Lịch Trình Chuyến Đi Cá Nhân",
        "icon": "calendar",
        "description": "Kế hoạch chuyến đi tự túc: Danh sách điểm đến từng ngày, Dự toán ngân sách chi tiêu và Bản đồ.",
        "tables": ["trips", "itinerary_days", "places_to_visit", "budget_items"],
        "seed_data": {
            "trips": [{"id": 1, "destination": "Đà Nẵng - Hội An", "duration_days": 4, "budget_limit": 6000000}],
        },
    },
    "visa_service": {
        "id": 48,
        "category": "travel",
        "name": "Dịch Vụ Nộp & Tra Cứu Thị Thực",
        "icon": "file-text",
        "description": "Nộp hồ sơ xin visa: Danh mục giấy tờ cần nộp và Theo dõi tiến trình phê duyệt hồ sơ thị thực.",
        "tables": ["visa_applications", "document_checklists", "embassy_statuses"],
        "seed_data": {
            "visa_applications": [{"id": 1, "country": "Nhật Bản", "applicant_name": "Phan Thị C", "status": "DANG_XU_LY"}],
        },
    },
    "luggage_storage": {
        "id": 49,
        "category": "travel",
        "name": "Gửi Giữ & Chuyển Hành Lý Khách Sạn",
        "icon": "briefcase",
        "description": "Dịch vụ giữ hành lý tại sân bay/nhà ga và Vận chuyển hành lý thẳng đến khu nghỉ dưỡng.",
        "tables": ["storage_points", "luggage_tickets", "delivery_routes"],
        "seed_data": {
            "storage_points": [{"id": 1, "location_name": "Sân Bay Tân Sơn Nhất - Ga Quốc Tế", "hourly_fee": 30000}],
        },
    },
    "cruise_booking": {
        "id": 50,
        "category": "travel",
        "name": "Đặt Vé Du Thuyền & Phòng Cabin",
        "icon": "anchor",
        "description": "Đặt hải trình du thuyền biển: Lộ trình qua các vịnh biển, Chọn hạng phòng cabin và Gói ẩm thực.",
        "tables": ["cruise_ships", "voyages", "cabins", "cruise_bookings"],
        "seed_data": {
            "voyages": [{"id": 1, "cruise_name": "Du Thuyền Hạ Long Sang Trọng", "route": "Hạ Long - Lan Hạ", "price": 4500000}],
        },
    },

    # ==========================================================================
    # 6. Y TẾ & CHĂM SÓC SỨC KHỎE (51-60)
    # ==========================================================================
    "clinic_appointment": {
        "id": 51,
        "category": "healthcare",
        "name": "Đặt Lịch Khám Phòng Khám Chuyên Khoa",
        "icon": "plus-square",
        "description": "Hệ thống phòng khám: Lựa chọn bác sĩ chuyên khoa, Khung giờ khám bệnh và Cấp số thứ tự điện tử.",
        "tables": ["doctors", "specialties", "appointments", "queues", "patients"],
        "seed_data": {
            "doctors": [{"id": 1, "name": "Bác Sĩ Nguyễn Văn D", "specialty": "Chuyên Khoa Tim Mạch", "room_no": "P204"}],
        },
    },
    "electronic_health_record": {
        "id": 52,
        "category": "healthcare",
        "name": "Bệnh Án Điện Tử & Tiền Sử Bệnh",
        "icon": "file-plus",
        "description": "Hồ sơ sức khỏe điện tử: Tiền sử dị ứng, Lịch sử tiêm chủng, Chỉ số sinh tồn và Toa thuốc đã kê.",
        "tables": ["patient_profiles", "medical_histories", "vital_signs", "prescriptions"],
        "seed_data": {
            "patient_profiles": [{"id": 1, "blood_type": "O+", "allergies": "Kháng sinh Penicillin", "emergency_contact": "0912345678"}],
        },
    },
    "telemedicine": {
        "id": 53,
        "category": "healthcare",
        "name": "Tư Vấn Sức Khỏe Từ Xa Qua Video",
        "icon": "video",
        "description": "Khám bệnh từ xa: Phòng tư vấn video với bác sĩ, Kê đơn thuốc điện tử và Giao thuốc tại nhà.",
        "tables": ["consultation_rooms", "e_prescriptions", "doctor_notes", "payments"],
        "seed_data": {
            "consultation_rooms": [{"id": 1, "patient_id": 1, "doctor_id": 1, "status": "DANG_CHO"}],
        },
    },
    "pharmacy_inventory": {
        "id": 54,
        "category": "healthcare",
        "name": "Quản Lý Nhà Thuốc & Hạn Sử Dụng",
        "icon": "shield",
        "description": "Quản lý kho dược phẩm đạt chuẩn: Quản lý theo số lô và hạn dùng, Bán thuốc theo đơn bác sĩ.",
        "tables": ["medicines", "medicine_batches", "prescriptions", "dispense_logs"],
        "seed_data": {
            "medicines": [{"id": 1, "name": "Thuốc Paracetamol 500mg", "stock": 500, "price": 2000, "active_ingredient": "Acetaminophen"}],
        },
    },
    "lab_test_results": {
        "id": 55,
        "category": "healthcare",
        "name": "Trả Kết Quả Xét Nghiệm Y Khoa",
        "icon": "activity",
        "description": "Quản lý xét nghiệm y học: Kết quả xét nghiệm máu/nước tiểu trực tuyến kèm dải chỉ số tham chiếu chuẩn.",
        "tables": ["test_packages", "test_orders", "lab_results", "reference_ranges"],
        "seed_data": {
            "lab_results": [{"id": 1, "test_name": "Đường Huyết Lúc Đói", "value": 5.2, "unit": "mmol/L", "is_normal": 1}],
        },
    },
    "fitness_tracker": {
        "id": 56,
        "category": "healthcare",
        "name": "Nhật Ký Tập Luyện & Calo Tiêu Thụ",
        "icon": "heart",
        "description": "Theo dõi sức khỏe thể chất: Đếm bước chân hàng ngày, Tính lượng calo tiêu hao và Kế hoạch dinh dưỡng.",
        "tables": ["workouts", "meals", "calorie_logs", "body_metrics"],
        "seed_data": {
            "calorie_logs": [{"id": 1, "date": "2026-08-31", "calories_in": 2100, "calories_burned": 650}],
        },
    },
    "blood_donation_hub": {
        "id": 57,
        "category": "healthcare",
        "name": "Ngân Hàng Máu & Báo Động Khẩn Cấp",
        "icon": "droplet",
        "description": "Mạng lưới hiến máu nhân đạo: Quản lý lượng máu dự trữ và Báo động tìm người hiến nhóm máu hiếm khẩn cấp.",
        "tables": ["blood_donors", "blood_inventory", "urgent_requests", "donation_events"],
        "seed_data": {
            "blood_inventory": [{"id": 1, "blood_type": "O-", "units_available": 15, "hospital_name": "Bệnh Viện Chợ Rẫy"}],
        },
    },
    "elderly_care_sos": {
        "id": 58,
        "category": "healthcare",
        "name": "Giám Sát Người Cao Tuổi & Nút SOS",
        "icon": "bell",
        "description": "Thiết bị chăm sóc người lớn tuổi: Theo dõi nhịp tim, Tự động phát hiện té ngã và Gửi cảnh báo SOS khẩn cấp.",
        "tables": ["elderly_users", "health_telemetry", "sos_alerts", "caregivers"],
        "seed_data": {
            "sos_alerts": [{"id": 1, "user_id": 1, "alert_type": "PHAT_HIEN_TE_NGA", "status": "DA_TIEP_NHAN"}],
        },
    },
    "dental_clinic": {
        "id": 59,
        "category": "healthcare",
        "name": "Hồ Sơ Răng Miệng & Nha Khoa",
        "icon": "smile",
        "description": "Quản lý phòng khám nha khoa: Sơ đồ cung răng, Lộ trình niềng răng/cấy ghép và Lịch hẹn tái khám định kỳ.",
        "tables": ["dental_records", "tooth_charts", "treatment_plans", "followups"],
        "seed_data": {
            "treatment_plans": [{"id": 1, "patient_name": "Trần Văn E", "treatment": "Niềng Răng Trong Suốt", "total_sessions": 12}],
        },
    },
    "mental_health_journal": {
        "id": 60,
        "category": "healthcare",
        "name": "Nhật Ký Cảm Xúc & Trị Liệu Tâm Lý",
        "icon": "sun",
        "description": "Chăm sóc sức khỏe tinh thần: Ghi chép cảm xúc hàng ngày, Bài tập hít thở thư giãn và Đặt hẹn chuyên gia.",
        "tables": ["mood_entries", "therapy_sessions", "breathing_exercises", "counselors"],
        "seed_data": {
            "mood_entries": [{"id": 1, "mood_score": 8, "notes": "Cảm thấy vui vẻ và tràn đầy năng lượng hoàn thành công việc"}],
        },
    },

    # ==========================================================================
    # 7. VẬN TẢI & QUẢN LÝ KHO VẬN (61-70)
    # ==========================================================================
    "ride_hailing": {
        "id": 61,
        "category": "logistics",
        "name": "Ứng Dụng Gọi Xe Công Nghệ",
        "icon": "navigation",
        "description": "Hệ thống điều phối xe: Tìm tài xế gần nhất, Tính cước phí tự động theo quãng đường và Định vị chuyến đi.",
        "tables": ["drivers", "passengers", "rides", "fare_rules", "driver_locations"],
        "seed_data": {
            "rides": [{"id": 1, "passenger_id": 1, "driver_id": 10, "pickup": "Quận 1", "dropoff": "Quận 7", "fare": 85000}],
        },
    },
    "last_mile_delivery": {
        "id": 62,
        "category": "logistics",
        "name": "Giao Hàng Chặng Cuối & Thu Hộ COD",
        "icon": "truck",
        "description": "Điều phối nhân viên giao hàng: Chia tuyến đường tối ưu, Thu tiền mặt khi nhận hàng và Chụp ảnh ký nhận.",
        "tables": ["parcels", "shippers", "delivery_trips", "cod_receipts", "proof_of_delivery"],
        "seed_data": {
            "parcels": [{"id": 1, "tracking_code": "VNX-998811", "receiver_name": "Võ Thị F", "cod_amount": 350000}],
        },
    },
    "warehouse_wms": {
        "id": 63,
        "category": "logistics",
        "name": "Quản Lý Vị Trí Ô Kệ Kho Hàng",
        "icon": "archive",
        "description": "Hệ thống quản lý kho: Quản lý vị trí dãy/kệ/ô hàng, Quy trình nhập kho, Lấy hàng theo đơn và Đóng gói.",
        "tables": ["inventory_items", "warehouse_zones", "shelf_bins", "stock_movements"],
        "seed_data": {
            "shelf_bins": [{"id": 1, "bin_code": "KHU-A-KE-03", "capacity_kg": 500, "current_weight_kg": 120}],
        },
    },
    "freight_fleet_management": {
        "id": 64,
        "category": "logistics",
        "name": "Quản Lý Đội Xe Tải Đường Dài",
        "icon": "truck",
        "description": "Điều vận đoàn xe tải liên tỉnh: Lịch bảo dưỡng định kỳ xe, Quản lý định mức xăng dầu và Phù hiệu vận tải.",
        "tables": ["trucks", "drivers", "freight_trips", "fuel_logs", "maintenance_records"],
        "seed_data": {
            "trucks": [{"id": 1, "plate_no": "29H-999.88", "tonnage": 15.0, "status": "DANG_CHAY"}],
        },
    },
    "container_shipping": {
        "id": 65,
        "category": "logistics",
        "name": "Theo Dõi Vận Tải Container Biển",
        "icon": "anchor",
        "description": "Vận chuyển container đường biển: Cảng xếp/dỡ hàng, Vận đơn đường biển và Thủ tục thông quan hải quan.",
        "tables": ["containers", "vessels", "bills_of_lading", "port_checkpoints", "customs_clearances"],
        "seed_data": {
            "containers": [{"id": 1, "container_no": "MSCU1234567", "size": "40HC", "destination_port": "Cảng Cát Lái"}],
        },
    },
    "food_delivery_dispatch": {
        "id": 66,
        "category": "logistics",
        "name": "Giao Đồ Ăn Trực Tuyến Hỏa Tốc",
        "icon": "coffee",
        "description": "Hệ thống giao món ăn: Thực đơn quán ăn, Điều phối tài xế lấy đồ và Theo dõi tiến trình bếp chuẩn bị món.",
        "tables": ["restaurants", "menu_dishes", "food_orders", "couriers"],
        "seed_data": {
            "food_orders": [{"id": 1, "restaurant_id": 1, "total_price": 125000, "status": "DANG_NAU"}],
        },
    },
    "cold_chain_tracking": {
        "id": 67,
        "category": "logistics",
        "name": "Giám Sát Chuỗi Cung Ứng Lạnh",
        "icon": "thermometer",
        "description": "Kiểm soát nhiệt độ thùng đông lạnh: Cảm biến nhiệt độ liên tục và Tự động cảnh báo đứt gãy bảo quản.",
        "tables": ["refrigerated_cargo", "temp_sensor_logs", "temp_violations"],
        "seed_data": {
            "temp_sensor_logs": [{"id": 1, "cargo_id": 1, "temperature_celsius": -18.5, "is_safe": 1}],
        },
    },
    "smart_parking": {
        "id": 68,
        "category": "logistics",
        "name": "Bãi Đỗ Xe Nhận Diện Biển Số AI",
        "icon": "map-pin",
        "description": "Bãi giữ xe thông minh: Camera nhận diện biển số xe tự động, Đóng mở barie và Tính tiền gửi xe tự động.",
        "tables": ["parking_slots", "vehicle_checkins", "parking_rates", "plate_logs"],
        "seed_data": {
            "parking_slots": [{"id": 1, "slot_code": "B1-A08", "is_occupied": 0, "hourly_rate": 15000}],
        },
    },
    "airport_baggage": {
        "id": 69,
        "category": "logistics",
        "name": "Kiểm Soát Hành Lý Sân Bay Thẻ Từ",
        "icon": "briefcase",
        "description": "Theo dõi hành lý máy bay: Quét thẻ từ RFID qua băng chuyền bốc dỡ và Phòng ngừa thất lạc hành lý khách.",
        "tables": ["baggage_tags", "flights", "conveyor_scans", "lost_reports"],
        "seed_data": {
            "baggage_tags": [{"id": 1, "tag_rfid": "THE-RFID-889922", "flight_id": 1, "status": "DA_LEN_MAY_BAY"}],
        },
    },
    "waste_management_routing": {
        "id": 70,
        "category": "logistics",
        "name": "Tối Ưu Tuyến Đường Thu Gom Rác",
        "icon": "trash-2",
        "description": "Điều phối xe gom rác đô thị: Cảm biến mức độ đầy của thùng rác công cộng và Tối ưu tuyến đường xe chạy.",
        "tables": ["smart_bins", "garbage_trucks", "collection_routes", "fill_levels"],
        "seed_data": {
            "smart_bins": [{"id": 1, "location": "Công viên 23 Tháng 9", "fill_percentage": 85, "needs_collection": 1}],
        },
    },

    # ==========================================================================
    # 8. PHẦN MỀM DOANH NGHIỆP SAAS (71-80)
    # ==========================================================================
    "crm_sales_pipeline": {
        "id": 71,
        "category": "saas",
        "name": "Quản Lý Khách Hàng & Phễu Bán Hàng",
        "icon": "target",
        "description": "Hệ thống chăm sóc khách hàng: Phễu bán hàng, Lịch sử liên hệ tư vấn và Theo dõi tỷ lệ chốt hợp đồng.",
        "tables": ["leads", "deals", "contacts", "sales_stages", "call_logs"],
        "seed_data": {
            "deals": [{"id": 1, "deal_name": "Gói Bản Quyền Doanh Nghiệp 500 Chỗ", "value": 50000000, "stage": "DANG_BAO_GIA"}],
        },
    },
    "project_management_kanban": {
        "id": 72,
        "category": "saas",
        "name": "Bảng Công Việc & Tiến Độ Dự Án",
        "icon": "trello",
        "description": "Quản lý công việc dự án linh hoạt: Bảng kéo thả công việc, Phân công nhiệm vụ và Chu kỳ hoàn thành.",
        "tables": ["projects", "kanban_columns", "tasks", "task_assignees", "sprints"],
        "seed_data": {
            "tasks": [{"id": 1, "title": "Hoàn thiện 100 Bản Thiết Kế Backend BFA", "status": "DANG_LAM", "priority": "CAO"}],
        },
    },
    "helpdesk_support": {
        "id": 73,
        "category": "saas",
        "name": "Tiếp Nhận & Xử Lý Yêu Cầu Hỗ Trợ",
        "icon": "headphones",
        "description": "Tổng đài hỗ trợ kỹ thuật: Tiếp nhận phiếu yêu cầu (Ticket), Phân công chuyên viên và Đo lường thời gian xử lý.",
        "tables": ["tickets", "ticket_replies", "support_agents", "sla_policies"],
        "seed_data": {
            "tickets": [{"id": 1, "subject": "Hỏi cách kết nối MySQL", "priority": "KHAN_CAP", "status": "DANG_MO"}],
        },
    },
    "hrm_attendance": {
        "id": 74,
        "category": "saas",
        "name": "Chấm Công & Duyệt Đơn Nghỉ Phép",
        "icon": "users",
        "description": "Quản trị nhân sự: Điểm danh chấm công qua vị trí/mạng văn phòng, Nộp và phê duyệt đơn xin nghỉ phép năm.",
        "tables": ["employees", "attendance_punches", "leave_requests", "holidays"],
        "seed_data": {
            "leave_requests": [{"id": 1, "employee_name": "Nguyễn Văn G", "leave_type": "PHEP_NAM", "days": 2, "status": "DA_DUYET"}],
        },
    },
    "okr_kpi_tracker": {
        "id": 75,
        "category": "saas",
        "name": "Theo Dõi Mục Tiêu & Chỉ Số Hiệu Quả",
        "icon": "target",
        "description": "Quản trị chiến lược doanh nghiệp: Mục tiêu cốt lõi và Các kết quả then chốt đo lường tiến độ công ty.",
        "tables": ["objectives", "key_results", "checkins", "departments"],
        "seed_data": {
            "objectives": [{"id": 1, "title": "Đạt 1,000 Lượt Đánh Giá Yêu Thích Trên GitHub", "progress_pct": 65}],
        },
    },
    "contract_e_signature": {
        "id": 76,
        "category": "saas",
        "name": "Trình Ký Hợp Đồng Điện Tử Nhiều Bên",
        "icon": "edit-2",
        "description": "Ký kết văn bản điện tử: Tải tệp hợp đồng PDF, Thiết lập vị trí chữ ký và Gửi mã xác thực ký số an toàn.",
        "tables": ["contracts", "signers", "signatures", "audit_trails"],
        "seed_data": {
            "contracts": [{"id": 1, "title": "Hợp Đồng Cung Cấp Dịch Vụ Máy Chủ", "status": "CHO_KY_SO"}],
        },
    },
    "enterprise_asset_tagging": {
        "id": 77,
        "category": "saas",
        "name": "Quản Lý Tài Sản & Thiết Bị Công Ty",
        "icon": "tag",
        "description": "Kiểm kê tài sản cố định: Máy tính xách tay, Màn hình, Biên bản bàn giao nhân viên và Tính khấu hao hàng năm.",
        "tables": ["assets", "asset_assignments", "maintenance_history", "depreciations"],
        "seed_data": {
            "assets": [{"id": 1, "asset_tag": "MAY-TINH-001", "name": "Máy Tính Xách Tay Chuyên Dụng", "assigned_to": 1}],
        },
    },
    "feedback_nps_survey": {
        "id": 78,
        "category": "saas",
        "name": "Khảo Sát Điểm Hài Lòng Khách Hàng",
        "icon": "star",
        "description": "Thu thập ý kiến đánh giá: Đo lường chỉ số mức độ hài lòng khách hàng và Phân loại ý kiến đóng góp.",
        "tables": ["surveys", "survey_responses", "nps_scores", "feedback_tags"],
        "seed_data": {
            "nps_scores": [{"id": 1, "score": 10, "feedback": "BFA Studio sử dụng rất tiện lợi và tốc độ xử lý nhanh"}],
        },
    },
    "multi_tenant_provisioning": {
        "id": 79,
        "category": "saas",
        "name": "Không Gian Làm Việc Đa Doanh Nghiệp",
        "icon": "grid",
        "description": "Cấp phát không gian tổ chức riêng biệt: Tên miền phụ độc lập và Phân quyền vai trò quản trị/thành viên.",
        "tables": ["tenants", "tenant_users", "roles", "tenant_subscriptions"],
        "seed_data": {
            "tenants": [{"id": 1, "subdomain": "cong-ty-acme", "company_name": "Tập Đoàn Toàn Cầu Acme", "plan": "CHUYEN_NGHIEP"}],
        },
    },
    "procurement_purchase_order": {
        "id": 80,
        "category": "saas",
        "name": "Quy Trình Phê Duyệt Đề Xuất Mua Sắm",
        "icon": "shopping-cart",
        "description": "Mua sắm trang thiết bị nội bộ: Phiếu yêu cầu mua sắm, Xét duyệt hạn mức tài chính và Xuất đơn đặt hàng.",
        "tables": ["purchase_requests", "purchase_orders", "approval_workflows", "vendors"],
        "seed_data": {
            "purchase_orders": [{"id": 1, "po_number": "DH-2026-88", "total_cost": 45000000, "status": "DA_PHE_DUYET"}],
        },
    },

    # ==========================================================================
    # 9. GIẢI TRÍ, PHIM ẢNH & GAME (81-90)
    # ==========================================================================
    "video_streaming_vod": {
        "id": 81,
        "category": "media",
        "name": "Xem Phim Trực Tuyến & Danh Sách Xem",
        "icon": "film",
        "description": "Nền tảng xem phim chất lượng cao: Danh mục phim, Quản lý tập phim, Xem tiếp đoạn dở và Phụ đề nhiều thứ tiếng.",
        "tables": ["movies", "episodes", "watch_history", "subtitles", "watchlists"],
        "seed_data": {
            "movies": [{"id": 1, "title": "Ma Trận Hồi Sinh", "release_year": 2026, "duration_mins": 138}],
        },
    },
    "music_streaming": {
        "id": 82,
        "category": "media",
        "name": "Nghe Nhạc Trực Tuyến & Danh Sách Phát",
        "icon": "music",
        "description": "Dịch vụ phát nhạc trực tuyến: Bài hát, Album nghệ sĩ, Danh sách phát cá nhân và Bảng xếp hạng thịnh hành.",
        "tables": ["tracks", "artists", "albums", "playlists", "play_counts"],
        "seed_data": {
            "tracks": [{"id": 1, "title": "Bản Giao Hưởng Backend", "artist": "Huy Nguyễn", "duration_sec": 240}],
        },
    },
    "podcast_hosting": {
        "id": 83,
        "category": "media",
        "name": "Phát Hành Âm Thanh & Kênh Thảo Luận",
        "icon": "mic",
        "description": "Phát hành bản ghi âm chuyên đề: Quản lý các tập phát sóng và Tự động phân phối luồng phát thanh chuẩn.",
        "tables": ["podcasts", "episodes", "rss_feeds", "subscriber_metrics"],
        "seed_data": {
            "podcasts": [{"id": 1, "title": "Chuyện Nghề Kỹ Sư Máy Chủ", "author": "Huy Nguyễn"}],
        },
    },
    "news_editorial_cms": {
        "id": 84,
        "category": "media",
        "name": "Tòa Soạn Báo Điện Tử & Nhuận Bút",
        "icon": "file-text",
        "description": "Tòa soạn tin tức: Biên tập bài viết, Tính nhuận bút tác giả, Phê duyệt xuất bản và Thống kê lượt xem bài.",
        "tables": ["articles", "authors", "categories", "royalties", "page_views"],
        "seed_data": {
            "articles": [{"id": 1, "headline": "BFA Ra Mắt 100 Kiến Trúc Backend Miễn Phí", "status": "DA_XUAT_BAN"}],
        },
    },
    "cinema_ticketing": {
        "id": 85,
        "category": "media",
        "name": "Bán Vé Xem Phim & Chọn Ghế Rạp",
        "icon": "tag",
        "description": "Đặt vé rạp chiếu phim và đêm nhạc: Sơ đồ chọn ghế theo thời gian thực và Quét mã vé vào cửa.",
        "tables": ["showtimes", "cinema_halls", "seats", "ticket_bookings"],
        "seed_data": {
            "showtimes": [{"id": 1, "movie_title": "Siêu Phẩm Avatar Mới", "start_time": "19:30", "price": 110000}],
        },
    },
    "game_matchmaking_lobby": {
        "id": 86,
        "category": "media",
        "name": "Phòng Chờ & Ghép Trận Game Thủ",
        "icon": "crosshair",
        "description": "Sảnh ghép trận thi đấu: Thuật toán ghép đối thủ theo mức điểm kỹ năng và Quản lý phòng chờ trò chơi.",
        "tables": ["game_lobbies", "players", "matchmaking_queues", "game_sessions"],
        "seed_data": {
            "game_lobbies": [{"id": 1, "lobby_name": "Phòng Đấu Xếp Hạng 5 Đấu 5", "max_players": 10, "status": "DANG_CHO"}],
        },
    },
    "leaderboard_achievements": {
        "id": 87,
        "category": "media",
        "name": "Bảng Xếp Hạng & Huy Hiệu Thành Tựu",
        "icon": "award",
        "description": "Bảng xếp hạng điểm số người chơi theo mùa giải và Mở khóa các danh hiệu thành tích trong trò chơi.",
        "tables": ["leaderboards", "player_scores", "achievements", "unlocked_badges"],
        "seed_data": {
            "achievements": [{"id": 1, "title": "Chiến Công Đầu", "points_reward": 50}],
        },
    },
    "game_inventory_trade": {
        "id": 88,
        "category": "media",
        "name": "Hòm Đồ & Chợ Trao Đổi Vật Phẩm",
        "icon": "box",
        "description": "Hòm trang bị nhân vật trò chơi: Phân cấp độ hiếm vật phẩm, Nâng cấp trang bị và Giao dịch giữa người chơi.",
        "tables": ["game_items", "player_inventories", "marketplace_listings", "trades"],
        "seed_data": {
            "game_items": [{"id": 1, "item_name": "Thanh Kiếm Huyền Thoại Cấp 9", "rarity": "HUYEN_THOAI", "attack": 999}],
        },
    },
    "webtoon_comic_reader": {
        "id": 89,
        "category": "media",
        "name": "Đọc Truyện Tranh & Mở Khóa Chương",
        "icon": "book-open",
        "description": "Ứng dụng đọc truyện tranh: Danh sách chương, Mở khóa tập truyện mới bằng xu và Đánh dấu trang yêu thích.",
        "tables": ["comic_series", "chapters", "user_coins", "chapter_unlocks", "bookmarks"],
        "seed_data": {
            "comic_series": [{"id": 1, "title": "Hành Trình Kiến Trúc Sư Backend", "total_chapters": 150}],
        },
    },
    "digital_art_gallery": {
        "id": 90,
        "category": "media",
        "name": "Triển Lãm Tranh & Đấu Giá Nghệ Thuật",
        "icon": "image",
        "description": "Phòng trưng bày tác phẩm nghệ thuật số: Đăng ảnh độ phân giải cao và Đấu giá tác phẩm nghệ thuật độc bản.",
        "tables": ["artworks", "artists", "art_collections", "bids"],
        "seed_data": {
            "artworks": [{"id": 1, "title": "Hoàng Hôn Trên Thành Phố Công Nghệ", "artist_name": "Mai Lan", "price": 8000000}],
        },
    },

    # ==========================================================================
    # 10. NHÀ THÔNG MINH & ĐÔ THỊ IOT (91-100)
    # ==========================================================================
    "smart_home_telemetry": {
        "id": 91,
        "category": "iot",
        "name": "Điều Khiển Thiết Bị Nhà Thông Minh",
        "icon": "home",
        "description": "Hệ thống nhà thông minh: Bật tắt đèn từ xa, Điều khiển điều hòa nhiệt độ, Cảm biến cửa và Ngữ cảnh tự động.",
        "tables": ["devices", "device_states", "automation_rules", "telemetry_logs"],
        "seed_data": {
            "devices": [{"id": 1, "device_name": "Đèn Phòng Khách", "device_type": "DEN_CHIEU_SANG", "is_on": 1, "brightness": 80}],
        },
    },
    "weather_sensor_network": {
        "id": 92,
        "category": "iot",
        "name": "Trạm Quan Trắc Thời Tiết & Chất Lượng Khí",
        "icon": "cloud-rain",
        "description": "Thu thập dữ liệu trạm khí tượng: Nhiệt độ, Độ ẩm không khí, Tốc độ gió và Chỉ số ô nhiễm không khí.",
        "tables": ["weather_stations", "sensor_readings", "air_quality_indices", "weather_alerts"],
        "seed_data": {
            "sensor_readings": [{"id": 1, "station_id": 1, "temp_c": 31.5, "humidity_pct": 68, "aqi": 45}],
        },
    },
    "vehicle_gps_fleet": {
        "id": 93,
        "category": "iot",
        "name": "Giám Sát Vị Trí Xe Cơ Giới GPS",
        "icon": "navigation",
        "description": "Định vị phương tiện thời gian thực: Tọa độ kinh độ/vĩ độ, Vận tốc xe chạy và Cảnh báo vượt quá tốc độ.",
        "tables": ["vehicles", "gps_pings", "geofences", "speed_alerts"],
        "seed_data": {
            "gps_pings": [{"id": 1, "vehicle_id": 1, "latitude": 10.7769, "longitude": 106.7009, "speed_kmh": 45}],
        },
    },
    "smart_utility_metering": {
        "id": 94,
        "category": "iot",
        "name": "Công Tơ Điện Nước Tự Động Ghi Số",
        "icon": "zap",
        "description": "Đo đếm điện nước từ xa: Ghi chỉ số tiêu thụ tự động hàng giờ, Tính tiền theo bậc thang và Cảnh báo rò rỉ.",
        "tables": ["utility_meters", "hourly_readings", "monthly_bills", "tariff_rates"],
        "seed_data": {
            "utility_meters": [{"id": 1, "meter_code": "DONG-HO-DIEN-99", "current_kwh": 482.5, "customer_id": 1}],
        },
    },
    "real_estate_portal": {
        "id": 95,
        "category": "iot",
        "name": "Sàn Đăng Tin Bất Động Sản & Nhà Đất",
        "icon": "home",
        "description": "Cổng thông tin mua bán/cho thuê nhà đất: Lọc theo diện tích/khoảng giá và Đặt lịch hẹn xem nhà thực tế.",
        "tables": ["listings", "property_agents", "viewing_appointments", "property_photos"],
        "seed_data": {
            "listings": [{"id": 1, "title": "Căn Hộ Cao Cấp 2 Phòng Ngủ", "price": 4200000000, "area_sqm": 78}],
        },
    },
    "property_management_pms": {
        "id": 96,
        "category": "iot",
        "name": "Ban Quản Lý Tòa Nhà & Thu Phí Dịch Vụ",
        "icon": "grid",
        "description": "Quản lý tòa nhà chung cư: Danh sách căn hộ cư dân, Thu phí quản lý dịch vụ hàng tháng và Bảng tin thông báo.",
        "tables": ["apartments", "residents", "monthly_fees", "building_announcements"],
        "seed_data": {
            "apartments": [{"id": 1, "unit_number": "A12-05", "owner_name": "Đặng Văn H", "balance_due": 1200000}],
        },
    },
    "facility_maintenance_order": {
        "id": 97,
        "category": "iot",
        "name": "Phiếu Báo Hỏng & Bảo Trì Thiết Bị",
        "icon": "tool",
        "description": "Quản lý bảo trì tòa nhà/nhà xưởng: Tiếp nhận báo hỏng, Phân công thợ kỹ thuật và Nghiệm thu hoàn thành.",
        "tables": ["work_orders", "technicians", "spare_parts", "maintenance_logs"],
        "seed_data": {
            "work_orders": [{"id": 1, "issue": "Thang máy số 2 phát ra tiếng kêu", "priority": "CAO", "status": "DANG_SUA"}],
        },
    },
    "coworking_desk_booking": {
        "id": 98,
        "category": "iot",
        "name": "Đặt Chỗ Ngồi Làm Việc & Phòng Họp",
        "icon": "monitor",
        "description": "Văn phòng chia sẻ: Đặt bàn làm việc linh hoạt theo giờ, Phòng họp thuyết trình và Gói đồ uống đi kèm.",
        "tables": ["desks", "meeting_rooms", "coworking_bookings", "memberships"],
        "seed_data": {
            "desks": [{"id": 1, "desk_name": "Bàn Làm Việc A-12", "hourly_price": 25000, "is_booked": 0}],
        },
    },
    "security_access_control": {
        "id": 99,
        "category": "iot",
        "name": "Kiểm Soát Ra Vào & Thẻ Từ Cửa Thông Minh",
        "icon": "lock",
        "description": "Hệ thống an ninh ra vào: Quẹt thẻ từ/nhận diện khuôn mặt, Phân quyền theo tầng và Cảnh báo xâm nhập trái phép.",
        "tables": ["access_doors", "rfid_cards", "access_logs", "security_alerts"],
        "seed_data": {
            "access_logs": [{"id": 1, "door_name": "Cửa Phòng Máy Chủ", "card_id": "THE-NFC-9988", "access_granted": 1}],
        },
    },
    "smart_street_lighting": {
        "id": 100,
        "category": "iot",
        "name": "Lưới Đèn Chiếu Sáng Đô Thị Thông Minh",
        "icon": "sun",
        "description": "Hệ thống đèn đường đô thị: Tự động điều chỉnh độ sáng theo khung giờ và Cảnh báo sự cố bóng đèn cháy.",
        "tables": ["light_poles", "grid_sectors", "dimming_schedules", "fault_alarms"],
        "seed_data": {
            "light_poles": [{"id": 1, "pole_id": "COT-DEN-Q1-105", "brightness_pct": 70, "power_watts": 120, "is_working": 1}],
        },
    },
}


CUSTOM_BLUEPRINT_CATALOG: dict = {}


def list_all_blueprints() -> list[dict]:
    """Trả về danh sách 100 blueprint mẫu cùng các blueprint tùy chỉnh."""
    result = []
    for key, bp in BLUEPRINT_CATALOG.items():
        item = bp.copy()
        item["key"] = key
        result.append(item)
    for key, bp in CUSTOM_BLUEPRINT_CATALOG.items():
        item = bp.copy()
        item["key"] = key
        result.append(item)
    return result


def get_blueprint(key_or_id: str | int) -> dict | None:
    """Lấy blueprint theo key hoặc ID."""
    all_dicts = (BLUEPRINT_CATALOG, CUSTOM_BLUEPRINT_CATALOG)
    if isinstance(key_or_id, int):
        for d in all_dicts:
            for key, bp in d.items():
                if bp["id"] == key_or_id:
                    item = bp.copy()
                    item["key"] = key
                    return item
        return None

    str_key = str(key_or_id).lower()
    for d in all_dicts:
        if str_key in d:
            item = d[str_key].copy()
            item["key"] = str_key
            return item
    return None


def register_custom_blueprint(bp_data: dict) -> dict:
    """Đăng ký thêm một bản thiết kế kiến trúc tùy chỉnh không giới hạn vào danh mục."""
    total_count = len(BLUEPRINT_CATALOG) + len(CUSTOM_BLUEPRINT_CATALOG)
    new_id = total_count + 1
    key = bp_data.get("key") or f"custom_{new_id}"
    bp_record = {
        "id": new_id,
        "category": bp_data.get("category", "custom"),
        "name": bp_data.get("name", f"Kiến Trúc Tùy Chỉnh #{new_id}"),
        "icon": bp_data.get("icon", "layers"),
        "description": bp_data.get("description", "Hệ thống kiến trúc tùy chỉnh được tạo động qua BFA Studio."),
        "tables": bp_data.get("tables", ["users", "records"]),
        "seed_data": bp_data.get("seed_data", {}),
    }
    CUSTOM_BLUEPRINT_CATALOG[key] = bp_record
    item = bp_record.copy()
    item["key"] = key
    return item


def clear_custom_blueprints() -> None:
    """Xóa danh sách blueprint tùy chỉnh."""
    CUSTOM_BLUEPRINT_CATALOG.clear()
