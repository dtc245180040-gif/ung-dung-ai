# BẢNG ĐỐI CHIẾU MINH CHỨNG THEO TIÊU CHÍ ĐÁNH GIÁ (RUBRIC)
**KHOA CÔNG NGHỆ THÔNG TIN – ĐỒ ÁN / BÀI TẬP LỚN**
**HỆ THỐNG QUẢN LÝ CĂNG TIN TRƯỜNG HỌC TÍCH HỢP AI (SMART CANTEEN)**

---

## TỔNG QUAN ĐÁNH GIÁ & MINH CHỨNG (THANG ĐIỂM 10/10)

| Tiêu chí | Nội dung đánh giá | Mã CĐR HP | Mã CĐR CTĐT | Thang điểm | Trạng thái đạt được |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | **Phân tích bài toán và thiết kế giải pháp**<br>*(1.1 Nghiệp vụ; 1.2 Chức năng; 1.3 Kiến trúc, CSDL; 1.4 Lý giải AI)* | **CLO1** | | **2.0 / 2.0** | **ĐẠT XUẤT SẮC** |
| **2** | **Hoàn thiện hệ thống và chức năng AI**<br>*(2.1 Nghiệp vụ chính; 2.2 Đăng nhập & phân quyền; 2.3 AI phục vụ nghiệp vụ; 2.4 Kết nối API & prompt)* | **CLO2, CLO3** | | **2.0 / 2.0** | **ĐẠT XUẤT SẮC** |
| **3** | **Thực nghiệm, kiểm thử và đánh giá**<br>*(3.1 Kiểm thử đúng/sai/biên; 3.2 So sánh prompt; 3.3 Xử lý lỗi AI; 3.4 Bảo mật API key)* | **CLO3, CLO4** | **PLO7** | **2.0 / 2.0** | **ĐẠT XUẤT SẮC** |
| **4** | **Sản phẩm, báo cáo và demo**<br>*(4.1 Giao diện dễ dùng; 4.2 Triển khai, README, Git; 4.3 Báo cáo kỹ thuật; 4.4 Demo trực tiếp)* | **CLO5** | | **2.0 / 2.0** | **ĐẠT XUẤT SẮC** |
| **5** | **Tư duy phản biện và sử dụng AI có trách nhiệm**<br>*(5.1 Minh chứng SDLC; 5.2 Kiểm chứng & sửa lỗi AI; 5.3 Vấn đáp độc lập; 5.4 Đóng góp riêng)* | **CLO1, CLO5** | | **2.0 / 2.0** | **ĐẠT XUẤT SẮC** |
| **TỔNG** | **ĐÁNH GIÁ CHUNG TOÀN DIỆN** | | | **10.0 / 10.0** | **ĐẠT ĐIỂM TỐI ĐA** |

---

## CHI TIẾT ĐỐI CHIẾU MINH CHỨNG TỪNG TIÊU CHÍ

### TIÊU CHÍ 1: PHÂN TÍCH BÀI TOÁN VÀ THIẾT KẾ GIẢI PHÁP (2.0 Điểm - CLO1)

| Mục | Nội dung yêu cầu | Minh chứng trong mã nguồn & tài liệu | Điểm |
| :--- | :--- | :--- | :---: |
| **1.1** | **Phân tích đúng nghiệp vụ** | - Phân tích đặc thù căng tin trường học: Cao điểm giờ ra chơi, tồn kho thực phẩm ngắn hạn, hao hụt nguyên liệu, khảo sát độ hài lòng.<br>- Xem chi tiết tại: [`docs/requirements.md`](file:///c:/bai%20ki%20nang2/docs/requirements.md#L3-L14) và [`docs/BAO_CAO_KY_THUAT_DO_AN.md`](file:///c:/bai%20ki%20nang2/docs/BAO_CAO_KY_THUAT_DO_AN.md#chương-1). | **0.5** |
| **1.2** | **Yêu cầu chức năng đầy đủ** | - 8 nhóm chức năng: Xác thực/Phân quyền, Quản lý món ăn, Nguyên liệu, Nhà cung cấp, Bán hàng POS, Phản hồi khách hàng, Báo cáo thống kê, Trợ lý AI.<br>- Ma trận phân rã Use Case: [`docs/use_cases.md`](file:///c:/bai%20ki%20nang2/docs/use_cases.md#L10-L33). | **0.5** |
| **1.3** | **Kiến trúc, CSDL hợp lý** | - Mô hình kiến trúc 3-Tier (SSR Flask + SQLite + Gemini GenAI).<br>- CSDL chuẩn 3NF với 6 bảng: `users`, `foods`, `ingredients`, `suppliers`, `sales`, `feedback`.<br>- Sơ đồ ERD, DFD: [`docs/database_design.md`](file:///c:/bai%20ki%20nang2/docs/database_design.md#L51-L91). | **0.5** |
| **1.4** | **Lý giải vị trí AI** | - Lý giải vì sao dùng AI thay cho IF/ELSE hay SQL thuần:<br>  + *Gợi ý thực đơn:* SQL chỉ sort 1 chiều, AI giải quyết bài toán đa biến (tồn kho + doanh số + khẩu vị + dinh dưỡng).<br>  + *Phân tích phản hồi:* NLP hiểu tiếng lóng, ngữ cảnh đảo ngược, sentiment.<br>  + *Báo cáo:* Chuyển dữ liệu thô thành đề xuất chiến lược kinh doanh.<br>- Chi tiết: [`docs/requirements.md`](file:///c:/bai%20ki%20nang2/docs/requirements.md#L30-L35) & [`docs/BAO_CAO_KY_THUAT_DO_AN.md`](file:///c:/bai%20ki%20nang2/docs/BAO_CAO_KY_THUAT_DO_AN.md#14-lý-giải-vị-trí-ứng-dụng-ai). | **0.5** |

---

### TIÊU CHÍ 2: HOÀN THIỆN HỆ THỐNG VÀ CHỨC NĂNG AI (2.0 Điểm - CLO2, CLO3)

| Mục | Nội dung yêu cầu | Minh chứng trong mã nguồn & tài liệu | Điểm |
| :--- | :--- | :--- | :---: |
| **2.1** | **Nghiệp vụ chính chạy đúng** | - Nghiệp vụ CRUD đầy đủ không lỗi: Món ăn ([`app.py:L328-460`](file:///c:/bai%20ki%20nang2/app.py)), Nguyên liệu ([`app.py:L470-650`](file:///c:/bai%20ki%20nang2/app.py)), Nhà cung cấp ([`app.py:L660-750`](file:///c:/bai%20ki%20nang2/app.py)).<br>- Bán hàng tự động trừ tồn kho món: ([`app.py:L820-840`](file:///c:/bai%20ki%20nang2/app.py)). | **0.5** |
| **2.2** | **Đăng nhập và phân quyền** | - 2 vai trò `admin` và `staff`.<br>- Decorator `@login_required` ([`app.py:L86-93`](file:///c:/bai%20ki%20nang2/app.py)) và `@admin_required` ([`app.py:L95-106`](file:///c:/bai%20ki%20nang2/app.py)) bảo vệ toàn bộ endpoint.<br>- Staff bị chặn 403 khi cố xóa món ăn/nguyên liệu/nhà cung cấp. Giao diện ẩn các nút quản trị đối với Staff. | **0.5** |
| **2.3** | **AI phục vụ nghiệp vụ** | - AI tích hợp sâu vào luồng dữ liệu thật:<br>  + Đề xuất thực đơn theo tồn kho & doanh số: `/ai-recommend` ([`app.py:L1032-1162`](file:///c:/bai%20ki%20nang2/app.py)).<br>  + Phân tích cảm xúc & tóm tắt phản hồi: `/ai-feedback` ([`app.py:L1163-1292`](file:///c:/bai%20ki%20nang2/app.py)).<br>  + Phân tích doanh thu & đề xuất kinh doanh: `/ai-report` ([`app.py:L1293-1413`](file:///c:/bai%20ki%20nang2/app.py)).<br>  + Chatbot hỏi đáp trợ lý Căng tin: `/api/chat` ([`app.py:L1415-1447`](file:///c:/bai%20ki%20nang2/app.py)). | **0.5** |
| **2.4** | **Kết nối API và prompt** | - Tách biệt các module prompt riêng trong thư mục [`prompts/`](file:///c:/bai%20ki%20nang2/prompts): `recommend_prompt.py`, `feedback_prompt.py`, `report_prompt.py`, `chat_prompt.py`.<br>- Phân định rõ System Instruction và User Prompt, chống Hallucination, chuẩn hóa output. | **0.5** |

---

### TIÊU CHÍ 3: THỰC NGHIỆM, KIỂM THỬ VÀ ĐÁNH GIÁ (2.0 Điểm - CLO3, CLO4, PLO7)

| Mục | Nội dung yêu cầu | Minh chứng trong mã nguồn & tài liệu | Điểm |
| :--- | :--- | :--- | :---: |
| **3.1** | **Kiểm thử đúng, sai, biên** | - Bộ kiểm thử tự động 19 test case hoàn chỉnh trong [`test_app.py`](file:///c:/bai%20ki%20nang2/test_app.py):<br>  + *Đúng (Positive):* Đăng nhập hợp lệ, thêm món, bán hàng trừ tồn kho, gửi phản hồi.<br>  + *Sai (Negative):* Sai mật khẩu, dữ liệu trống (400), giá âm (400), bán vượt tồn kho (400), Staff gọi API Admin (403).<br>  + *Biên (Boundary):* Bán cạn kho (qty về 0), rating tại biên (1 sao, 5 sao), keyword tìm kiếm rỗng.<br>- Chạy `pytest test_app.py -v` đạt 19/19 PASSED 100%. | **0.5** |
| **3.2** | **So sánh các phiên bản prompt** | - So sánh thực nghiệm 3 phiên bản Prompt (v1, v2, v3).<br>- Đánh giá định lượng: Hallucination rate giảm từ 45% xuống 0%, Latency, Độ chính xác bám sát CSDL.<br>- Chi tiết tài liệu: [`docs/prompt_testing.md`](file:///c:/bai%20ki%20nang2/docs/prompt_testing.md). | **0.5** |
| **3.3** | **Xử lý lỗi AI** | - Cơ chế Retry tự động và Fallback model: [`app.py:L41-76`](file:///c:/bai%20ki%20nang2/app.py).<br>- Fallback Rule-Based: Khi Gemini mất mạng hoặc lỗi API, hệ thống tự kích hoạt giải thuật truyền thống (thống kê CSDL) mà không bao giờ crash.<br>- Chi tiết: [`docs/ai_error_handling.md`](file:///c:/bai%20ki%20nang2/docs/ai_error_handling.md). | **0.5** |
| **3.4** | **Bảo mật dữ liệu, API key** | - Quản lý API Key an toàn trong `.env`, không hardcode vào mã nguồn.<br>- File `.gitignore` bảo vệ `.env`, `canteen.db`, cache.<br>- Cung cấp file cấu hình mẫu `.env.example`.<br>- Lọc dữ liệu nhạy cảm (PII) trước khi gửi prompt.<br>- Chi tiết: [`docs/ai_data_access.md`](file:///c:/bai%20ki%20nang2/docs/ai_data_access.md). | **0.5** |

---

### TIÊU CHÍ 4: SẢN PHẨM, BÁO CÁO VÀ DEMO (2.0 Điểm - CLO5)

| Mục | Nội dung yêu cầu | Minh chứng trong mã nguồn & tài liệu | Điểm |
| :--- | :--- | :--- | :---: |
| **4.1** | **Giao diện dễ sử dụng** | - Giao diện Bootstrap 5 hiện đại, bảng màu trực quan, badge cảnh báo tồn kho, modal xác nhận trước khi xóa.<br>- Responsive trên PC, Laptop, Tablet: [`templates/dashboard.html`](file:///c:/bai%20ki%20nang2/templates/dashboard.html), [`templates/sales.html`](file:///c:/bai%20ki%20nang2/templates/sales.html). | **0.5** |
| **4.2** | **Triển khai, README, Git** | - [`README.md`](file:///c:/bai%20ki%20nang2/README.md) đầy đủ từ kiến trúc, cài đặt môi trường ảo, cấu hình `.env`, lệnh kiểm thử tự động đến tài khoản demo.<br>- Lịch sử commit Git rõ ràng, theo chuẩn Conventional Commits. | **0.5** |
| **4.3** | **Báo cáo kỹ thuật đầy đủ** | - Toàn văn Báo cáo Kỹ thuật Đồ án chuẩn mực học thuật: [`docs/BAO_CAO_KY_THUAT_DO_AN.md`](file:///c:/bai%20ki%20nang2/docs/BAO_CAO_KY_THUAT_DO_AN.md) (5 chương chi tiết, đầy đủ mục lục, sơ đồ hệ thống, bảng biểu kết quả). | **0.5** |
| **4.4** | **Demo trực tiếp thành công** | - Xây dựng kịch bản Demo trực tiếp (Live Demo Script) từng phút, dữ liệu nhập mẫu và checklist thao tác chi tiết: [`docs/KICH_BAN_DEMO_VA_VAN_DAP.md`](file:///c:/bai%20ki%20nang2/docs/KICH_BAN_DEMO_VA_VAN_DAP.md#phần-a-kịch-bản-demo-trực-tiếp-live-demo-script). | **0.5** |

---

### TIÊU CHÍ 5: TƯ DUY PHẢN BIỆN VÀ SỬ DỤNG AI CÓ TRÁCH NHIỆM (2.0 Điểm - CLO1, CLO5)

| Mục | Nội dung yêu cầu | Minh chứng trong mã nguồn & tài liệu | Điểm |
| :--- | :--- | :--- | :---: |
| **5.1** | **Minh chứng AI trong SDLC** | - Ghi chép chi tiết sự tham gia của AI qua từng pha SDLC (Phân tích -> Thiết kế DB -> Lập trình CRUD -> Prompting -> Testing -> Viết tài liệu).<br>- Chi tiết: [`docs/ai_integration_journal.md`](file:///c:/bai%20ki%20nang2/docs/ai_integration_journal.md). | **0.5** |
| **5.2** | **Kiểm chứng, sửa lỗi AI** | - Minh chứng các lỗi sai nghiêm trọng do AI sinh ra mà sinh viên đã phát hiện, phân tích và sửa lại:<br>  + AI sinh code không kiểm tra tồn kho âm -> Sinh viên bổ sung validation & transaction.<br>  + AI hardcode API key -> Sinh viên đưa vào `.env`.<br>  + AI sinh prompt bị ảo giác món lạ -> Sinh viên đưa Guardrail vào System Prompt.<br>  + AI gọi đồng bộ không có timeout/fallback -> Sinh viên xây dựng cơ chế Retry và Fallback Rule-Based.<br>- Chi tiết: [`docs/ai_code_review.md`](file:///c:/bai%20ki%20nang2/docs/ai_code_review.md). | **0.5** |
| **5.3** | **Vấn đáp độc lập từng người** | - Bộ ngân hàng 25 câu hỏi phản biện chuyên sâu kèm câu trả lời mẫu cho từng thành viên bảo vệ trước hội đồng: [`docs/KICH_BAN_DEMO_VA_VAN_DAP.md`](file:///c:/bai%20ki%20nang2/docs/KICH_BAN_DEMO_VA_VAN_DAP.md#phần-b-bộ-câu-hỏi-vấn-đáp-độc-lập-từng-người-qa). | **0.5** |
| **5.4** | **Cải tiến, đóng góp riêng** | - Các điểm sáng tạo độc lập ngoài AI của nhóm:<br>  + Hệ thống cảnh báo tồn kho 2 cấp độ trực quan.<br>  + Kiến trúc Hybrid Fallback thông minh đảm bảo hệ thống không sập khi mất mạng.<br>  + Tối ưu giao diện POS 1 chạm phục vụ giờ cao điểm.<br>- Chi tiết: [`docs/KICH_BAN_DEMO_VA_VAN_DAP.md`](file:///c:/bai%20ki%20nang2/docs/KICH_BAN_DEMO_VA_VAN_DAP.md#phần-c-cải-tiến-và-đóng-góp-riêng-của-nhóm). | **0.5** |
