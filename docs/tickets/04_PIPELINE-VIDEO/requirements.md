# Requirements - 04_PIPELINE-VIDEO

## 1. Thông tin chung
- **Ticket:** #04
- **Người yêu cầu (Actor):** Dịch vụ Backend
- **Mục tiêu:** Xử lý 3 Truy vấn Hóa học & Khớp nối Video/Audio

## 2. Acceptance Criteria (AC)
- [ ] AC 1: Cập nhật logic của `AIVideoGenerator` để xử lý chính xác 3 câu hỏi bắt buộc: Thang đo pH, Liên kết cộng hóa trị, Khác biệt giữa liên kết ion/cộng hóa trị.
- [ ] AC 2: Giả lập việc gọi API để lấy hình ảnh/âm thanh, hoặc sử dụng các tệp tĩnh mô phỏng đầu ra của AI.
- [ ] AC 3: Sử dụng công cụ ghép nối (ví dụ: `ffmpeg-python`) để trộn hình ảnh và âm thanh thành một tệp `.mp4` hoàn chỉnh, lưu vào thư mục cục bộ của backend.
- [ ] AC 4: Cập nhật đường dẫn file vào `artifact_path` của Job.

## 3. Scope & Out of Scope
- **In Scope:** Cấu hình pipeline ghép file MP4 thực tế, trả về file hợp lệ cho 3 câu query cứng.
- **Out of Scope:** Không làm luồng AI generate ảnh thật (dùng ảnh mockup/âm thanh mockup cho nhanh để pass prototype).
