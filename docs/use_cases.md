# TÀI LIỆU USE CASE (USE CASES DESIGN)

## 1. Xác định Actor
Hệ thống bao gồm 2 nhóm người dùng chính (Actors):
- **Admin (Quản lý Căng tin)**: Người có toàn quyền quản lý hệ thống, cấu hình dữ liệu, xem báo cáo toàn diện và nhận các tư vấn từ AI.
- **Staff (Nhân viên bán hàng/Thủ kho)**: Người trực tiếp thao tác bán hàng, kiểm kê nguyên liệu và ghi nhận phản hồi từ học sinh.

*(Lưu ý: Khách hàng/Học sinh không trực tiếp đăng nhập hệ thống, mà nhân viên sẽ là người thao tác hoặc khách hàng thao tác trên màn hình kiosk không cần đăng nhập).*

## 2. Danh sách Use Case

### Nhóm Use Case: Xác thực
1. **UC01 - Đăng nhập / Đăng xuất**: Cả Admin và Staff sử dụng để truy cập/thoát khỏi hệ thống.

### Nhóm Use Case: Quản lý Danh mục (Chỉ Admin)
2. **UC02 - Quản lý món ăn**: Thêm, sửa, xóa món ăn, cập nhật giá bán.
3. **UC03 - Quản lý nguyên liệu**: Nhập kho nguyên liệu, thiết lập định mức tối thiểu.
4. **UC04 - Quản lý nhà cung cấp**: Lưu thông tin liên hệ nhà cung cấp.

### Nhóm Use Case: Nghiệp vụ hàng ngày (Staff & Admin)
5. **UC05 - Quản lý bán hàng (POS)**: Chọn món, nhập số lượng, ghi nhận doanh thu và hệ thống tự trừ tồn kho.
6. **UC06 - Xem/Tìm kiếm/Lọc thông tin**: Tìm kiếm món ăn, tìm kiếm nhà cung cấp, lọc danh sách nguyên liệu.
7. **UC07 - Nhập phản hồi khách hàng**: Ghi nhận số sao (1-5) và bình luận của thực khách.

### Nhóm Use Case: Báo cáo & Thống kê
8. **UC08 - Xem Dashboard / Báo cáo**: Hiển thị tổng doanh thu, món bán chạy, nguyên liệu sắp hết.

### Nhóm Use Case: Trí tuệ nhân tạo (AI Integration)
9. **UC09 - Sinh thực đơn bằng AI**: Yêu cầu AI gợi ý món ăn nên bán dựa trên tồn kho.
10. **UC10 - Phân tích phản hồi bằng AI**: Nhờ AI tóm tắt các đánh giá tích cực/tiêu cực.
11. **UC11 - Phân tích kinh doanh bằng AI**: Nhờ AI đánh giá tổng quan doanh thu và đưa ra lời khuyên.

## 3. Sơ đồ Use Case (Minh họa)

```mermaid
usecaseDiagram
    actor Admin
    actor Staff

    usecase "Đăng nhập" as UC01
    usecase "Quản lý món ăn" as UC02
    usecase "Quản lý nguyên liệu" as UC03
    usecase "Bán hàng (POS)" as UC05
    usecase "Thu thập phản hồi" as UC07
    usecase "Xem Báo cáo" as UC08
    usecase "Tính năng AI (Gợi ý, Tóm tắt)" as UC09

    Staff --> UC01
    Staff --> UC05
    Staff --> UC07

    Admin --> UC01
    Admin --> UC02
    Admin --> UC03
    Admin --> UC05
    Admin --> UC07
    Admin --> UC08
    Admin --> UC09
```
