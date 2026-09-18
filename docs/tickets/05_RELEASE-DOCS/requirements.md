# Requirements - 05_RELEASE-DOCS

## 1. Thông tin chung
- **Ticket:** #05
- **Người yêu cầu (Actor):** DevOps / Ban Giám Khảo
- **Mục tiêu:** Hoàn thiện Logging, Viết tài liệu, Export Mock Videos & Benchmarking

## 2. Kiến trúc & Acceptance Criteria (AC)
- [x] AC 1: Rà soát codebase, thêm hệ thống logging (info, error) vào các sự kiện chuyển đổi trạng thái job.
- [x] AC 2: Hoàn thiện file `README.md` bao gồm: Hướng dẫn thiết lập (setup `requirements.txt`) và chạy (run) dịch vụ; Các lệnh API mẫu (cURL).
- [x] AC 3: Viết "Architecture Note" trong README giải thích cách vòng đời Job hoạt động, ranh giới lưu trữ.
- [x] AC 4: Cập nhật script generate video demo (`scripts/generate_mock_videos.py`). Script phải giả lập chạy thẳng hàm assemble_video qua các test case (Câu ngắn, câu vừa, câu dài, Unicode), không cần HTTP server. Bắt buộc có chức năng benchmark thời gian render cho mỗi video (in số giây).

## 3. Scope & Out of Scope
- **In Scope:** Dọn dẹp code, thêm log, update README.md hoàn chỉnh, export file nộp.
- **Out of Scope:** Code thêm tính năng logic.
