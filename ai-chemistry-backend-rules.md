# Coding Rules & Debug - AI Chemistry Video Service Backend

Tài liệu này định nghĩa tiêu chuẩn lập trình và gỡ lỗi cho dự án Backend Prototype xây dựng bằng **FastAPI** và **Python 3.10+**. 
**QUAN TRỌNG:** Đây là bộ quy tắc đã được đúc kết sau 6 ticket/defect đầu tiên của dự án, mọi Agent BẮT BUỘC phải tuân thủ nghiêm ngặt để đảm bảo ra kết quả đúng ngay từ lần prompt đầu tiên.

## 1. Công nghệ & Framework
- **Core:** Python 3.10+, FastAPI, Pydantic v2.
- **Server:** Uvicorn.
- **Testing:** Pytest, httpx (cho TestClient). Unit test liên quan đến subprocess FFmpeg phải mock `subprocess.Popen`, KHÔNG sử dụng hex string/mock bytes để giả lập MP4 vì sẽ tạo file corrupt.
- **Typing/Linting:** Strict Type Hints, Ruff (hoặc Flake8/Black).
- **Dependency Management:** Sử dụng `requirements.txt` làm chuẩn duy nhất để đảm bảo tính khả thi triển khai.

## 2. Kiến trúc Sinh Video (Video Generation Architecture) BẮT BUỘC
Để đảm bảo chất lượng Professional-grade Video (1080p, 30fps) và tránh các lỗi đã từng gặp:
- **KHÔNG sử dụng OpenCV:** OpenCV quá nặng, render chữ xấu và không phù hợp.
- **Dùng Pillow (PIL):** Toàn bộ frame (khung hình) được vẽ bằng Pillow.
  - Sử dụng Font `Roboto` lưu ở `assets/fonts/` để render tiếng Việt (Unicode).
  - Sử dụng Layering: Tách lớp tĩnh (Static Background Gradient, Static Shadow UI, Bounding Box caching) ra khỏi lớp động (Dynamic Text Animation Fade-in/Slide-up) để giữ FPS ổn định.
  - Tự động tách đoạn chữ dài ra nhiều Scene để đảm bảo khả năng đọc.
- **FFmpeg Raw Pipe:** Render frame ra numpy arrays (RGB24) và ghi thẳng vào `process.stdin` của subprocess `ffmpeg` (để encode H.264 MP4).
- **Tránh Subprocess Deadlock:** Phải luôn đẩy `stderr` của FFmpeg vào một log file tạm (vd: `stderr=open("...log", "w")`) hoặc xử lý bằng luồng riêng. NẾU để `stderr=subprocess.PIPE` mà không đọc, pipe buffer sẽ đầy (do ffmpeg ghi log liên tục) và gây treo toàn bộ ứng dụng (deadlock).

## 3. Cấu trúc Dự án BẮT BUỘC
Để giữ dự án sạch sẽ, tuân thủ cấu trúc "src-layout":
```
Learn-AI-coding-tool/
├── src/                    # Chứa toàn bộ mã nguồn, tài nguyên và bài test
│   ├── api/          # FastAPI Routers
│   ├── core/         # Config, Exceptions
│   ├── models/       # Pydantic schemas
│   ├── services/     # Job logic, Pipeline orchestration (Chứa Background Tasks)
│   ├── ai/           # AI Video Generator (Có cơ chế Retry & Validate Keyword)
│   ├── pipeline/     # Video Assembler (Pillow + FFmpeg stdin pipeline)
│   ├── repositories/ # Storage (In-memory/File)
│   ├── assets/       # Tài nguyên tĩnh (Fonts, mockup images...)
│   ├── tests/        # Unit Tests
│   └── main.py       # FastAPI entrypoint
├── docs/             # Tài liệu, requirements
├── output/           # Chứa kết quả sinh từ pipeline (exported_videos, extracted_frames)
├── scripts/          # Script chạy tiện ích (generate_mock)
└── requirements.txt
```

## 4. Quy tắc Fix Bug / Debug
- **RCA Documentation:** Trước khi đổi code, luôn viết RCA (Root Cause Analysis). Đọc trực tiếp code router và traceback, không giả định.
- **Traceability:** Nếu gặp bug về async task (Job bị kẹt ở PROCESSING), kiểm tra ngay việc có sử dụng hàm blocking (như `time.sleep`) trong thread của asyncio hay không. Đẩy các tác vụ nặng vào `BackgroundTasks`.
- **API Contracts:** Lỗi liên quan đến Validation Body/Query Parameter thường nằm ở khai báo Pydantic. Hãy kiểm tra các file `models/` trước khi check logic router.
- **Không "Swallow" Exception:** Khi fix bug do crash, không được bọc bằng `except Exception: pass`. Phải log lỗi và cập nhật state của Job thành `FAILED`.

## 5. Trạng thái Job & Caching
- **State Machine:** Mỗi Job (Video Task) đi qua các trạng thái: `PENDING` -> `PROCESSING` -> `COMPLETED` (có artifact_path) hoặc `FAILED` (có error_message).
- **Caching Logic:** Job mới gửi lên NẾU trùng khớp `query` với một Job đã hoàn thành trước đó (cùng file name mapping) thì phải trả về kết quả ngay (trạng thái `COMPLETED`) để reuse video, không chạy lại quy trình render (tuân thủ mục tiêu `Same Question -> Same Video Asset`).
