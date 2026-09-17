# Test Plan - 02_API-ASYNC

## 1. Mục tiêu kiểm thử
Đảm bảo các API endpoints cho Job hoạt động chính xác, dữ liệu đầu vào được validate đúng bởi Pydantic, và luồng `BackgroundTasks` xử lý AI (bao gồm Happy Path và Failure Path) không bị crash.

## 2. Các kịch bản kiểm thử (Test Cases)

### 2.1. API Endpoints (`tests/test_job_router.py`)
Sử dụng `fastapi.testclient.TestClient`.
- `test_submit_job_success`: Gửi POST request hợp lệ, kiểm tra trả về HTTP 202 và có thuộc tính `id`.
- `test_submit_job_validation_error`: Gửi POST request với `query` rỗng hoặc quá dài (VD > 1000 ký tự), kiểm tra trả về HTTP 422 Unprocessable Entity.
- `test_get_all_jobs`: Gọi GET `/api/v1/jobs` và kiểm tra trả về dạng mảng.
- `test_get_job_success`: Gọi GET `/api/v1/jobs/{id}` với ID hợp lệ, kiểm tra HTTP 200.
- `test_get_job_not_found`: Gọi GET với ID ảo, kiểm tra HTTP 404.
- `test_get_video_not_ready`: Gọi GET `/api/v1/videos/{id}` với Job chưa hoàn thành, kiểm tra HTTP 404 (chưa có video).

### 2.2. Background Task (`process_video_job`)
Kiểm thử trực tiếp hàm `process_video_job` trong `src/services/video_service.py` bằng `pytest.mark.asyncio`.
- `test_process_video_job_success`: Dùng `unittest.mock.AsyncMock` để patch `asyncio.sleep`, đảm bảo Job được chuyển thành `COMPLETED` và có `artifact_path`.
- `test_process_video_job_failure`: Patch `asyncio.sleep` để `side_effect = Exception("API Timeout")`, đảm bảo exception được catch và Job chuyển sang `FAILED` với `error_message` hợp lệ.

## 3. Type Hints Audit
Đã audit bằng mắt:
- 100% các endpoint trong `job_router.py` đều có Strict Type Hints.
- Hàm `process_video_job` khai báo rõ `job_id: str, repo: JobRepository`.
- `JobCreateRequest` áp dụng triệt để Pydantic `Field`.
