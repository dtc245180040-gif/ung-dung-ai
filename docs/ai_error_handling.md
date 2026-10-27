# XỬ LÝ LỖI AI

## 1. Mục tiêu

Hệ thống phải đảm bảo chức năng AI không làm dừng toàn bộ
hệ thống khi xảy ra lỗi trong quá trình gọi Gemini API.

Các lỗi được xử lý:

- Timeout.
- Rate limit.
- API lỗi.
- API Key không hợp lệ hoặc chưa cấu hình.
- Kết quả AI rỗng.
- Dữ liệu gửi đến AI quá dài.

---

## 2. Timeout

Khi Gemini API phản hồi quá lâu hoặc kết nối bị gián đoạn,
hệ thống bắt lỗi và hiển thị thông báo phù hợp.

Thông báo:

"AI phản hồi quá lâu. Vui lòng thử lại."

Hệ thống vẫn tiếp tục hoạt động bình thường.

---

## 3. Rate Limit

Khi API đạt giới hạn số lượng request,
hệ thống không làm dừng ứng dụng.

Thông báo:

"AI đang được sử dụng quá nhiều. Vui lòng thử lại sau."

---

## 4. Kết quả AI rỗng

Nếu API không trả về nội dung,
hệ thống kiểm tra kết quả trước khi hiển thị.

Nếu kết quả rỗng:

"AI không trả về kết quả. Vui lòng thử lại."

---

## 5. Dữ liệu quá dài

Trước khi gửi dữ liệu đến Gemini,
hệ thống giới hạn lượng dữ liệu đưa vào prompt.

Mục đích:

- Giảm kích thước request.
- Tránh vượt giới hạn của model.
- Giảm thời gian xử lý.
- Giảm chi phí API.

---

## 6. Lỗi API

Các lỗi phát sinh trong quá trình gọi Gemini
được bắt bằng cơ chế xử lý exception.

Hệ thống hiển thị thông báo lỗi thay vì làm ứng dụng bị dừng.

---

## 7. Thiếu API Key

API Key được đọc từ biến môi trường:

GEMINI_API_KEY

Nếu chưa cấu hình API Key,
hệ thống thông báo AI chưa được cấu hình.

API Key không được hiển thị trên giao diện.

---

## 8. Nguyên tắc xử lý lỗi

Khi AI gặp lỗi:

1. Không làm dừng toàn bộ hệ thống.
2. Hiển thị thông báo dễ hiểu cho người dùng.
3. Không hiển thị API Key.
4. Không tự tạo dữ liệu giả để thay thế dữ liệu thật.
5. Cho phép người dùng thử lại.

---

## 9. Kiểm thử

| Trường hợp | Kết quả mong đợi |
|------------|------------------|
| Gemini hoạt động bình thường | Hiển thị kết quả AI |
| Timeout | Hiển thị cảnh báo timeout |
| Rate limit | Hiển thị cảnh báo giới hạn request |
| AI trả về rỗng | Hiển thị cảnh báo kết quả rỗng |
| Dữ liệu quá dài | Giới hạn dữ liệu trước khi gửi |
| API lỗi | Hiển thị thông báo lỗi |
| Không có API Key | Thông báo AI chưa cấu hình |

---

## 10. Kết luận

Hệ thống có cơ chế xử lý lỗi khi giao tiếp với Gemini API.

Mục tiêu là đảm bảo lỗi của AI không làm ảnh hưởng
đến các chức năng quản lý căng tin khác.