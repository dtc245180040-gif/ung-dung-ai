# AI DATA ACCESS AND ACCESS CONTROL

## 1. Mục đích

Hệ thống Smart School Canteen Management System sử dụng dữ liệu
từ cơ sở dữ liệu nội bộ để cung cấp thông tin cho các chức năng AI.

AI không tự truy cập trực tiếp vào toàn bộ cơ sở dữ liệu.
Ứng dụng Flask truy vấn những dữ liệu cần thiết và truyền dữ liệu
đã được xử lý vào prompt.

---

## 2. Các nguồn dữ liệu AI sử dụng

### AI đề xuất thực đơn

AI sử dụng:

- Dữ liệu món ăn.
- Dữ liệu nguyên liệu.
- Dữ liệu bán hàng.

Mục đích:

- Phân tích món ăn.
- Phân tích doanh số.
- Kiểm tra tình trạng nguyên liệu.
- Đề xuất thực đơn.

### AI phân tích phản hồi

AI sử dụng:

- Tên món ăn.
- Điểm đánh giá.
- Nội dung phản hồi.
- Thời gian phản hồi.

Mục đích:

- Phân tích mức độ hài lòng.
- Tìm vấn đề thường gặp.
- Đề xuất hướng cải thiện.

### AI phân tích báo cáo

AI sử dụng:

- Tổng doanh thu.
- Tổng số lượng bán.
- Tổng số giao dịch.
- Món bán chạy.
- Doanh thu theo ngày.

Mục đích:

- Phân tích hoạt động kinh doanh.
- Xác định món bán chạy.
- Phân tích xu hướng doanh thu.
- Đề xuất cải thiện.

---

## 3. Quy trình truy cập dữ liệu

Quy trình xử lý:

Database
    ↓
Flask Backend
    ↓
SQL Query
    ↓
Dữ liệu cần thiết
    ↓
Prompt AI
    ↓
Gemini API
    ↓
Kết quả AI
    ↓
Giao diện hệ thống

AI chỉ nhận dữ liệu cần thiết cho từng chức năng.

---

## 4. Phân quyền người dùng

Hệ thống có cơ chế đăng nhập và kiểm tra quyền truy cập.

Các nhóm quyền:

### Admin

Có quyền quản lý và xem các chức năng quản trị,
bao gồm các chức năng AI.

### Staff

Có quyền sử dụng các chức năng nghiệp vụ
được hệ thống cho phép.

Người dùng chưa đăng nhập không được truy cập
các trang yêu cầu đăng nhập.

---

## 5. Kiểm soát truy cập

Các route quan trọng được bảo vệ bằng cơ chế:

- login_required
- admin_required

Backend kiểm tra quyền trước khi cho phép truy cập
các chức năng tương ứng.

Việc kiểm tra quyền được thực hiện ở phía server,
không chỉ dựa vào giao diện người dùng.

---

## 6. Nguyên tắc bảo vệ dữ liệu

Hệ thống áp dụng các nguyên tắc:

1. Chỉ lấy dữ liệu cần thiết cho từng chức năng AI.
2. Không gửi toàn bộ database cho AI.
3. API Key được lưu trong file `.env`.
4. File `.env` được thêm vào `.gitignore`.
5. AI không được phép tự thay đổi dữ liệu database.
6. Kết quả AI chỉ có chức năng hỗ trợ phân tích và ra quyết định.
7. Người quản lý là người quyết định cuối cùng.

---

## 7. Kiểm thử phân quyền

| Trường hợp | Kết quả mong đợi |
|------------|------------------|
| Chưa đăng nhập truy cập chức năng AI | Bị yêu cầu đăng nhập |
| Đăng nhập Admin | Có thể sử dụng chức năng được cấp |
| Đăng nhập Staff | Chỉ sử dụng chức năng được cấp |
| Truy cập URL quản trị trái phép | Bị từ chối |
| AI yêu cầu thay đổi database | Không thực hiện |

---

## 8. Kết luận

AI được tích hợp với dữ liệu nghiệp vụ thực tế của hệ thống
thông qua Flask Backend và Database.

Dữ liệu được kiểm soát trước khi gửi đến Gemini API.
Các chức năng được bảo vệ bằng cơ chế xác thực và phân quyền.

AI đóng vai trò hỗ trợ phân tích và đề xuất,
không tự ý thay đổi dữ liệu hệ thống.