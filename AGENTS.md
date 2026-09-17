# AI Chemistry Video Service - Project Instructions & AGENTS

Tài liệu này định nghĩa kiến trúc cốt lõi, quy trình phát triển và các quy tắc BẮT BUỘC mà mọi AI Assistant PHẢI tuân thủ trong dự án này (FastAPI Backend).

## 1. Foundational Rules
- Core framework: **FastAPI** + Pydantic v2.
- Architecture: Layered (Router -> Service -> Repository).
- Logic tạo video bắt buộc phải bất đồng bộ (Background Tasks).

## 2. Mandatory: Root Cause Analysis (Defect Workflow)
- Khi thực hiện sửa lỗi (Bug/Defect), Agent **BẮT BUỘC** phải tiến hành phân tích nguyên nhân gốc rễ (RCA) bằng cách đọc code thực tế thay vì đoán mò. 
- Không được phép thay đổi code nếu RCA chưa được người dùng xác nhận (Confirm).

## 3. Mandatory: API Contract & Typing Checks
- **Trước khi đổi API Response:** Nếu một defect yêu cầu sửa response schema, Agent phải `grep` toàn bộ project (đặc biệt là folder `tests/`) để đảm bảo không làm gãy các test cases hiện tại.
- Tất cả hàm mới hoặc sửa đổi đều phải có Strict Type Hints. QC Agent phải kiểm tra điều này.

## 4. Agent Roles & Workflow
Dự án hoạt động với đội ngũ chuyên biệt.
- Sử dụng `usage.md` cho việc xây dựng Feature mới.
- Sử dụng `defect_usage.md` cho việc xử lý Bug / Defect.

## 5. Cập nhật Memory (Bài học kinh nghiệm)
Sau khi fix xong bất kỳ một defect nào, Agent phải chủ động hỏi người dùng có muốn lưu kinh nghiệm/anti-pattern vừa phát hiện vào system memory để tránh lặp lại lỗi tương tự trong các phiên code sau không.
