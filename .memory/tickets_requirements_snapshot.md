# Tóm tắt Yêu cầu & Kiến trúc Cốt lõi của Dự án (Snapshot)

Tài liệu này đóng vai trò là kim chỉ nam về kiến trúc, bao gồm tất cả các thành phần cốt lõi của Backend Video Service. Mọi Agent tiếp nhận dự án này bắt buộc tuân thủ hoàn toàn thiết kế dưới đây mà không đi đường vòng hay sử dụng thư viện thay thế.

## 1. Base API & State Machine (Ticket 1 & 2)
- **Mục tiêu:** Xây dựng hệ thống REST API bằng FastAPI, tiếp nhận yêu cầu (Job) sinh video và quản lý vòng đời của Job.
- **Thiết kế Chuẩn:** 
  - Tạo model Pydantic chứa `job_id`, `query`, `status`, `artifact_path`. 
  - Vòng đời Job có 4 trạng thái bắt buộc: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`. 
  - Tích hợp `BackgroundTasks` trong Route API để không block luồng xử lý chính. Mọi logic gọi AI hay render video đều phải đẩy vào background task.
  - Sử dụng Repository Pattern (Lưu In-Memory dictionary) để dễ test và mock.

## 2. AI Video Generator Logic (Ticket 3)
- **Mục tiêu:** Sinh kịch bản hóa học dựa trên query của người dùng (tích hợp gọi LLM).
- **Thiết kế Chuẩn:** 
  - Sử dụng class `AIVideoGenerator` với hàm `generate_with_retry(query, max_retries=3)`.
  - Content Validation: Bắt buộc kiểm tra output AI phải chứa ít nhất một thuật ngữ chuyên ngành (keyword hóa học). Nếu không có, phải tự động văng lỗi và retry.

## 3. Video Pipeline Core (Ticket 4 & DM-01)
- **Mục tiêu:** Pipeline render ra file H.264 MP4 từ kịch bản AI, phải đảm bảo chất lượng video không bị giật, không lỗi hình, tương thích mọi trình phát.
- **Thiết kế Chuẩn:**
  - Class `VideoAssembler` nhận chữ ký `assemble_video(query, script, output_path)`.
  - Sử dụng `subprocess.Popen` để mở luồng giao tiếp stdin tới FFmpeg. Không sử dụng thư viện `opencv-python` do không tối ưu để sinh text.
  - FFmpeg Command chuẩn: `-f rawvideo -vcodec rawvideo -s 1920x1080 -pix_fmt rgb24 -i - -c:v libx264 -pix_fmt yuv420p -preset fast -crf 23`.
  - Phải xử lý triệt để Exception: Khi FFmpeg bị crash, chương trình Python phải dừng sinh frame, catch lỗi, không sinh file rác và cập nhật Job thành `FAILED`.

## 5. Development Scripts & Release Docs (Ticket 5)
- **Mục tiêu:** Đóng gói dự án để chạy kiểm định (mock run) và tài liệu chuẩn chỉ.
- **Thiết kế Chuẩn:** 
  - File `scripts/generate_mock_videos.py` giả lập API, test qua 4 trường hợp gốc rễ: Short (câu ngắn), Medium (câu vừa), Long (câu siêu dài để test split scene), và Unicode (test Tiếng Việt).
  - Tích hợp Benchmark đo tốc độ render (FPS) cho mỗi lần chạy test.
  - Có file README.md với cấu trúc rõ ràng hướng dẫn setup `requirements.txt`.

## 6. Professional Visuals & Animations (Ticket 6)
- **Mục tiêu:** Xây dựng giao diện hiển thị chuyên nghiệp với UI 1080p, có background gradient, card bo góc, bóng mờ, xử lý hiển thị Unicode và Word Wrap.
- **Thiết kế Chuẩn:**
  - **Pillow Rendering System:** 
    - *Static Layer Cache:* Sử dụng thuật toán sinh meshgrid của `numpy` để tạo Gradient Background (chỉ tính 1 lần, sau đó lưu cache và copy ra mỗi frame).
    - Vẽ UI Card: Sử dụng `ImageDraw.rounded_rectangle` để vẽ hộp thoại bo góc, kết hợp `ImageFilter.GaussianBlur` để tạo bóng mờ 3D (shadow). Dùng `alpha_composite` ghép lên khung tĩnh.
    - *Animation:* Text phải có hiệu ứng trượt nhẹ (Slide up) và mờ dần vào (Fade in) dựa trên tỉ lệ tiến trình `time_in_scene`.
  - **Word Wrapping & Layout Cache:** Khung Text của Scene phải được đo đạc kích thước (bounding box) và bẻ dòng (word-wrap) 1 lần duy nhất lúc tính scene, lưu trạng thái `layout_cached=True`. Tuyệt đối không đo kích thước font ở mỗi frame để tiết kiệm CPU.
  - **Scene Splitting:** Chữ quá dài phải tự động được cắt thành các đoạn nhỏ (<40 chữ) để hiển thị thành các Scene liên tiếp. Thời lượng phải linh hoạt: `duration = max(4.0, word_count * 0.4)`.
  - **Tiếng Việt & Font:** Phải load file `.ttf` thật (Roboto-Regular, Roboto-Bold) từ thư mục `src/assets/fonts/` để hiển thị tiếng Việt có dấu.
  - **Tránh Deadlock Subprocess:** Khi gọi FFmpeg, bắt buộc đẩy `stderr` ra một file text thật trên ổ cứng (`open("...log", "w")`) để FFmpeg xả log, tránh hiện tượng đầy pipe OS gây treo (deadlock) luồng Python.
