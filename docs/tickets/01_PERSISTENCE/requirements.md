# Requirements - 01_PERSISTENCE

## 1. Thông tin chung
- **Ticket:** #01
- **Người yêu cầu (Actor):** Dịch vụ Backend (AI Chemistry Prototype)
- **Mục tiêu:** Khởi tạo Project FastAPI & Thiết kế Ranh giới Lưu trữ (Persistence)

## 2. Kiến trúc & Acceptance Criteria (AC)
- [x] AC 1: Khởi tạo một project FastAPI với cấu trúc thư mục sạch sẽ (src-layout). Bắt buộc gom mã nguồn, assets, test vào `src/` (bao gồm: `src/api/`, `src/models/`, `src/services/`, `src/ai/`, `src/pipeline/`, `src/repositories/`, `src/assets/`, `src/tests/`). Các file xuất ra nằm trong `output/`.
- [x] AC 2: Định nghĩa các Pydantic models chuẩn cho `Job` (bao gồm: `id`, `query`, `status`, `artifact_path`, `error_message`, `created_at`).
- [x] AC 3: Đảm bảo các trạng thái của job được khai báo bằng Enum, bắt buộc phải có đủ 4 trạng thái: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`. Không được thiết kế thiếu trạng thái FAILED.
- [x] AC 4: Xây dựng một class `InMemoryJobRepository` để quản lý trạng thái công việc (dùng Dictionary in-memory để dễ mock/test).
- [x] AC 5: Bắt buộc tuân thủ quy tắc Không Khóa Luồng (Non-blocking I/O) khi thực hiện các tác vụ nặng.

## 3. Scope & Out of Scope
- **In Scope:** Setup FastAPI cơ bản, khai báo model, tạo Repository mẫu, setup `requirements.txt`.
- **Out of Scope:** Chưa tạo API endpoints (làm ở ticket sau), chưa gọi AI.
