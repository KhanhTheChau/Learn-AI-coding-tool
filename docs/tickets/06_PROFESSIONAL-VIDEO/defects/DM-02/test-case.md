# Test Cases Verify Fix - DM-02

## 1. Regression Test (Luồng API Job)
- **Mục tiêu:** Đảm bảo thay đổi `video_assembler.py` không làm gãy luồng xử lý bất đồng bộ từ PENDING -> PROCESSING -> COMPLETED.
- **Phương pháp:** Chạy toàn bộ bộ test `pytest tests/` hiện có.
- **Kết quả:** Tất cả test case (đặc biệt là test workflow API) đều PASS xanh.

## 2. QA Test (Visual Verification)
- **Mục tiêu:** Xác minh hình ảnh file `.mp4` không còn sọc màu và dải nhiễu/glitch ở đáy video.
- **Phương pháp:**
  1. Chạy lệnh: `python scripts/generate_mock_videos.py`
  2. Dùng công cụ giải nén FFprobe hoặc mở trực tiếp 3 file `exported_videos/demo_*.mp4` bằng trình phát (VLC/Media Player).
- **Kết quả nghiệm thu:** Video phát mượt mà, khung hình chỉ hiển thị màu đen tĩnh duy nhất, không còn dải nhiễu như filter `testsrc` cũ. Khắc phục triệt để lỗi người dùng phàn nàn.

*(Trạng thái QA: Đã Pass, sẵn sàng Release)*
