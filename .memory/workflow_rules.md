# Quy tắc Dừng & Ghi nhận lỗi (Anti-Drift Extension) & Các Bài học Anti-Patterns

Kinh nghiệm rút ra từ quá trình xây dựng và nghiệm thu toàn bộ dự án:
Để tránh AI tự động chạy qua lỗi mà không báo cáo, và tránh lặp lại các sai lầm kiến trúc, bắt buộc tuân thủ quy tắc sau:

## 1. Quy tắc Dừng (STRICT STOP)
Tại cuối mỗi bước lớn (Bước 1, 2, 3, 4) trong `usage.md` hoặc `defect_usage.md`, Agent TUYỆT ĐỐI KHÔNG ĐƯỢC tự động làm tiếp. Agent phải dừng lại, trình bày kết quả và chỉ được phép thực hiện bước tiếp theo khi User gõ chính xác chữ "Confirm" (hoặc đồng ý rõ ràng).

## 2. Ghi nhận Lỗi (Error Logging) & Root Cause Analysis
Nếu có bất kỳ lỗi nào xảy ra trong quá trình thực thi (test thất bại, lỗi linter, ngoại lệ hệ thống...), Agent PHẢI lưu chi tiết lỗi và kết quả phân tích nguyên nhân (RCA) vào file trạng thái của ticket (hoặc tạo file lỗi riêng) trước khi dừng lại báo cáo cho User. Không tự ý đoán mò sửa lỗi khi chưa được Confirm.

## 3. Các Anti-Patterns TUYỆT ĐỐI TRÁNH (Kinh nghiệm Đắt Giá)
- **Anti-Pattern 1 (Blocking in Asyncio):** Sử dụng `time.sleep()` hoặc bất kỳ I/O blocking call nào (ví dụ: `gTTS.save()` hoặc các call gọi ra mạng) trực tiếp trong FastAPI async endpoint. Phải đưa mọi quá trình render/AI vào `BackgroundTasks` và bọc API I/O blocking bằng `asyncio.to_thread`.
- **Anti-Pattern 2 (Sử dụng thư viện C++ nặng nề):** Tuyệt đối KHÔNG dùng thư viện `OpenCV` (cv2) để sinh video vì thư viện này nặng, không render được font chữ đẹp và gây xung đột. Luôn dùng `Pillow (PIL)` kết hợp `FFmpeg rawvideo stdout`.
- **Anti-Pattern 3 (Subprocess Deadlock):** Bỏ qua luồng stderr khi pipe dữ liệu vào `subprocess.Popen(ffmpeg)`. Việc ffmpeg liên tục xả log sẽ làm đầy buffer pipe của OS (64KB), khiến chương trình Python bị kẹt vô thời hạn (Deadlock). **Giải pháp bắt buộc:** Trỏ `stderr` vào một file log thực (vd: `stderr=open("log.txt", "w")`).
- **Anti-Pattern 4 (Mock sai cách trong Unit Test):** Trong quá trình test pipeline sinh video, KHÔNG viết bài test tạo file hex/rác để giả lập vì MP4 sinh ra sẽ corrupt. Phải mock `subprocess.Popen` (sử dụng `unittest.mock.patch`) để chặn quá trình call FFmpeg thực sự, sau đó verify rằng nó đã được gọi đúng.
- **Anti-Pattern 5 (Font Fallback kém):** Cố định hardcode font path chỉ có trên máy tính cá nhân. Phải dùng tính năng fallback (thử lấy trong thư mục `assets/fonts/Roboto.ttf`, nếu hỏng thì phải tự rớt về `ImageFont.load_default()`).
- **Anti-Pattern 6 (Chỉ test Metadata, bỏ qua Visual):** Sử dụng thư viện `testsrc` hoặc `color=black` trong `ffmpeg` để qua mặt test (tạo ra video đen xì). Việc test Video Generation phải kiểm định bằng mắt để đảm bảo có chữ (Text) và giao diện UI rõ ràng.
- **Anti-Pattern 7 (Tải Disk I/O trong Vòng lặp Render Khung hình):** Không bao giờ mở (`Image.open`) hoặc đọc tệp ảnh nền trong mỗi lần tạo frame (vd ở hàm `_render_frame`), điều này sẽ khiến quá trình render FFmpeg chậm đi hàng ngàn lần. Bắt buộc phải có một layer Caching (`self.bg_cache = {}`) để lưu dữ liệu tĩnh.
- **Anti-Pattern 8 (Crash văng Pipe do Audio ngắn hơn Video):** Khi dùng FFmpeg flag `-shortest` và gắn audio đầu vào, FFmpeg sẽ ngắt ống pipe stdin sớm ngay khi file mp3 kết thúc. Nếu vòng lặp Python vẫn cố ghi (`stdin.write`), sẽ gây lỗi `BrokenPipeError` hoặc `Errno 22` trên Windows làm sập toàn bộ background task. Luôn bọc `try/except BrokenPipeError` ở hàm write frame.
