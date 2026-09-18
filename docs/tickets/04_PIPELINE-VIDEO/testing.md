# Testing Plan - 04_PIPELINE-VIDEO

## 1. Mục tiêu (Objective)
Đảm bảo module `VideoAssembler` xử lý an toàn (fallback) khi môi trường thiếu ffmpeg và Module AI trả về đúng kịch bản cứng theo 3 queries yêu cầu.

## 2. Kịch bản Test (Test Cases)

### 2.1. Test VideoAssembler (Fallback Mechanism)
- File: `tests/test_pipeline.py`
- Test: `test_assemble_video_fallback`
  - Dùng `unittest.mock.patch` để chặn gọi hàm `ffmpeg.probe` và ép ném ra lỗi `FileNotFoundError` giả lập máy Windows không có ffmpeg.
  - Kỳ vọng: File `.mp4` dummy được tạo thành công ở thư mục `tmp_path`, file không rỗng và có byte signature chuẩn MP4, không làm crash luồng.

### 2.2. Bổ sung Test AI Video Generator (Cập nhật `tests/test_ai_generator.py`)
- Test: `test_mock_ai_call_specific_queries`
  - Kiểm tra 3 query: "thang đo ph", "liên kết cộng hóa trị", "liên kết ion".
  - Kỳ vọng: Hàm `_mock_ai_call` trả về chuỗi kịch bản có chứa thông tin đặc thù thay vì kịch bản mặc định.

## 3. Lệnh chạy và Kết quả
Chạy lệnh `pytest tests/test_pipeline.py tests/test_ai_generator.py -v`.
Tất cả các case bắt buộc phải PASSED.
