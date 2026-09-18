# Requirements - 03_AI-CORE-RETRY

## 1. Thông tin chung
- **Ticket:** #03
- **Người yêu cầu (Actor):** Hệ thống Video Pipeline
- **Mục tiêu:** Thiết kế Ranh giới AI, Cơ chế Retry & Xác thực kết quả

## 2. Kiến trúc & Acceptance Criteria (AC)
- [x] AC 1: Tạo class `AIVideoGenerator` độc lập để handle mọi logic liên lạc LLM.
- [x] AC 2: Bắt buộc thiết kế class với cơ chế xử lý lỗi (guardrails): thêm logic retry (thử lại tối đa 3 lần nếu có lỗi hoặc hallucination trong quá trình sinh nội dung).
- [x] AC 3: Viết hàm `validate_chemistry_keywords(output)` để kiểm tra nội dung trả về từ AI có chứa ít nhất 1 từ khóa chuyên ngành hóa học (oxi, axit, bazơ, electron...) không. Ném exception nếu không hợp lệ để kích hoạt tiến trình retry.
- [x] AC 4: Ném RuntimeError và để Job tự chuyển trạng thái `FAILED` nếu hết số lần retry mà không thành công (fail-fast architecture).

## 3. Scope & Out of Scope
- **In Scope:** Logic xử lý AI Call, Retry mechanism, Validate LLM response.
- **Out of Scope:** Chưa tạo MP4 video ngay (làm ở ticket sau), không gọi API thật (sử dụng async mock).
