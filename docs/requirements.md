# TÀI LIỆU YÊU CẦU HỆ THỐNG (REQUIREMENTS)

## 1. Phân tích bài toán quản lý
**Bối cảnh:**
Căng tin trường học phục vụ một lượng lớn học sinh, sinh viên và giảng viên mỗi ngày. Việc quản lý thông tin các món ăn, nhà cung cấp, và nhập xuất nguyên liệu thường được ghi chép thủ công trên sổ sách hoặc Excel, dẫn đến các rủi ro:
- Dễ sai sót, thất thoát nguyên liệu.
- Khó kiểm soát tồn kho, đôi khi hết nguyên liệu mà không kịp nhập.
- Không nắm bắt được nhu cầu thực tế, không biết món nào bán chạy, món nào ế.
- Bỏ qua các ý kiến phản hồi của thực khách.

**Vấn đề cần giải quyết:**
- Số hóa quy trình quản lý món ăn, nguyên liệu, nhà cung cấp, bán hàng và phản hồi.
- Ứng dụng AI để tối ưu hóa việc phân tích và ra quyết định, hỗ trợ gợi ý thực đơn và tổng hợp thông tin nhanh chóng.

## 2. Xác định yêu cầu chức năng (Functional Requirements)
Hệ thống cần cung cấp các chức năng quản lý cốt lõi:
1. **Quản lý phân quyền**: Đăng nhập hệ thống (Admin, Staff).
2. **Quản lý món ăn**: Thêm, sửa, xóa, tìm kiếm món ăn. Đầu vào: Tên món, loại, giá. Đầu ra: Danh sách món ăn.
3. **Quản lý nguyên liệu & Nhà cung cấp**: Thêm, sửa, xóa, theo dõi tồn kho. Đầu vào: Tên nguyên liệu, số lượng, định mức tối thiểu. Đầu ra: Cảnh báo nguyên liệu sắp hết.
4. **Quản lý bán hàng (POS)**: Tạo đơn hàng, tự động trừ số lượng món ăn và nguyên liệu (nếu có logic định lượng). Đầu vào: Món ăn, số lượng. Đầu ra: Hóa đơn, doanh thu cập nhật.
5. **Quản lý phản hồi**: Ghi nhận đánh giá của người dùng về món ăn. Đầu vào: Điểm đánh giá (1-5 sao), bình luận.
6. **Báo cáo & Thống kê**: Xem báo cáo doanh thu theo ngày, món bán chạy.

## 3. Xác định yêu cầu phi chức năng (Non-Functional Requirements)
- **Hiệu năng**: Hệ thống phải phản hồi nhanh (dưới 2 giây cho mỗi thao tác CRUD). Các truy vấn AI có thể mất thời gian hơn nhưng cần có cơ chế hiển thị loading/cảnh báo.
- **Bảo mật**: Mật khẩu cần được bảo mật, API key của AI không được lưu trữ cứng trong code mà phải dùng file `.env`. Phân quyền rõ ràng giữa Admin và Staff.
- **Khả dụng**: Giao diện trực quan, tương thích hiển thị tốt trên máy tính và máy tính bảng (Responsive cơ bản).
- **Tính ổn định**: Hệ thống bắt lỗi (try-catch) khi gọi AI thất bại (timeout, rate limit) để không làm crash hệ thống chính.

## 4. Xác định vị trí ứng dụng AI
Chức năng AI không tách rời mà gắn trực tiếp vào các dữ liệu hiện có trong hệ thống:
1. **AI Gợi ý thực đơn**: Dựa trên số lượng nguyên liệu tồn kho (ưu tiên nguyên liệu sắp hết hạn/còn nhiều) và dữ liệu các món bán chạy để gợi ý thực đơn ngày mai (Tại màn hình `AI Recommend`).
2. **AI Tóm tắt phản hồi**: Sử dụng AI phân tích cảm xúc (Sentiment Analysis) từ danh sách bình luận của học sinh, rút ra các điểm cần khắc phục và món nào bị chê nhiều nhất (Tại màn hình `AI Feedback`).
3. **AI Phân tích doanh thu**: Đọc dữ liệu thống kê tuần/tháng, chỉ ra xu hướng tăng giảm và đưa ra lời khuyên kinh doanh (Tại màn hình `AI Report`).
