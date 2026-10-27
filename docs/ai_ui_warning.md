# GIAO DIỆN HIỂN THỊ KẾT QUẢ AI VÀ CẢNH BÁO

## 1. Hiển thị kết quả AI

Hệ thống hiển thị kết quả phân tích AI trực tiếp trên giao diện
của từng chức năng.

Các chức năng AI:

- AI đề xuất thực đơn.
- AI phân tích phản hồi khách hàng.
- AI phân tích báo cáo doanh thu.

Kết quả AI được hiển thị trong khu vực riêng,
giúp người dùng dễ dàng phân biệt nội dung do AI tạo ra
với dữ liệu quản lý thông thường.

---

## 2. Giao diện AI đề xuất thực đơn

Trang AI đề xuất thực đơn có khu vực:

"Phân tích từ Gemini AI"

Kết quả được hiển thị trong một khung riêng.

Ngoài kết quả AI, hệ thống còn hiển thị:

- Các món ăn được đề xuất.
- Giá món ăn.
- Số lượng đã bán.
- Nhận xét của AI.
- Tình trạng nguyên liệu.

---

## 3. Cảnh báo nguyên liệu

Hệ thống kiểm tra số lượng nguyên liệu với mức tối thiểu.

Nếu:

quantity <= min_quantity

hệ thống hiển thị trạng thái:

"⚠ Sắp hết"

Nếu số lượng nguyên liệu lớn hơn mức tối thiểu,
hệ thống hiển thị:

"✓ Đủ hàng"

Việc cảnh báo giúp người quản lý chú ý đến những nguyên liệu
có nguy cơ thiếu.

---

## 4. Cảnh báo khi AI không hoạt động

Nếu Gemini API không thể kết nối,
hệ thống không dừng toàn bộ chức năng.

Hệ thống hiển thị thông báo:

"Không thể kết nối AI."

Đồng thời hệ thống vẫn có thể hiển thị
dữ liệu và đề xuất dựa trên dữ liệu nội bộ.

---

## 5. Cảnh báo khi chưa cấu hình API Key

Nếu hệ thống chưa có GEMINI_API_KEY,
người dùng được thông báo rằng AI chưa được cấu hình.

Hệ thống không hiển thị API Key trên giao diện.

---

## 6. Nguyên tắc sử dụng kết quả AI

Kết quả AI có tính chất hỗ trợ.

Người quản lý cần kiểm tra lại thông tin
trước khi đưa ra quyết định thực tế.

AI không tự động thay đổi dữ liệu trong hệ thống.

---

## 7. Kiểm thử giao diện

| Trường hợp | Kết quả |
|------------|---------|
| AI trả về kết quả bình thường | Hiển thị kết quả AI |
| Có nguyên liệu dưới mức tối thiểu | Hiển thị cảnh báo "Sắp hết" |
| Không có dữ liệu món ăn | Hiển thị thông báo phù hợp |
| Gemini API lỗi | Hiển thị cảnh báo kết nối AI |
| Chưa cấu hình API Key | Hiển thị thông báo AI chưa được cấu hình |

---

## 8. Kết luận

Giao diện AI được tích hợp trực tiếp vào hệ thống quản lý căng tin.

Kết quả AI được hiển thị rõ ràng, đồng thời hệ thống có
các cảnh báo để người dùng nhận biết tình trạng dữ liệu
và lỗi kết nối AI.

AI chỉ đóng vai trò hỗ trợ và người quản lý vẫn là người
đưa ra quyết định cuối cùng.