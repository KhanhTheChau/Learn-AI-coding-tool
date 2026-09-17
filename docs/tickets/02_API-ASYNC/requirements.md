# Requirements - 02_API-ASYNC

## 1. Thông tin chung
- **Ticket:** #02
- **Người yêu cầu (Actor):** Frontend / API Client
- **Mục tiêu:** Thiết lập API Endpoints & Luồng xử lý bất đồng bộ

## 2. Acceptance Criteria (AC)
- [ ] AC 1: Xây dựng 4 API endpoints (POST `/jobs`, GET `/jobs`, GET `/jobs/{id}`, GET `/videos/{id}`).
- [ ] AC 2: Đối với `POST /jobs`, sử dụng `BackgroundTasks` để chạy hàm giả lập `process_video_job(job_id)`.
- [ ] AC 3: Hàm giả lập tạm thời chỉ sleep 5 giây (nhớ dùng `asyncio.sleep`) rồi cập nhật trạng thái job thành `COMPLETED`.
- [ ] AC 4: Trạng thái job được lưu trữ và cập nhật qua Repository (Dependency Injection).

## 3. Scope & Out of Scope
- **In Scope:** 4 endpoints RESTful, BackgroundTasks, giả lập luồng async 5 giây.
- **Out of Scope:** Xử lý AI thực tế, Video generation.
