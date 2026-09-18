# Requirements - 04_PIPELINE-VIDEO

## 1. Thông tin chung
- **Ticket:** #04
- **Người yêu cầu (Actor):** Dịch vụ Backend
- **Mục tiêu:** Sinh MP4 thô từ Text (The Core Assembler)

## 2. Kiến trúc & Acceptance Criteria (AC)
- [x] AC 1: Khởi tạo module `VideoAssembler` với phương thức `assemble_video(query, script, output_path)`.
- [x] AC 2: Thiết kế kiến trúc Pipe Frame: Chuyển dữ liệu ảnh trực tiếp sang `stdin` của subprocess `ffmpeg`. FFmpeg command bắt buộc bao gồm `-f rawvideo -vcodec rawvideo -s 1920x1080 -pix_fmt rgb24 -i - -c:v libx264 -pix_fmt yuv420p -preset fast -crf 23`.
- [x] AC 3: **Không sử dụng OpenCV.** 
- [x] AC 4: Cập nhật đường dẫn file vào `artifact_path` của Job.
- [x] AC 5: Bắt lỗi FFmpeg: Nếu subprocess crash hoặc return code khác 0, ném `RuntimeError` để hệ thống bắt và cập nhật Job thành `FAILED`. Tuyệt đối không dùng mã hex rác (fake mp4 header fallback) khi bị lỗi.

## 3. Scope & Out of Scope
- **In Scope:** Cấu hình pipeline gọi FFmpeg thực tế, trả về file hợp lệ.
- **Out of Scope:** Chưa làm giao diện UI đẹp, chưa xử lý word-wrap, chưa xử lý Unicode tiếng Việt (được thực hiện riêng ở Ticket UI).
