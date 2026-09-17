# Architecture & API Design - 02_API-ASYNC

## 1. Data Models (Pydantic / DB)
- Tái sử dụng model `Job` và `JobStatus` (từ ticket 01_PERSISTENCE).
- **Thêm Model mới:**
  - **Model Name:** `JobCreateRequest`
  - **Fields:** 
    - `query`: `str` (Nội dung yêu cầu tạo video)
    - *Validation:* Sử dụng `Field(..., min_length=5, max_length=1000)` để ngăn prompt rỗng hoặc quá dài (chống Prompt Injection).

## 2. API Contracts

### 2.1. Submit Job
- **Endpoint:** `POST /api/v1/jobs`
- **Request Body:** `JobCreateRequest`
  ```json
  { "query": "Giải thích phản ứng Oxi hóa khử" }
  ```
- **Response (202 Accepted):** Trả về đối tượng `Job` vừa được tạo (status: `PENDING`).

### 2.2. Get All Jobs
- **Endpoint:** `GET /api/v1/jobs`
- **Response (200 OK):** `list[Job]`

### 2.3. Get Job by ID
- **Endpoint:** `GET /api/v1/jobs/{id}`
- **Response (200 OK):** Trả về `Job`. (Nếu không tồn tại, trả về 404 Not Found).

### 2.4. Get Video
- **Endpoint:** `GET /api/v1/videos/{id}`
- **Mục tiêu:** Mở rộng sau này để trả về file video hoặc redirect.
- **Response hiện tại:** 
  - Nếu `artifact_path` có giá trị: Redirect (hoặc trả về file info). 
  - Tạm thời: Trả về thông báo "Video is available at {artifact_path}" (200 OK) hoặc 404 nếu job chưa xong/không có kết quả.

## 3. Background Tasks / Async Flow
- Tạo một file service (ví dụ `src/services/video_service.py`).
- Implement hàm `async def process_video_job(job_id: str, repo: JobRepository):`
  - Bao bọc toàn bộ logic trong khối `try...except`.
  - Đầu tiên cập nhật job status thành `PROCESSING`.
  - Giả lập công việc AI bằng cách gọi `await asyncio.sleep(5)`.
  - Sau đó cập nhật job status thành `COMPLETED` và `artifact_path` thành chuỗi dummy (ví dụ: `https://dummy-bucket/videos/{job_id}.mp4`).
  - Nếu có exception xảy ra trong quá trình xử lý, log lỗi và **bắt buộc** cập nhật trạng thái Job thành `FAILED` kèm `error_message`.
- Khi user gọi `POST /api/v1/jobs`:
  - Controller (Router) sẽ khởi tạo Job mới thông qua repo.
  - Sử dụng `fastapi.BackgroundTasks` để ném hàm `process_video_job` vào luồng chạy ngầm.
  - Trả về ngay HTTP 202 Accepted cho user.

## 4. Dependency Injection
- Cấu hình `get_job_repository` dependency trong FastAPI để inject `InMemoryJobRepository` vào cả Router và Background Task.

## 5. Testing Strategy
- Sử dụng `pytest` kết hợp `httpx` (TestClient) để test các endpoints.
- Cần có unit test kiểm tra luồng thất bại của `process_video_job` bằng cách sử dụng `unittest.mock.AsyncMock` để throw Exception, đảm bảo `Job` tự động chuyển sang `FAILED`.
