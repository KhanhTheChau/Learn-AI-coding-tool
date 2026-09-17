# Requirements - 01_PERSISTENCE

## 1. Thông tin chung
- **Ticket:** #01
- **Người yêu cầu (Actor):** Dịch vụ Backend (AI Chemistry Prototype)
- **Mục tiêu:** Khởi tạo Project FastAPI & Thiết kế Ranh giới Lưu trữ (Persistence)

## 2. Acceptance Criteria (AC)
- [ ] AC 1: Khởi tạo một project FastAPI với cấu trúc thư mục rõ ràng.
- [ ] AC 2: Định nghĩa các Pydantic models cho `Job` (bao gồm: `id`, `query`, `status`, `artifact_path`, `error_message`, `created_at`).
- [ ] AC 3: Đảm bảo các trạng thái của job bao gồm: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`.
- [ ] AC 4: Xây dựng một class `InMemoryJobRepository` (hoặc `LocalFileRepository`) để quản lý trạng thái công việc.
- [ ] AC 5: Repository chạy được các hàm CRUD cơ bản cho thực thể Job.

## 3. Scope & Out of Scope
- **In Scope:** Setup FastAPI cơ bản, khai báo model, tạo Repository mẫu.
- **Out of Scope:** Chưa tạo API endpoints (làm ở ticket sau), chưa gọi AI.
