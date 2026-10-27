# AI CODE REVIEW – SMART CANTEEN

## 1. Mục tiêu

Sử dụng AI để hỗ trợ kiểm tra mã nguồn của hệ thống Smart Canteen,
phát hiện các vấn đề về:
- Chất lượng code.
- Bảo mật.
- Xử lý lỗi.
- Quản lý API Key.
- Trùng lặp code.
- Khả năng bảo trì.

Sau khi AI đưa ra nhận xét, nhóm kiểm tra và áp dụng các thay đổi phù hợp.

---

# 2. Phạm vi Review

Các thành phần được kiểm tra:

- app.py
- Các module prompts
- Các chức năng kết nối Gemini API.
- Chức năng truy vấn SQLite.
- Chức năng xử lý dữ liệu AI.
- Các route quản lý hệ thống.

---

# 3. Prompt sử dụng để Review Code

## System Prompt

Bạn là chuyên gia Code Review cho ứng dụng Flask.

Hãy kiểm tra mã nguồn được cung cấp và tập trung vào:

1. Lỗi logic.
2. Lỗi xử lý ngoại lệ.
3. Vấn đề bảo mật.
4. Bảo vệ API Key.
5. SQL Injection.
6. Kiểm tra dữ liệu đầu vào.
7. Code trùng lặp.
8. Khả năng bảo trì.
9. Khả năng cải thiện cấu trúc code.

Không tự ý thay đổi chức năng nghiệp vụ.

Hãy đưa ra:
- Vấn đề phát hiện.
- Mức độ ảnh hưởng.
- Nguyên nhân.
- Cách cải thiện.
- Đoạn code đề xuất nếu cần.

## User Prompt

Hãy review mã nguồn Smart Canteen được cung cấp.

Tập trung đặc biệt vào:
- Gemini API.
- Flask route.
- SQLite.
- API Key.
- Input từ người dùng.
- Exception handling.

Sau khi review, hãy đề xuất các thay đổi có thể áp dụng
mà không làm thay đổi chức năng chính của hệ thống.

---

# 4. Kết quả Review

## Vấn đề 1 – API Key

### Phát hiện

API Key không nên được viết trực tiếp trong mã nguồn.

### Cách xử lý

Sử dụng file `.env`:

GEMINI_API_KEY=your_api_key

Trong Python sử dụng:

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

### Kết quả

API Key được tách khỏi mã nguồn.

---

# 5. Vấn đề 2 – File .env

### Phát hiện

File `.env` có thể chứa thông tin bí mật.

### Cách xử lý

Thêm `.env` vào `.gitignore`.

Ví dụ:

.env
__pycache__/
venv/

### Kết quả

Hạn chế việc đưa API Key lên GitHub.

---

# 6. Vấn đề 3 – Xử lý Exception

### Phát hiện

Các chức năng gọi AI có thể phát sinh lỗi khi:
- API không hoạt động.
- API Key không hợp lệ.
- Kết nối mạng lỗi.
- Model trả về kết quả rỗng.

### Cách xử lý

Sử dụng try/except để hệ thống không bị dừng khi AI gặp lỗi.

Ví dụ:

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    if response and response.text:
        ai_text = response.text
    else:
        ai_text = "AI không trả về kết quả."

except Exception as e:
    ai_text = "Không thể kết nối với AI. Vui lòng thử lại."

### Kết quả

Hệ thống có thông báo khi chức năng AI gặp lỗi.

---

# 7. Vấn đề 4 – Kiểm tra dữ liệu đầu vào

### Phát hiện

Dữ liệu do người dùng nhập cần được kiểm tra trước khi xử lý.

### Cách xử lý

Kiểm tra dữ liệu rỗng:

question = request.form.get("question", "").strip()

if not question:
    return render_template(
        "ai_recommend.html",
        error="Vui lòng nhập nội dung."
    )

### Kết quả

Hạn chế xử lý dữ liệu rỗng hoặc không hợp lệ.

---

# 8. Vấn đề 5 – SQL Injection

### Phát hiện

Các câu SQL nhận dữ liệu từ người dùng cần tránh nối chuỗi trực tiếp.

### Cách xử lý

Sử dụng parameterized query.

Ví dụ:

cursor.execute(
    "SELECT * FROM foods WHERE name LIKE ?",
    (f"%{keyword}%",)
)

### Kết quả

Giảm nguy cơ SQL Injection.

---

# 9. Vấn đề 6 – Code trùng lặp

### Phát hiện

Các chức năng AI có một số đoạn xử lý tương tự:
- Kiểm tra API Client.
- Gọi Gemini.
- Kiểm tra kết quả.
- Xử lý exception.

### Đề xuất

Có thể tách phần gọi Gemini thành một hàm dùng chung.

Ví dụ:

def call_gemini(system_prompt, user_prompt):
    if client is None:
        return None

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )

    if response and response.text:
        return response.text

    return None

### Kết quả

Giảm code trùng lặp và dễ bảo trì hơn.

---

# 10. Kết quả trước và sau Review

| Nội dung | Trước Review | Sau Review |
|---|---|---|
| API Key | Có nguy cơ viết trong code | Sử dụng `.env` |
| Exception | Xử lý cơ bản | Có fallback |
| Input | Chưa kiểm tra đầy đủ | Có kiểm tra dữ liệu |
| SQL | Truy vấn cần kiểm tra | Sử dụng parameterized query |
| Gemini | Code gọi tại nhiều route | Có thể dùng hàm chung |
| Bảo trì | Khó mở rộng | Cấu trúc rõ ràng hơn |

---

# 11. Kết luận

AI được sử dụng như một công cụ hỗ trợ Code Review.

Nhóm không áp dụng trực tiếp mọi đề xuất của AI mà kiểm tra lại
trước khi thay đổi mã nguồn.

Các nội dung được ưu tiên xử lý gồm:
- Bảo mật API Key.
- Xử lý lỗi.
- Kiểm tra dữ liệu đầu vào.
- SQL Injection.
- Giảm code trùng lặp.

Qua quá trình Review, mã nguồn được tổ chức rõ ràng hơn,
an toàn hơn và thuận tiện hơn cho việc bảo trì.