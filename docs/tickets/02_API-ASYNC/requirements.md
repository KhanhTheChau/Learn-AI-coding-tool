# Requirements - 02_API-ASYNC

## 1. Thông tin chung
- **Ticket:** #02
- **Người yêu cầu (Actor):** Frontend / API Client
- **Mục tiêu:** Thiết lập API Endpoints & Luồng xử lý bất đồng bộ, Caching cơ bản

## 2. Kiến trúc & Acceptance Criteria (AC)
- [x] AC 1: Xây dựng 4 API endpoints (POST `/jobs`, GET `/jobs`, GET `/jobs/{id}`, GET `/videos/{id}`).
- [x] AC 2: Đối với `POST /jobs`, **bắt buộc** sử dụng `BackgroundTasks` (của FastAPI) để chạy hàm `process_video_job(job_id)`. Tuyệt đối không dùng logic synchronous / blocking.
- [x] AC 3: Xử lý ngoại lệ trong `process_video_job`. Nếu xảy ra lỗi ở bất kỳ khâu nào (render lỗi, AI lỗi), Job phải chuyển sang `FAILED` và lưu lại lỗi để API GET có thể lấy được.
- [x] AC 4: Trạng thái job được lưu trữ và cập nhật qua Repository (Dependency Injection).
- [x] AC 5: **Video Caching System:** Khi người dùng gửi một `POST /jobs` với một `query` đã từng được thực hiện thành công, API phải trả về ngay Job hoàn thành cũ (cùng video path) thay vì tạo Job mới để tiết kiệm tài nguyên.

## 3. Scope & Out of Scope
- **In Scope:** 4 endpoints RESTful, BackgroundTasks, Exception handling cho State Machine, Job Caching.
- **Out of Scope:** AI generation, Video generation.
