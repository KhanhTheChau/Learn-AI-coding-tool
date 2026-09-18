# Architecture & Pipeline Design - 04_PIPELINE-VIDEO

## 1. Mục tiêu (Objective)
Xây dựng một Video Pipeline thực thụ để ghép nối Image và Audio thành file `.mp4` dựa trên kịch bản từ AI. Quản lý nội dung AI thông minh để trả về kịch bản chuyên sâu cho 3 câu hỏi Hóa học cố định, và cập nhật luồng trả file cho người dùng.

## 2. Kiến trúc & Logic

### 2.1. Nâng cấp `AIVideoGenerator` (Xử lý 3 câu hỏi)
- **File:** `src/ai/video_generator.py`
- **Logic:** 
  - Trong `_mock_ai_call`, kiểm tra `query` (đã lower-case).
  - Trả về 3 kịch bản cứng (mockup) cực kỳ chi tiết nếu query chứa:
    1. `"thang đo ph"`: Kịch bản về tính Axit/Bazơ.
    2. `"liên kết cộng hóa trị"`: Kịch bản chia sẻ electron.
    3. `"liên kết ion"`: Kịch bản lực hút tĩnh điện.
  - Các trường hợp khác: Giữ nguyên logic trả về kịch bản có từ khóa `oxi hóa khử` như cũ.

### 2.2. Xây dựng `VideoAssembler` (Pipeline Video)
- **Thư mục:** `src/pipeline/` (mới) và file `video_assembler.py`.
- **Thư viện:** Bổ sung `ffmpeg-python` vào `requirements.txt`.
- **Logic Class `VideoAssembler`:**
  - `async def assemble_video(self, script: str, output_path: str) -> str:`
    - Tạo thư mục đích nếu chưa có.
    - Cố gắng sử dụng `ffmpeg` để ghép 1 ảnh tĩnh (tạo tạm hoặc lấy từ `assets/`) và 1 file âm thanh thành `.mp4`.
    - **Fallback Cơ chế an toàn:** Việc cài đặt `ffmpeg` trên Windows có thể phức tạp. Do đó, tôi sẽ bọc logic ffmpeg vào `try-except`. Nếu HĐH của user không có `ffmpeg`, nó sẽ tự động sinh ra một file `.mp4` giả lập (valid dummy file) và lưu vào ổ cứng để luồng hệ thống vẫn chạy mượt mà.

### 2.3. Cập nhật `VideoService` & Static Files
- **Cập nhật `process_video_job`:**
  - Tích hợp `VideoAssembler`.
  - Thay vì gán cứng `artifact_path = "https://dummy-bucket..."`, giờ sẽ truyền đường dẫn vật lý cục bộ (VD: `static/videos/{job_id}.mp4`).
  - Gán `job.artifact_path = f"/static/videos/{job_id}.mp4"`.
- **Mount thư mục Static:**
  - Trong `src/main.py`, sử dụng `app.mount("/static", StaticFiles(directory="static"), name="static")` để cho phép user hoặc frontend tải file `.mp4` thực tế về máy.

## 3. Testing Strategy (Unit Test)
- Cập nhật test cũ của `AIVideoGenerator` để check 3 query mới.
- Viết Unit Test cho `VideoAssembler`, dùng `patch` để mock `ffmpeg.run` nhằm test xem pipeline có ném lỗi hoặc kích hoạt fallback chuẩn xác không.
