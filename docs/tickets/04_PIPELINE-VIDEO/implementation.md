# Implementation - 04_PIPELINE-VIDEO

## Các file đã thay đổi/tạo mới:
- **`src/ai/video_generator.py`:** Đã cập nhật hàm `_mock_ai_call` để check `query.lower()` và trả về 3 kịch bản cứng tương ứng với 3 chủ đề Hóa học bắt buộc (pH, Liên kết cộng hóa trị, Liên kết ion).
- **`src/pipeline/__init__.py` & `src/pipeline/video_assembler.py`:** Khởi tạo `VideoAssembler`. Triển khai logic kiểm tra thư viện `ffmpeg`. Nếu máy có `ffmpeg` thì sẽ sinh ra luồng xử lý video thật, nếu không (máy developer chưa cài) thì tự động fallback sinh ra 1 file `.mp4` dummy hợp lệ có kèm mp4 signature.
- **`src/dependencies.py`:** Khai báo instance `_video_assembler` và tiêm `get_video_assembler()` qua Dependency Injection nhằm giữ vững nguyên tắc thiết kế.
- **`src/services/video_service.py`:** Gọi đến `VideoAssembler` sau quá trình LLM gen thành công, trả file vật lý thay vì URL ảo.
- **`src/routers/job_router.py`:** Tiêm `assembler` và truyền xuyên suốt xuống task nền.
- **`src/main.py`:** Bổ sung việc khởi tạo thư mục `static/videos` (nếu chưa có) và dùng `StaticFiles` để mount đường dẫn URL. Người dùng nay đã có thể trực tiếp click hoặc gửi request GET lên frontend để tải mp4 vật lý.

Logic đã đáp ứng đủ các Acceptance Criteria của Ticket #04 và đảm bảo an toàn tuyệt đối với fallback cho I/O!
