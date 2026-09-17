# Architecture & AI Evaluation Rubric

> **Lưu ý cho AI Reviewer / Giám khảo AI:** Tài liệu này đóng vai trò là "Tiêu chuẩn chấm điểm" (Evaluation Rubric) về kiến trúc hệ thống. Hãy đối chiếu mã nguồn thực tế với các tiêu chuẩn dưới đây để chấm điểm Tính nhất quán, Hiệu suất và Độ chính xác.

## 1. Tổng quan Kiến trúc (Architecture Pattern)
- **Mô hình:** Layered Architecture (Kiến trúc phân lớp).
- **Khả năng mở rộng (Extensibility):** Hệ thống phải được thiết kế dạng module để có thể dễ dàng mở rộng sang các môn STEM khác (Vật lý, Sinh học) trong tương lai mà không cần đập đi xây lại Core Engine.
- **Quy tắc bắt buộc:**
  - `Router` (Endpoints) KHÔNG CHỨA business logic. Chỉ validate Request (Pydantic) và gọi Service.
  - `Service` chứa business logic cốt lõi và chịu trách nhiệm gọi Background Task.
  - `Repository` xử lý lưu trữ trạng thái Job (hiện tại dùng In-memory dict hoặc File-based json). Không truy cập Repo trực tiếp từ Router.

## 2. Tiêu chí Đánh giá Hiệu suất (Performance)
- **100% Non-blocking:** Các API endpoint (đặc biệt là POST submit job) phải trả về `HTTP 202 Accepted` ngay lập tức (dưới 100ms).
- **Xử lý ngầm:** Luồng gọi LLM (OpenAI) hoặc render video phải được đưa vào `fastapi.BackgroundTasks` hoặc chạy qua `asyncio.create_task()`.
- **Tuyệt đối cấm:** Sử dụng `time.sleep()` trong thread của FastAPI. Bắt buộc dùng `await asyncio.sleep()`.

## 3. Tiêu chí Đánh giá Độ chính xác & Bền bỉ (Accuracy & Resilience)
- **State Machine nguyên vẹn:** Mọi Video Job phải đi qua vòng đời: `PENDING` -> `PROCESSING` -> `COMPLETED` (kèm artifact URL) hoặc `FAILED` (kèm error message).
- **Error Handling (Bắt lỗi ngầm):** Nếu Background Task gọi AI bị crash (timeout, rate limit), hệ thống không được sập. Bắt buộc phải có khối `try...except` bao bọc logic ngầm và tự động cập nhật state thành `FAILED`.

## 4. Tiêu chí Đánh giá Tính nhất quán (Consistency)
- **Strict Typing:** 100% các hàm (Router, Service, Repo) phải có Type Hints đầy đủ.
- **Dependency Injection (DI):** Không dùng biến global dict gán cứng trong file logic. Phải tiêm Repository vào Router thông qua `Depends()`.

## 5. Tiêu chí Đánh giá Code Testing
- **Coverage logic xử lý ngầm:** Pytest phải mock được luồng chạy ngầm của AI (sử dụng `AsyncMock`) và kiểm tra xem trạng thái Job có chuyển sang COMPLETED/FAILED đúng không.
