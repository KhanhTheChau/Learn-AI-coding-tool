# Tóm tắt Yêu cầu & Kiến trúc Cốt lõi của Dự án (Snapshot)

Tài liệu này đóng vai trò là kim chỉ nam về kiến trúc, bao gồm tất cả các thành phần cốt lõi của Backend Video Service. Mọi Agent tiếp nhận dự án này bắt buộc tuân thủ hoàn toàn thiết kế dưới đây mà không đi đường vòng hay sử dụng thư viện thay thế.

## 1. Base API & State Machine (Ticket 1 & 2)
- **Mục tiêu:** Xây dựng hệ thống REST API bằng FastAPI, tiếp nhận yêu cầu (Job) sinh video và quản lý vòng đời của Job.
- **Thiết kế Chuẩn:** 
  - Tạo model Pydantic chứa `job_id`, `query`, `status`, `artifact_path`, `error_message`. 
  - Vòng đời Job có 4 trạng thái bắt buộc: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`. 
  - Tích hợp `BackgroundTasks` trong Route API để không block luồng xử lý chính. Mọi logic gọi AI hay render video đều phải đẩy vào background task.
  - Sử dụng Repository Pattern (Lưu In-Memory dictionary) để dễ test và mock.

## 2. AI Video Generator Logic & Non-Determinism Handling (Ticket 3)
- **Mục tiêu:** Sinh kịch bản hóa học dựa trên query của người dùng (tích hợp gọi LLM) với 3 câu truy vấn Tiếng Anh bắt buộc (`pH scale`, `covalent bonds`, `ionic vs covalent`).
- **Thiết kế Chuẩn:** 
  - Sử dụng class `AIVideoGenerator` với hàm `generate_with_retry(query, max_retries=3)`.
  - **Treat AI Non-determinism as an Engineering Problem:** Phải giả lập một tỷ lệ Hallucination (vd: 20%) để test. Content Validation bắt buộc kiểm tra output AI phải chứa ít nhất một thuật ngữ chuyên ngành (keyword hóa học). Nếu không có, phải tự động văng lỗi (Exception) và Retry tự động.

## 3. Third-Party Provider & Mock Mode Architecture (Ticket 4 & DM-01)
- **Mục tiêu:** Tích hợp với dịch vụ sinh video bên thứ ba (Third-Party), cung cấp cơ chế Fallback Mock Mode chạy cục bộ khi không có API key.
- **Thiết kế Chuẩn:**
  - `ThirdPartyVideoProvider` là module cắm thả (plug-and-play). Đọc biến `VIDEO_API_KEY`.
  - **Với API Key:** Giả lập Polling API (chờ kết quả) bằng `asyncio.sleep`, xử lý lỗi mạng (network timeout, 500 server error) bằng `try/except` và Retry mechanism. Nếu thất bại sau tất cả lần thử, Job phải được đánh `FAILED` và ghi lỗi.
  - **Không có API Key (Mock Mode):** Fallback về bộ nguồn Pillow + FFmpeg cục bộ `VideoAssembler` để xuất video `.mp4` minh họa xịn sò out-of-the-box (chạy ngay lập tức).

## 4. Local Video Rendering (Mock Mode)
- **Mục tiêu:** Sinh video khoa học giáo dục chất lượng cao với âm thanh TTS.
- **Thiết kế Chuẩn:**
  - *FFmpeg:* `subprocess.Popen` nối pipe stdin. Sử dụng `-shortest` kết hợp đầu vào `-i audio.mp3` để tự động ngắt video theo thời lượng âm thanh. Phải xử lý ngoại lệ đứt ống nước (`BrokenPipeError`) khi video dừng sớm. Tránh Deadlock bằng cách trút `stderr` ra file.
  - *Audio:* Sử dụng `gTTS` lưu ra file tạm, bọc trong `asyncio.to_thread` để tránh block FastAPI. Phải tự dọn dẹp file `.mp3` sau khi ghép nối thành công.
  - *Visual (Pillow):* Giao diện trình chiếu học thuật (không dùng giao diện chat). Chữ màu sáng, có Word Wrapping tự động bẻ dòng. Background là ảnh giáo khoa lấy từ `assets/images/` được crop vừa khung hình và đè phủ lớp màng mờ đen (60% opacity). Phải sử dụng cơ chế Caching Background Image (`self.bg_cache = {}`) trong lúc render để không làm chậm vòng lặp frame.

## 5. Development Scripts & Release Docs (Ticket 5)
- **Mục tiêu:** Đóng gói dự án để chạy kiểm định (mock run) và tài liệu chuẩn chỉ.
- **Thiết kế Chuẩn:** 
  - File `scripts/generate_mock_videos.py` giả lập API cho đúng 3 câu hỏi tiếng Anh bắt buộc. Test khả năng tự sửa sai lỗi AI (Retry loop).
  - Có file README.md với cấu trúc rõ ràng hướng dẫn setup `requirements.txt`. Cung cấp đầy đủ cURL chuẩn và giải thích kỹ càng sơ đồ Kiến trúc Third-party.
