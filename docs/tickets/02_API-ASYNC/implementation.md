# Implementation - 02_API-ASYNC

## Các file đã thay đổi/tạo mới:
- **`src/models/job.py`:** Bổ sung class `JobCreateRequest` với Pydantic validation (min_length=5, max_length=1000) chống rỗng và giới hạn độ dài.
- **`src/services/video_service.py`:** Tạo hàm `process_video_job` mô phỏng luồng AI bằng `await asyncio.sleep(5)`. Đặc biệt có khối `try...except` để catch mọi lỗi (nếu xảy ra) và update trạng thái về `FAILED`.
- **`src/dependencies.py`:** Tạo file chứa Dependency Injection `get_job_repository()` để tiêm `InMemoryJobRepository` một cách thống nhất.
- **`src/routers/job_router.py`:** Triển khai 4 API (POST `/jobs` với status 202 Accepted, GET `/jobs`, GET `/jobs/{id}`, GET `/videos/{id}`). Sử dụng `fastapi.BackgroundTasks` để ném tiến trình xử lý ngầm.
- **`src/main.py`:** Khai báo `app.include_router(job_router.router)` để đăng ký các API.

Code đã bám sát 100% feedback thiết kế từ AI Reviewer (chú trọng về Exception Handling, Resilience, Non-blocking, và Validation).
