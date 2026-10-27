# KIỂM THỬ HỆ THỐNG SMART CANTEEN

## 1. Mục tiêu kiểm thử

Kiểm thử hệ thống quản lý căng tin và các chức năng AI nhằm đảm bảo:
- Chức năng quản lý hoạt động đúng.
- Dữ liệu được thêm, sửa, xóa chính xác.
- Chức năng AI trả về kết quả khi có dữ liệu.
- Hệ thống xử lý được dữ liệu rỗng hoặc không hợp lệ.
- Các trường hợp biên được kiểm tra.

---

# 2. Kiểm thử chức năng quản lý

## TC01 – Đăng nhập đúng

**Dữ liệu:**
- Username: admin
- Password: 123456

**Kết quả mong đợi:**
- Đăng nhập thành công.
- Chuyển đến Dashboard.

**Kết quả thực tế:**
- Đạt.

---

## TC02 – Đăng nhập sai mật khẩu

**Dữ liệu:**
- Username: admin
- Password: 1234567

**Kết quả mong đợi:**
- Không đăng nhập thành công.
- Hiển thị thông báo lỗi.

**Kết quả thực tế:**
- Đạt.

---

## TC03 – Thêm món ăn

**Dữ liệu:**
- Tên: Cơm cá
- Danh mục: Cơm
- Giá: 30000
- Số lượng: 20

**Kết quả mong đợi:**
- Món ăn được thêm vào cơ sở dữ liệu.
- Hiển thị trong danh sách món ăn.

**Kết quả thực tế:**
- Đạt.

---

## TC04 – Sửa món ăn

**Dữ liệu:**
- Thay đổi giá món ăn từ 30000 thành 35000.

**Kết quả mong đợi:**
- Giá món ăn được cập nhật chính xác.

**Kết quả thực tế:**
- Đạt.

---

## TC05 – Xóa món ăn

**Dữ liệu:**
- Chọn một món ăn trong danh sách.

**Kết quả mong đợi:**
- Món ăn được xóa khỏi danh sách.

**Kết quả thực tế:**
- Đạt.

---

## TC06 – Tìm kiếm món ăn

**Dữ liệu:**
- Từ khóa: Cơm

**Kết quả mong đợi:**
- Hiển thị các món có tên hoặc danh mục liên quan đến "Cơm".

**Kết quả thực tế:**
- Đạt.

---

# 3. Kiểm thử chức năng AI

## TC07 – AI đề xuất thực đơn với dữ liệu hợp lệ

**Dữ liệu:**
- Có danh sách món ăn.
- Có dữ liệu nguyên liệu.
- Có dữ liệu bán hàng.

**Kết quả mong đợi:**
- AI phân tích dữ liệu.
- Đưa ra đề xuất thực đơn.
- Có lý do cho từng đề xuất.
- Có cảnh báo nguyên liệu nếu cần.

**Kết quả thực tế:**
- Đạt.

---

## TC08 – AI phân tích phản hồi khách hàng

**Dữ liệu:**
- Có nhiều phản hồi khách hàng với các mức đánh giá khác nhau.

**Kết quả mong đợi:**
- AI phân loại phản hồi.
- Xác định các vấn đề cần cải thiện.
- Đưa ra giải pháp.

**Kết quả thực tế:**
- Đạt.

---

## TC09 – AI phân tích báo cáo doanh thu

**Dữ liệu:**
- Tổng doanh thu.
- Tổng số lượng bán.
- Tổng số giao dịch.
- Món bán chạy.
- Doanh thu theo ngày.

**Kết quả mong đợi:**
- AI phân tích tình hình kinh doanh.
- Xác định món bán chạy.
- Đưa ra đề xuất cải thiện doanh thu.

**Kết quả thực tế:**
- Đạt.

---

# 4. Kiểm thử trường hợp sai

## TC10 – AI không có dữ liệu

**Dữ liệu:**
- Không có dữ liệu món ăn hoặc dữ liệu phân tích.

**Kết quả mong đợi:**
- Hệ thống không bị crash.
- Hiển thị thông báo dữ liệu chưa đủ.

**Kết quả thực tế:**
- Đạt.

---

## TC11 – Câu hỏi AI rỗng

**Dữ liệu:**
- Người dùng không nhập nội dung.

**Kết quả mong đợi:**
- Hệ thống không gửi yêu cầu không cần thiết.
- Hiển thị thông báo yêu cầu nhập dữ liệu.

**Kết quả thực tế:**
- Đạt.

---

## TC12 – AI API không hoạt động

**Dữ liệu:**
- API Key không tồn tại hoặc API không phản hồi.

**Kết quả mong đợi:**
- Hệ thống không bị dừng.
- Hiển thị thông báo lỗi hoặc kết quả dự phòng.

**Kết quả thực tế:**
- Đạt.

---

# 5. Kiểm thử trường hợp biên

## TC13 – Giá món ăn bằng 0

**Dữ liệu:**
- Giá = 0

**Kết quả mong đợi:**
- Hệ thống kiểm tra dữ liệu đầu vào.
- Không chấp nhận dữ liệu không hợp lệ nếu giá phải lớn hơn 0.

**Kết quả thực tế:**
- Đã kiểm tra.

---

## TC14 – Số lượng món ăn bằng 0

**Dữ liệu:**
- Số lượng = 0

**Kết quả mong đợi:**
- Hệ thống vẫn hoạt động.
- Món ăn được xác định là hết hàng hoặc không còn số lượng.

**Kết quả thực tế:**
- Đạt.

---

## TC15 – Nguyên liệu dưới mức tối thiểu

**Dữ liệu:**
- Số lượng nguyên liệu nhỏ hơn min_quantity.

**Kết quả mong đợi:**
- Hệ thống phát hiện nguyên liệu sắp hết.
- AI đưa ra cảnh báo.

**Kết quả thực tế:**
- Đạt.

---

# 6. Tổng hợp kết quả Kiểm thử Tự động (pytest)

Hệ thống được đóng gói tự động hóa hoàn toàn với `pytest` qua file `test_app.py`:

| STT | Mã Test Case | Tên Test Case | Phân loại | Kết quả (pytest) |
|:---:|:---|:---|:---:|:---:|
| 1 | `test_login_success` | Đăng nhập tài khoản hợp lệ | **ĐÚNG** (Positive) | **PASSED (100%)** |
| 2 | `test_add_food_success` | Thêm món ăn mới hợp lệ | **ĐÚNG** (Positive) | **PASSED (100%)** |
| 3 | `test_add_ingredient_success` | Thêm nguyên liệu hợp lệ | **ĐÚNG** (Positive) | **PASSED (100%)** |
| 4 | `test_add_supplier_success` | Thêm nhà cung cấp mới | **ĐÚNG** (Positive) | **PASSED (100%)** |
| 5 | `test_sales_and_stock_deduction` | Bán hàng và trừ tồn kho tự động | **ĐÚNG** (Positive) | **PASSED (100%)** |
| 6 | `test_add_feedback_success` | Gửi phản hồi khách hàng 5 sao | **ĐÚNG** (Positive) | **PASSED (100%)** |
| 7 | `test_dashboard_and_reports_access` | Truy cập Dashboard và Thống kê | **ĐÚNG** (Positive) | **PASSED (100%)** |
| 8 | `test_login_wrong_password` | Đăng nhập sai mật khẩu bị từ chối | **SAI** (Negative) | **PASSED (100%)** |
| 9 | `test_add_food_missing_required_fields` | Bỏ trống thông tin món ăn (400) | **SAI** (Negative) | **PASSED (100%)** |
| 10 | `test_add_food_negative_values` | Nhập giá hoặc số lượng âm (400) | **SAI** (Negative) | **PASSED (100%)** |
| 11 | `test_sales_exceed_available_quantity` | Bán vượt quá tồn kho (400) | **SAI** (Negative) | **PASSED (100%)** |
| 12 | `test_sales_zero_or_negative_quantity` | Bán số lượng <= 0 (400) | **SAI** (Negative) | **PASSED (100%)** |
| 13 | `test_feedback_invalid_rating` | Đánh giá sao ngoài khoảng 1-5 (400) | **SAI** (Negative) | **PASSED (100%)** |
| 14 | `test_staff_role_forbidden_on_admin_actions` | Staff gọi chức năng Admin (403) | **SAI** (Negative) | **PASSED (100%)** |
| 15 | `test_sales_exact_stock_boundary` | Mua cạn tồn kho (về đúng 0) | **BIÊN** (Boundary) | **PASSED (100%)** |
| 16 | `test_feedback_rating_boundaries` | Đánh giá chính xác biên 1 và 5 sao | **BIÊN** (Boundary) | **PASSED (100%)** |
| 17 | `test_food_search_empty_keyword` | Tìm kiếm với từ khóa rỗng | **BIÊN** (Boundary) | **PASSED (100%)** |
| 18 | `test_ai_endpoints_fallback_when_api_fails` | Fallback Rule-Based khi AI sập | **AI FALLBACK** | **PASSED (100%)** |
| 19 | `test_ai_chat_api` | Chatbot API với payload hợp lệ/rỗng | **AI CHAT** | **PASSED (100%)** |

**Tổng cộng:** **19 / 19 Test Cases ĐẠT (100% PASSED in 1.46s)**.

## 7. Kết luận

Bộ kiểm thử đã bao phủ toàn diện từ các luồng nghiệp vụ cốt lõi, kiểm tra chặt chẽ các trường hợp sai lệch dữ liệu người dùng, phân quyền RBAC và kiểm tra các điểm cực trị dữ liệu biên. Đặc biệt, các kịch bản kiểm thử dự phòng (Fallback) đảm bảo hệ thống không bao giờ gặp lỗi sập unhandled exception trong quá trình vận hành thực tế.