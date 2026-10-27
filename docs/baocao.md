# BÁO CÁO DỰ ÁN: HỆ THỐNG QUẢN LÝ CĂNG TIN TRƯỜNG HỌC TÍCH HỢP AI

## 1. Giới thiệu bài toán
Căng tin trường học truyền thống thường quản lý thủ công, dẫn đến các vấn đề như: thiếu nguyên liệu bất chợt, khó nắm bắt xu hướng tiêu dùng (món nào được ưa chuộng), và tốn thời gian thống kê doanh thu.
Dự án **Smart Canteen Management System** được xây dựng nhằm mục đích số hóa quy trình quản lý, đồng thời tích hợp AI (Trí tuệ nhân tạo) để tự động hóa các khâu ra quyết định, phân tích phản hồi và báo cáo, qua đó nâng cao hiệu quả hoạt động của căng tin.

## 2. Mục tiêu dự án
- Xây dựng hệ thống quản lý toàn diện (Món ăn, Nguyên liệu, Bán hàng, Phản hồi, Nhà cung cấp).
- Phân quyền rõ ràng giữa quản lý (Admin) và nhân viên bán hàng (Staff).
- Tích hợp AI (Google Gemini) để:
  1. Gợi ý thực đơn thông minh dựa trên nguyên liệu tồn kho và dữ liệu bán hàng.
  2. Tóm tắt phản hồi, đánh giá sự hài lòng của học sinh/sinh viên.
  3. Phân tích doanh thu và tự động sinh báo cáo kinh doanh định kỳ.

## 3. Kiến trúc và Công nghệ
- **Mô hình kiến trúc**: Server-Side Rendering (SSR) với Flask.
- **Backend**: Python 3.8+, Flask Framework.
- **Frontend**: HTML5, CSS3, Jinja2 template.
- **Cơ sở dữ liệu**: SQLite (sử dụng thư viện `sqlite3` tích hợp).
- **AI Engine**: Google Gemini API thông qua thư viện `google-generativeai`.

## 4. Quá trình phát triển SDLC với sự hỗ trợ của AI
Dự án đã ứng dụng AI trong suốt vòng đời phát triển phần mềm (SDLC):
- **Giai đoạn 1 (Thiết kế & Phân tích)**: Sử dụng AI để thiết kế schema cơ sở dữ liệu (các bảng `foods`, `ingredients`, `sales`, `feedback`, `users`), xác định luồng hoạt động chính và thiết kế các module chức năng.
- **Giai đoạn 2 (Phát triển CRUD)**: Sử dụng AI để sinh mã nguồn chuẩn cho các chức năng Thêm/Sửa/Xóa, thiết lập quan hệ trừ tồn kho khi phát sinh giao dịch bán hàng, và fix lỗi liên quan đến logic trừ nguyên liệu.
- **Giai đoạn 3 (Tích hợp AI Prompting)**: Dùng AI để tối ưu hóa các prompt (lời nhắc) dùng trong hệ thống (gợi ý thực đơn, tóm tắt phản hồi). Kiểm thử các prompt với dữ liệu thiếu để đánh giá độ ổn định.
- **Giai đoạn 4 (Triển khai & Tài liệu)**: Sử dụng AI để hoàn thiện `README.md`, sinh báo cáo dự án và tạo cấu trúc slide thuyết trình, đồng thời hướng dẫn cài đặt cấu hình `.env` cho API key.

## 5. Kết quả đạt được
- Hệ thống chạy ổn định, đáp ứng được các nhu cầu cơ bản như ghi nhận đơn hàng, cập nhật kho tự động, tra cứu danh mục.
- Module AI hoạt động trơn tru:
  - Phân tích tốt các bình luận của sinh viên thành các ý chính (tích cực/tiêu cực).
  - Tự động cảnh báo nguyên liệu sắp hết và đề xuất thực đơn hợp lý (Ví dụ: Ưu tiên bán các món có nhiều nguyên liệu tồn).
  - Báo cáo sinh động, tóm lược được tình hình doanh thu theo ngày/tuần.

## 6. Hướng phát triển tương lai
- **Mở rộng CSDL**: Chuyển đổi từ SQLite sang PostgreSQL khi số lượng dữ liệu lớn.
- **Tách biệt Frontend/Backend**: Xây dựng Frontend riêng biệt bằng ReactJS/VueJS, backend chỉ cung cấp RESTful API hoặc GraphQL.
- **Dự báo nhu cầu (Forecasting)**: Triển khai các mô hình Machine Learning riêng biệt để dự đoán số lượng nguyên liệu cần nhập mỗi ngày một cách chính xác hơn, không chỉ phụ thuộc vào LLM.
