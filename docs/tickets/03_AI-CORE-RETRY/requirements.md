# Requirements - 03_AI-CORE-RETRY

## 1. Thông tin chung
- **Ticket:** #03
- **Người yêu cầu (Actor):** Hệ thống Video Pipeline
- **Mục tiêu:** Thiết kế Ranh giới AI, Cơ chế Retry & Xác thực kết quả

## 2. Acceptance Criteria (AC)
- [ ] AC 1: Tạo class `AIVideoGenerator`.
- [ ] AC 2: Thiết kế class với cơ chế xử lý lỗi (guardrails): thêm logic retry (thử lại tối đa 3 lần nếu có lỗi trong quá trình sinh nội dung).
- [ ] AC 3: Viết hàm `validate_output()` để kiểm tra nội dung tạo ra có hợp lệ hay không. Nếu không, ném exception để kích hoạt tiến trình retry.
- [ ] AC 4: Trả về trạng thái `FAILED` rõ ràng nếu hết số lần retry thay vì fail silently.

## 3. Scope & Out of Scope
- **In Scope:** Logic xử lý AI Call, Retry mechanism, Validate LLM response.
- **Out of Scope:** Chưa tạo MP4 video ngay (làm ở ticket sau), không gọi API thật nếu có thể mock.
