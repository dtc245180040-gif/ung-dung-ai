# NHẬT KÝ TÍCH HỢP AI – HỆ THỐNG SMART CANTEEN

**Sinh viên thực hiện:** Đặng Thanh  
**Mã SV:** DTC245180040  
**Ngày cập nhật:** 19/09/2026  

---

## MỤC LỤC

1. [Nhật ký Prompt](#1-nhật-ký-prompt)
2. [Phản hồi AI (mẫu)](#2-phản-hồi-ai-mẫu)
3. [Phần code được AI hỗ trợ](#3-phần-code-được-ai-hỗ-trợ)
4. [Phần sinh viên đã kiểm tra và chỉnh sửa](#4-phần-sinh-viên-đã-kiểm-tra-và-chỉnh-sửa)

---

## 1. NHẬT KÝ PROMPT

Hệ thống tích hợp **4 chức năng AI** với prompt được tách riêng ra thư mục `prompts/`.

### 1.1. Prompt AI Đề xuất thực đơn (`prompts/recommend_prompt.py`)

**System Prompt:**

```text
Bạn là trợ lý AI quản lý căng tin trường học.

Nhiệm vụ:
- Phân tích dữ liệu món ăn.
- Phân tích số lượng nguyên liệu còn lại.
- Phân tích doanh số bán hàng.
- Đề xuất thực đơn phù hợp cho căng tin.

Quy tắc xử lý dữ liệu:
1. Chỉ sử dụng dữ liệu được cung cấp.
2. Không tự bịa số liệu hoặc món ăn.
3. Ưu tiên món có doanh số tốt.
4. Không ưu tiên món có nguyên liệu dưới mức tối thiểu.
5. Nếu dữ liệu không đủ, phải nói rõ.
6. Mỗi đề xuất phải có lý do ngắn gọn.
7. Phải cảnh báo nếu nguyên liệu có nguy cơ hết.
8. Không tự ý thay đổi dữ liệu trong cơ sở dữ liệu.
```

**User Prompt:**

```text
Hãy phân tích dữ liệu căng tin dưới đây.

DỮ LIỆU MÓN ĂN: {food_data}
DỮ LIỆU NGUYÊN LIỆU: {ingredient_data}
DỮ LIỆU BÁN HÀNG: {sales_data}

Hãy trả lời theo đúng cấu trúc:
1. THỰC ĐƠN ĐỀ XUẤT (Tên món + Lý do đề xuất)
2. NGUYÊN LIỆU CẦN CHÚ Ý (Tên + Tình trạng)
3. CẢNH BÁO (Các vấn đề phát hiện được)
4. KẾT LUẬN (Tóm tắt ngắn gọn)
```

**Biến context truyền vào:** `food_data`, `ingredient_data`, `sales_data` – lấy từ CSDL SQLite.

---

### 1.2. Prompt AI Tổng hợp phản hồi (`prompts/feedback_prompt.py`)

**System Prompt:**

```text
Bạn là AI trợ lý quản lý căng tin trường học.
Hãy phân tích các phản hồi của khách hàng.
Yêu cầu:
1. Đánh giá mức độ hài lòng chung.
2. Xác định món được đánh giá tốt.
3. Xác định vấn đề nhận nhiều phản hồi chưa tốt.
4. Tóm tắt ý kiến khách hàng thường nhắc đến.
5. Đề xuất 3 giải pháp cải thiện.
6. Đưa ra kết luận ngắn gọn.
Không tự bịa dữ liệu.
```

**Biến context:** `feedback_data` (tên món, số sao, nội dung phản hồi).

---

### 1.3. Prompt AI Báo cáo doanh thu (`prompts/report_prompt.py`)

**System Prompt:**

```text
Bạn là AI trợ lý phân tích doanh thu cho căng tin trường học.
Hãy tạo báo cáo doanh thu ngắn gọn bằng tiếng Việt.
Yêu cầu:
1. Nêu tổng doanh thu, tổng số lượng món, số giao dịch.
2. Xác định món bán chạy nhất.
3. Phân tích xu hướng doanh thu.
4. Đưa ra 3 đề xuất tăng doanh thu.
Không tự bịa dữ liệu.
```

**Biến context:** `total_revenue`, `total_quantity`, `total_orders`, `best_selling`, `daily_revenue`.

---

### 1.4. Prompt Chatbot Trợ lý (`prompts/chat_prompt.py`)

**System Prompt:**

```text
Bạn là Trợ lý AI quản lý căng tin trường học (Smart Canteen Assistant).
Nhiệm vụ: hỗ trợ Quản lý/Nhân viên trả lời câu hỏi về bán hàng, món ăn, tồn kho.

Thông tin hiện tại:
- Tổng số món ăn: {food_count}
- Tổng số nguyên liệu: {ingredient_count}
- Tổng doanh thu: {revenue} VNĐ
- Tổng số giao dịch: {sale_count}

Quy tắc:
1. Trả lời ngắn gọn, lịch sự, thân thiện.
2. KHÔNG tự bịa dữ liệu.
3. Không dùng bảng lớn.
4. Xưng "tôi", gọi người dùng "bạn/anh/chị".
```

**Biến context:** `food_count`, `ingredient_count`, `revenue`, `sale_count` – lấy realtime từ CSDL.

---

## 2. PHẢN HỒI AI (MẪU)

### 2.1. AI Đề xuất thực đơn – Phản hồi mẫu

**Câu hỏi gửi AI:** Prompt tự động kèm dữ liệu 6 món ăn + 5 nguyên liệu + bán hàng.

**Phản hồi AI:**

```
1. THỰC ĐƠN ĐỀ XUẤT
- Tên món: Cơm gà
  Lý do: Món đang bán với số lượng còn nhiều (50 suất), nguyên liệu "Thịt gà" (15 kg)
  và "Gạo" (50 kg) đều đạt và vượt mức tồn kho tối thiểu.

- Tên món: Phở bò
  Lý do: Món đang bán với số lượng còn lại tốt (40 suất), nguyên liệu "Thịt bò" (12 kg)
  vượt tồn kho tối thiểu (8 kg).

- Tên món: Trà sữa
  Lý do: Món đang bán với số lượng lớn nhất còn lại (60 phần).

2. NGUYÊN LIỆU CẦN CHÚ Ý
- Rau xanh: Còn 3 kg (Thấp hơn mức tối thiểu 8 kg) ⚠️

3. CẢNH BÁO
- Nguyên liệu "Rau xanh" đang ở mức rất thấp, cần nhập thêm trước khi hết.

4. KẾT LUẬN
- Nên ưu tiên bán Cơm gà, Phở bò, Trà sữa. Cần nhập bổ sung Rau xanh.
```

---

### 2.2. Chatbot Trợ lý – Phản hồi mẫu

**Câu hỏi:** "Hôm nay doanh thu thế nào?"

**Phản hồi AI:**

```
Chào bạn! Theo dữ liệu hiện tại, tổng doanh thu của căng tin là 1,250,000 VNĐ 
với 45 giao dịch. Bạn có thể xem chi tiết tại trang Báo cáo.
```

**Câu hỏi:** "Có nguyên liệu nào sắp hết không?"

**Phản hồi AI:**

```
Hiện tại tôi chỉ có thông tin tổng quan: hệ thống đang quản lý 5 loại nguyên liệu.
Để xem chi tiết nguyên liệu nào sắp hết, bạn nên kiểm tra tại trang Nguyên liệu 
hoặc Dashboard (mục "Nguyên liệu sắp hết"). Tôi không muốn đưa ra thông tin 
không chính xác.
```

---

### 2.3. AI Tổng hợp phản hồi – Phản hồi mẫu

**Câu hỏi gửi AI:** Prompt tự động kèm danh sách phản hồi khách hàng.

**Phản hồi AI:**

```
TỔNG HỢP PHẢN HỒI KHÁCH HÀNG

1. Đánh giá chung: Khách hàng nhìn chung hài lòng (trung bình 4.2/5 sao).
2. Món được khen: Cơm gà (nhiều phản hồi tích cực về hương vị).
3. Vấn đề cần cải thiện: Thời gian phục vụ (một số khách phản hồi phải chờ lâu).
4. Đề xuất:
   - Tăng nhân viên phục vụ giờ cao điểm.
   - Chuẩn bị sẵn các món bán chạy.
   - Thêm lựa chọn đồ uống.
```

---

## 3. PHẦN CODE ĐƯỢC AI HỖ TRỢ

### 3.1. Hàm `call_gemini()` – Retry & Fallback tự động

**Vị trí:** `app.py` (dòng 39-75)

```python
GEMINI_MODELS = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-3.6-flash"]

def call_gemini(contents, system_instruction=None, max_retries=3):
    """Gọi Gemini API với retry và fallback model tự động."""
    if not client:
        return None, "Chưa cấu hình GEMINI_API_KEY."
    
    from google.genai import types
    
    for model_name in GEMINI_MODELS:
        for attempt in range(max_retries):
            try:
                config = None
                if system_instruction:
                    config = types.GenerateContentConfig(
                        system_instruction=system_instruction
                    )
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config
                )
                return response.text, None  # Thành công
            except Exception as e:
                error_str = str(e)
                if "503" in error_str or "UNAVAILABLE" in error_str:
                    time.sleep(2 * (attempt + 1))  # Chờ rồi thử lại
                    continue
                elif "404" in error_str or "NOT_FOUND" in error_str:
                    break  # Model không tồn tại, chuyển model tiếp
                else:
                    return None, f"Lỗi Gemini: {error_str}"
    
    return None, "Không thể kết nối Gemini AI sau nhiều lần thử."
```

**Mục đích:** AI hỗ trợ thiết kế hàm này để xử lý 2 lỗi thường gặp:
- Lỗi 503 (server quá tải) → tự động thử lại tối đa 3 lần.
- Lỗi 404 (model không tồn tại) → tự chuyển sang model dự phòng.

---

### 3.2. API Endpoint `/api/chat` – Chatbot

**Vị trí:** `app.py` (dòng ~1440-1473)

```python
@app.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    data = request.get_json()
    user_message = data["message"].strip()

    conn = get_db()
    food_count = conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0]
    ingredient_count = conn.execute("SELECT COUNT(*) FROM ingredients").fetchone()[0]
    revenue = conn.execute("SELECT COALESCE(SUM(total), 0) FROM sales").fetchone()[0]
    sale_count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    conn.close()

    system_instruction = CHAT_SYSTEM_PROMPT.format(
        food_count=food_count, ingredient_count=ingredient_count,
        revenue="{:,.0f}".format(revenue), sale_count=sale_count
    )
    
    result, error = call_gemini(user_message, system_instruction=system_instruction)
    if result:
        return jsonify({"response": result})
    else:
        return jsonify({"response": f"Xin lỗi, {error}"})
```

**Mục đích:** Nhận câu hỏi từ giao diện Chat, lấy dữ liệu realtime từ CSDL, chèn vào system prompt, gọi Gemini và trả về JSON.

---

### 3.3. Frontend Chat Widget

**Vị trí:** `templates/dashboard.html` (cuối file)

```html
<!-- Nút mở chat -->
<button id="chat-toggle-btn" class="chat-toggle-btn">💬</button>

<!-- Cửa sổ chat -->
<div id="chat-widget" class="chat-widget">
    <div class="chat-header">🤖 Trợ lý Căng tin</div>
    <div id="chat-messages" class="chat-messages">...</div>
    <div class="chat-input-area">
        <input type="text" id="chat-input" placeholder="Nhập câu hỏi...">
        <button id="send-chat">Gửi</button>
    </div>
</div>

<script>
// JavaScript: Gọi /api/chat bằng fetch(), hiển thị phản hồi AI
const sendMessage = async () => {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    });
    const data = await response.json();
    botDiv.innerHTML = data.response.replace(/\n/g, '<br>');
};
</script>
```

**Mục đích:** Giao diện chat bong bóng nổi ở góc dưới bên phải Dashboard, cho phép người dùng hỏi AI trực tiếp.

---

## 4. PHẦN SINH VIÊN ĐÃ KIỂM TRA VÀ CHỈNH SỬA

### 4.1. Kiểm tra chức năng AI

| # | Nội dung kiểm tra | Kết quả | Ghi chú |
|---|-------------------|---------|---------|
| 1 | AI Đề xuất thực đơn có trả về đúng dữ liệu? | ✅ Đạt | AI chỉ dùng dữ liệu từ CSDL, không bịa |
| 2 | AI Tổng hợp phản hồi có tóm tắt đúng? | ✅ Đạt | Đối chiếu với bảng feedback trong SQLite |
| 3 | AI Báo cáo doanh thu có đúng số liệu? | ✅ Đạt | So sánh với query SQL trực tiếp |
| 4 | Chatbot có trả lời đúng khi hỏi doanh thu? | ✅ Đạt | Câu trả lời khớp dữ liệu |
| 5 | Chatbot có từ chối khi hỏi ngoài phạm vi? | ✅ Đạt | AI báo "chỉ có thông tin tổng quan" |

### 4.2. Kiểm tra bảo mật

| # | Nội dung kiểm tra | Kết quả | Ghi chú |
|---|-------------------|---------|---------|
| 1 | API Key có bị lộ trong code không? | ✅ An toàn | Dùng `.env` + `load_dotenv()` |
| 2 | `.env` có trong `.gitignore`? | ✅ Có | Không bị push lên Git |
| 3 | Endpoint `/api/chat` có yêu cầu đăng nhập? | ✅ Có | Dùng `@login_required` |
| 4 | Input người dùng có được kiểm tra? | ✅ Có | Check rỗng + strip() |

### 4.3. Kiểm tra xử lý lỗi

| # | Tình huống lỗi | Cách xử lý | Kết quả |
|---|---------------|------------|---------|
| 1 | API Key sai hoặc chưa có | Hiển thị "Chưa cấu hình GEMINI_API_KEY" | ✅ Không crash |
| 2 | Model Gemini bị quá tải (503) | `call_gemini` tự retry 3 lần, chờ 2-4-6 giây | ✅ Tự phục hồi |
| 3 | Model không tồn tại (404) | Tự chuyển sang model dự phòng | ✅ Fallback thành công |
| 4 | Mất kết nối mạng | Trả thông báo "Không thể kết nối" | ✅ Không crash |
| 5 | Người dùng gửi tin nhắn rỗng | Trả HTTP 400 + thông báo lỗi | ✅ Validate đúng |

### 4.4. Các chỉnh sửa quan trọng đã thực hiện

| # | Vấn đề phát hiện | Nguyên nhân | Cách sửa |
|---|-----------------|-------------|----------|
| 1 | AI không phản hồi sau khi thêm API key | `load_dotenv()` cache key cũ | Đổi thành `load_dotenv(override=True)` |
| 2 | Lỗi "model not found" (404) | Model `gemini-2.5-flash` bị ngưng hỗ trợ | Chuyển sang `gemini-3.5-flash` |
| 3 | Lỗi "503 UNAVAILABLE" | Server Gemini quá tải | Thêm hàm `call_gemini` với retry + fallback |
| 4 | Model dự phòng sai tên | `gemini-2.0-flash`, `gemini-1.5-flash` không tồn tại | Chạy `client.models.list()` để lấy đúng tên model |
| 5 | Code gọi Gemini trùng lặp ở 4 route | Copy-paste cùng logic | Tạo hàm `call_gemini()` dùng chung cho tất cả |

### 4.5. Quá trình tối ưu Prompt (3 vòng)

| Tiêu chí | Vòng 1 | Vòng 2 | Vòng 3 (sử dụng) |
|----------|--------|--------|-------------------|
| Có cấu trúc output rõ ràng | ❌ | Khá rõ | ✅ Rõ ràng |
| Có quy tắc chống bịa dữ liệu | ❌ | ✅ | ✅ |
| Có cảnh báo nguyên liệu | ❌ | ✅ | ✅ |
| Tách System/User Prompt | ❌ | ❌ | ✅ |
| Prompt lưu riêng file | ❌ | ❌ | ✅ (`prompts/`) |

Chi tiết xem tại: `docs/prompt_testing.md`

---

## 5. KẾT LUẬN

Hệ thống Smart Canteen tích hợp **4 chức năng AI** (Đề xuất thực đơn, Tổng hợp phản hồi, Báo cáo doanh thu, Chatbot trợ lý) sử dụng Google Gemini API. 

Toàn bộ prompt được:
- Tách riêng vào thư mục `prompts/` (không hardcode trong `app.py`).
- Tối ưu qua 3 vòng thử nghiệm.
- Có quy tắc chống bịa dữ liệu.

Code AI được:
- Xử lý lỗi đầy đủ (retry, fallback model, thông báo thân thiện).
- Bảo mật API Key (`.env` + `.gitignore`).
- Yêu cầu đăng nhập (`@login_required`).

Sinh viên đã kiểm tra, đối chiếu kết quả AI với dữ liệu thực tế trong CSDL và chỉnh sửa code/prompt khi phát hiện vấn đề.
