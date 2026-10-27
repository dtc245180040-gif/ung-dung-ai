# AI USER EXPERIENCE – SMART CANTEEN

## 1. Mục tiêu

Tích hợp AI trực tiếp vào quy trình quản lý căng tin,
giúp nhân viên không cần chuyển sang một ứng dụng AI khác
mà có thể sử dụng AI ngay trong hệ thống Smart Canteen.

AI được sử dụng để:
- Đề xuất thực đơn.
- Phân tích phản hồi khách hàng.
- Phân tích báo cáo doanh thu.
- Cảnh báo nguyên liệu sắp hết.

---

# 2. Luồng sử dụng AI

Quy trình hoạt động:

Quản lý dữ liệu
        ↓
Nhân viên mở chức năng AI
        ↓
Hệ thống lấy dữ liệu từ Database
        ↓
AI phân tích dữ liệu
        ↓
Hiển thị kết quả trên giao diện
        ↓
Nhân viên xem kết quả
        ↓
Nhân viên đưa ra quyết định quản lý

---

# 3. AI đề xuất thực đơn

## Người dùng

Nhân viên quản lý căng tin.

## Dữ liệu sử dụng

- Danh sách món ăn.
- Số lượng món ăn.
- Nguyên liệu.
- Mức tồn kho tối thiểu.
- Doanh số bán hàng.

## Quy trình

1. Nhân viên mở chức năng "AI đề xuất thực đơn".
2. Hệ thống lấy dữ liệu từ Database.
3. Dữ liệu được gửi đến AI.
4. AI phân tích dữ liệu.
5. Kết quả được hiển thị trên giao diện.
6. Nhân viên sử dụng đề xuất để tham khảo khi xây dựng thực đơn.

## Kết quả hiển thị

- Món ăn được đề xuất.
- Lý do đề xuất.
- Nguyên liệu cần chú ý.
- Cảnh báo.

---

# 4. AI phân tích phản hồi

## Người dùng

Nhân viên hoặc quản lý.

## Quy trình

1. Nhân viên mở chức năng phân tích phản hồi.
2. Hệ thống lấy dữ liệu feedback từ Database.
3. AI phân tích các đánh giá.
4. Hệ thống hiển thị kết quả.
5. Nhân viên xem các vấn đề cần cải thiện.

## Kết quả

AI cung cấp:
- Tổng quan mức độ hài lòng.
- Các món được đánh giá tốt.
- Các vấn đề cần cải thiện.
- Các chủ đề xuất hiện nhiều.
- Giải pháp đề xuất.

---

# 5. AI phân tích báo cáo

## Người dùng

Quản lý căng tin.

## Quy trình

1. Quản lý mở chức năng AI báo cáo.
2. Hệ thống lấy dữ liệu doanh thu.
3. AI phân tích dữ liệu.
4. Kết quả được hiển thị.
5. Quản lý sử dụng kết quả để tham khảo trong việc quản lý.

## Kết quả

AI phân tích:
- Tổng doanh thu.
- Số lượng bán.
- Món bán chạy.
- Xu hướng doanh thu.
- Đề xuất cải thiện.

---

# 6. Cảnh báo AI

AI có thể hỗ trợ phát hiện các vấn đề từ dữ liệu hệ thống.

Ví dụ:

Nguyên liệu:
- Thịt gà: 4 kg
- Mức tối thiểu: 10 kg

Hệ thống phát hiện:

"Cảnh báo: Thịt gà đang thấp hơn mức tồn kho tối thiểu."

Thông tin cảnh báo được hiển thị trực tiếp trên giao diện.

---

# 7. Thiết kế trải nghiệm người dùng

AI được tích hợp vào giao diện chính của hệ thống.

Người dùng có thể truy cập:

- AI đề xuất thực đơn
- AI phân tích phản hồi
- AI phân tích báo cáo

Người dùng không cần:
- Mở ứng dụng AI bên ngoài.
- Sao chép dữ liệu thủ công.
- Nhập lại toàn bộ dữ liệu từ Database.

---

# 8. Nguyên tắc sử dụng AI

AI đóng vai trò hỗ trợ người dùng.

AI:
- Phân tích dữ liệu.
- Đưa ra đề xuất.
- Đưa ra cảnh báo.

Người dùng:
- Kiểm tra kết quả.
- Đánh giá đề xuất.
- Quyết định hành động cuối cùng.

AI không tự động thay đổi dữ liệu trong Database.

---

# 9. Kết luận

AI được tích hợp trực tiếp vào quy trình quản lý Smart Canteen.

Việc tích hợp giúp người dùng có thể:
- Phân tích dữ liệu nhanh hơn.
- Nhận cảnh báo từ dữ liệu.
- Nhận đề xuất hỗ trợ quản lý.
- Sử dụng AI ngay trong hệ thống.

AI đóng vai trò là công cụ hỗ trợ ra quyết định,
không thay thế quyết định của người quản lý.