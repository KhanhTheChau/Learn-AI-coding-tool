# Architecture & API Design - 01_PERSISTENCE

## 1. Data Models (Pydantic / DB)
- **Model Name:** Job
- **Description:** Đại diện cho một job trong hệ thống (AI video generation job).
- **Fields:**
  - `id`: `str` (UUID hoặc chuỗi định danh duy nhất)
  - `query`: `str` (Nội dung yêu cầu từ user)
  - `status`: `JobStatus` (Enum với 4 trạng thái: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`)
  - `artifact_path`: `str | None` (Đường dẫn tới kết quả sau khi hoàn thành, mặc định `None`)
  - `error_message`: `str | None` (Nội dung lỗi nếu status là `FAILED`, mặc định `None`)
  - `created_at`: `datetime` (Thời gian tạo job)

## 2. API Contracts
- (Ticket này chưa yêu cầu tạo API Endpoint - Out of Scope)

## 3. Background Tasks / Async Flow
- (Ticket này chưa yêu cầu gọi AI / xử lý logic - Out of Scope)
- **Thiết kế Repository pattern:**
  - Sẽ có abstract class `JobRepository` quy định các contract (phương thức) quản lý state.
  - Implement class `InMemoryJobRepository` để lưu các Job vào `dict` trên RAM (hoặc `LocalFileRepository`).
  - Hỗ trợ các hàm CRUD cơ bản:
    - `create(job: Job) -> Job`
    - `get(job_id: str) -> Job | None`
    - `update(job: Job) -> Job`
    - `list() -> list[Job]`
