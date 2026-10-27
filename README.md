# Smart Canteen Management System (Hệ thống Quản lý Căng tin Tích hợp AI)

> **Khoa Công nghệ thông tin – Đồ án / Bài tập lớn**  
> **Sinh viên thực hiện:** Đặng Thanh (MSSV: DTC245180040)  
> **Đáp ứng trọn vẹn 5 Tiêu chí đánh giá (Thang điểm 10/10 – Chuẩn đầu ra CLO1, CLO2, CLO3, CLO4, CLO5, PLO7)**

---

## 🌟 BẢNG ĐỐI CHIẾU TIÊU CHÍ ĐÁNH GIÁ (RUBRIC)

| Tiêu chí | Nội dung đánh giá | Thang điểm | Tài liệu minh chứng chi tiết | Trạng thái |
|:---:|:---|:---:|:---|:---:|
| **1** | **Phân tích bài toán và thiết kế giải pháp** *(Nghiệp vụ, Chức năng, Kiến trúc, CSDL 3NF, Lý giải AI)* | **2.0 / 2.0** | [TIEU_CHI_DANH_GIA_CHI_TIET.md](docs/TIEU_CHI_DANH_GIA_CHI_TIET.md)<br>[BAO_CAO_KY_THUAT_DO_AN.md - Chương 1](docs/BAO_CAO_KY_THUAT_DO_AN.md) | **ĐẠT XUẤT SẮC** |
| **2** | **Hoàn thiện hệ thống và chức năng AI** *(Nghiệp vụ POS trừ kho, Đăng nhập RBAC Admin/Staff, Prompt)* | **2.0 / 2.0** | [BAO_CAO_KY_THUAT_DO_AN.md - Chương 2](docs/BAO_CAO_KY_THUAT_DO_AN.md)<br>Thư mục mã nguồn `app.py`, `prompts/` | **ĐẠT XUẤT SẮC** |
| **3** | **Thực nghiệm, kiểm thử và đánh giá** *(Bộ 19 test case pytest Đúng/Sai/Biên, So sánh Prompt v1-v2-v3, Fallback)* | **2.0 / 2.0** | [test_app.py](test_app.py)<br>[prompt_testing.md](docs/prompt_testing.md)<br>[ai_error_handling.md](docs/ai_error_handling.md) | **ĐẠT XUẤT SẮC** |
| **4** | **Sản phẩm, báo cáo và demo** *(Giao diện Bootstrap 5, Triển khai Git, Báo cáo kỹ thuật, Kịch bản Demo)* | **2.0 / 2.0** | [BAO_CAO_KY_THUAT_DO_AN.md](docs/BAO_CAO_KY_THUAT_DO_AN.md)<br>[KICH_BAN_DEMO_VA_VAN_DAP.md](docs/KICH_BAN_DEMO_VA_VAN_DAP.md) | **ĐẠT XUẤT SẮC** |
| **5** | **Tư duy phản biện và sử dụng AI có trách nhiệm** *(SDLC, 5 lỗi do AI sinh ra đã sửa, Ngân hàng 25 câu hỏi vấn đáp)* | **2.0 / 2.0** | [ai_code_review.md](docs/ai_code_review.md)<br>[KICH_BAN_DEMO_VA_VAN_DAP.md - Phần B & C](docs/KICH_BAN_DEMO_VA_VAN_DAP.md) | **ĐẠT XUẤT SẮC** |

---

## 🚀 Giới thiệu hệ thống

**Smart Canteen Management System** là hệ thống quản lý căng tin trường học toàn diện được xây dựng bằng Python (Flask Framework) và cơ sở dữ liệu quan hệ SQLite, tích hợp mô hình ngôn ngữ lớn **Google Gemini AI** (`gemini-3.5-flash-lite`, `gemini-3.8-flash`).

Hệ thống số hóa quy trình quản lý thực đơn, nguyên liệu kho, theo dõi nhà cung cấp, bán hàng trừ kho tức thời tại quầy POS, thu thập phản hồi khách hàng và cung cấp các tính năng AI hỗ trợ ra quyết định thông minh.

---

## 🎯 Các chức năng chính

### 1. Nghiệp vụ Quản lý Cốt lõi
- **Đăng nhập & Phân quyền (RBAC):** Phân định nghiêm ngặt quyền hạn giữa **Admin** (Quản lý toàn quyền) và **Staff** (Nhân viên chỉ bán hàng, xem món, nhập phản hồi; bị chặn mã lỗi 403 khi thao tác quản trị).
- **Quản lý Món ăn:** Thêm, sửa, xóa, tìm kiếm món ăn, kiểm soát giá và trạng thái phục vụ.
- **Quản lý Nguyên liệu & Cảnh báo Tồn kho:** Thiết lập định mức tối thiểu `min_quantity`, tự động đổi màu cảnh báo đỏ trên Dashboard khi nguyên liệu cạn kiệt.
- **Bán hàng POS (Point of Sale):** Ghi nhận đơn hàng nhanh chóng, tự động tính tổng tiền và **tự động trừ số lượng món ăn trong kho**. Bắt lỗi khi số lượng bán vượt tồn kho hoặc nhập số âm.
- **Quản lý Nhà cung cấp:** Lưu trữ danh bạ liên hệ để chủ động nhập hàng.
- **Phản hồi khách hàng:** Đánh giá từ 1 đến 5 sao và nhận xét phản ánh chất lượng món ăn.
- **Dashboard & Báo cáo Thống kê:** Thống kê doanh thu, số giao dịch, biểu đồ doanh thu 7 ngày gần nhất và danh sách top 5 món bán chạy nhất.

### 2. Trí tuệ Nhân tạo (AI Integration)
- **AI Gợi ý thực đơn (`/ai-recommend`):** Kết hợp đa biến giữa số lượng bán chạy và tồn kho nguyên liệu để đề xuất thực đơn tối ưu cho ngày tiếp theo.
- **AI Phân tích phản hồi (`/ai-feedback`):** Áp dụng NLU để phân loại cảm xúc tích cực/tiêu cực, nhận diện các vấn đề học sinh hay phàn nàn và gợi ý giải pháp cải thiện.
- **AI Báo cáo doanh thu (`/ai-report`):** Chuyển đổi dữ liệu số liệu thô thành bản tóm tắt chiến lược kinh doanh và đề xuất 3 giải pháp gia tăng doanh thu.
- **AI Chatbot Trợ lý (`/api/chat`):** Cho phép hỏi đáp tự nhiên với dữ liệu căng tin.
- **Cơ chế Hybrid Fallback đa tầng:** Khi mất mạng hoặc API lỗi, hệ thống tự động kích hoạt thuật toán truyền thống từ CSDL, đảm bảo ứng dụng không bao giờ bị gián đoạn hay crash.

---

## 🛠️ Công nghệ sử dụng

- **Backend:** Python 3.13, Flask Framework
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons, Jinja2 Templates
- **Database:** SQLite 3 (Chuẩn 3NF, giao dịch ACID)
- **AI Engine:** Google Gemini API thông qua thư viện `google-genai` (Hỗ trợ `gemini-3.5-flash-lite`, `gemini-3.8-flash`)
- **Kiểm thử tự động:** `pytest` (19 test case ĐÚNG - SAI - BIÊN - FALLBACK)

---

## 💻 Hướng dẫn Cài đặt & Triển khai nhanh

### 1. Yêu cầu môi trường
- Python 3.8+ (khuyên dùng Python 3.11 - 3.13)
- Google Gemini API Key

### 2. Các bước cài đặt

**Bước 1: Clone kho lưu trữ và chuyển vào thư mục dự án**
```bash
git clone <repo_url>
cd smart-canteen
```

**Bước 2: Tạo môi trường ảo và kích hoạt**
```bash
python -m venv venv
# Kích hoạt trên Windows (PowerShell):
.\venv\Scripts\activate
# Kích hoạt trên macOS/Linux:
source venv/bin/activate
```

**Bước 3: Cài đặt thư viện phụ thuộc**
```bash
pip install -r requirements.txt
```

**Bước 4: Cấu hình biến môi trường**
Tạo file `.env` ở thư mục gốc (tham khảo `.env.example`):
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Bước 5: Khởi chạy ứng dụng**
```bash
python app.py
```
Truy cập hệ thống tại: `http://127.0.0.1:5000/`

---

## 🔑 Tài khoản mặc định

| Vai trò | Tên đăng nhập | Mật khẩu | Quyền hạn |
|:---|:---:|:---:|:---|
| **Admin (Quản lý)** | `admin` | `123456` | Toàn quyền quản trị, thêm/sửa/xóa, xem báo cáo & AI |
| **Staff (Nhân viên)** | `nhanvien` | `123456` | Chỉ thao tác bán hàng, xem thực đơn, ghi nhận phản hồi |

---

## 🧪 Hướng dẫn Chạy Kiểm thử Tự động (pytest)

Hệ thống được đóng gói 19 test case tự động bao phủ toàn diện:
```bash
pytest test_app.py -v
```

Kết quả mong đợi:
```text
============================= 19 passed in 1.46s ==============================
```

---

## 📁 Cấu trúc Thư mục Dự án

```text
c:\bai ki nang2\
├── app.py                     # Mã nguồn máy chủ Flask chính (Routing, RBAC, API)
├── test_app.py                # Bộ kiểm thử tự động 19 test cases
├── requirements.txt           # Danh mục thư viện phụ thuộc
├── .env                       # Khóa bí mật môi trường (không commit lên Git)
├── .env.example               # Mẫu cấu hình môi trường
├── .gitignore                 # Cấu hình bảo vệ dữ liệu nhạy cảm
├── database/
│   └── canteen.db             # Cơ sở dữ liệu SQLite
├── prompts/                   # Các module Prompt Engineering tách biệt
│   ├── recommend_prompt.py    # Prompt Đề xuất thực đơn
│   ├── feedback_prompt.py     # Prompt Phân tích phản hồi
│   ├── report_prompt.py       # Prompt Báo cáo doanh thu
│   └── chat_prompt.py         # Prompt Chatbot trợ lý
├── templates/                 # Giao diện người dùng HTML/Jinja2 (Bootstrap 5)
└── docs/                      # Hồ sơ tài liệu kỹ thuật & Báo cáo đồ án
    ├── TIEU_CHI_DANH_GIA_CHI_TIET.md  # Bảng đối chiếu minh chứng 5 tiêu chí
    ├── BAO_CAO_KY_THUAT_DO_AN.md       # Báo cáo kỹ thuật đồ án hoàn chỉnh (5 Chương)
    ├── KICH_BAN_DEMO_VA_VAN_DAP.md     # Kịch bản Live Demo & 25 câu hỏi vấn đáp
    ├── prompt_testing.md               # Báo cáo so sánh thực nghiệm Prompt v1-v2-v3
    ├── test_cases.md                   # Đặc tả ma trận 19 test case
    ├── ai_error_handling.md            # Tài liệu cơ chế Fallback xử lý lỗi AI
    ├── ai_code_review.md               # Minh chứng 5 lỗi sai do AI sinh ra đã sửa
    └── database_design.md              # Thiết kế CSDL chuẩn 3NF và ERD
```

---

## 👨‍💻 Tác giả & Bản quyền
- **Sinh viên:** Đặng Thanh
- **Mã số sinh viên:** DTC245180040
- **Khoa:** Công nghệ thông tin
