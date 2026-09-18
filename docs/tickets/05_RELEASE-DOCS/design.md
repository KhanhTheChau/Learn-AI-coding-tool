# Design & Release Strategy - 05_RELEASE-DOCS

## 1. Mục tiêu (Objective)
Hoàn thiện dự án bằng cách tăng cường khả năng theo dõi (observability) qua Logging, viết tài liệu Hướng dẫn sử dụng & Kiến trúc (README.md) chuẩn mực, và xuất các Artifact (Video) cho Ban Giám Khảo nghiệm thu.

## 2. Kế hoạch Triển khai (Execution Plan)

### 2.1. Tăng cường Logging (AC 1)
- **Mục đích:** Giúp Sysadmin và Developer dễ dàng theo dõi vòng đời của Job (từ lúc tạo, đang xử lý, cho đến thành công hoặc thất bại) thông qua console output.
- **Vị trí can thiệp:**
  - `src/routers/job_router.py`: Bổ sung log ở mức độ `INFO` khi một Job mới được submit.
  - `src/services/video_service.py`: 
    - Thêm `INFO` khi Job chuyển sang trạng thái `PROCESSING`.
    - Thêm `INFO` khi Job hoàn tất (`COMPLETED`).
    - Các log `ERROR` khi Job `FAILED` đã được implement từ Ticket 04, sẽ được giữ nguyên và rà soát lại.

### 2.2. Hoàn thiện README.md (AC 2 & AC 3)
- **Cấu trúc mới của README.md:**
  1. **Giới thiệu dự án:** Tổng quan về Backend tạo Video bằng AI.
  2. **Yêu cầu hệ thống & Setup:** Hướng dẫn tạo môi trường ảo (venv), cài đặt `requirements.txt` và lưu ý về việc cài đặt `ffmpeg` (kèm nhắc nhở về tính năng fallback nếu không cài).
  3. **Hướng dẫn chạy (Run):** Lệnh khởi động Uvicorn.
  4. **Hướng dẫn sử dụng (API Usage):** Cung cấp các lệnh `cURL` (format inline chuẩn Windows) cho các endpoint tạo Job, check Job, và GET video.
  5. **Architecture Note:**
     - Mô tả **Vòng đời Job (Job Lifecycle):** PENDING -> PROCESSING -> COMPLETED/FAILED.
     - Phân tích ranh giới lưu trữ: Job Info lưu ở Memory (Dictionary tạm), Video thực tế được lưu trên ổ cứng cục bộ (`/static/videos`).

### 2.3. Xuất Video Demo (AC 4)
- **Mục đích:** Cung cấp sẵn kết quả để Ban giám khảo không cần phải tự chạy lại toàn bộ môi trường nếu chỉ muốn xem output.
- **Cách thực hiện:** 
  - Khởi chạy server nội bộ.
  - Gọi API bằng 3 query Hóa học (`Thang đo pH`, `Liên kết cộng hóa trị`, `Liên kết ion`).
  - Lấy các file MP4 sinh ra từ thư mục `static/videos/`.
  - Tạo thư mục `exported_videos/` ở root của project và copy 3 file này sang đó, đặt tên rõ ràng (VD: `demo_ph.mp4`, `demo_conghoatri.mp4`, `demo_ion.mp4`).

*(Lưu ý: Step 1.2 và 1.3 của quy trình được đánh N/A do ticket này không yêu cầu thay đổi Pydantic schemas hay logic Asynchronous).*
