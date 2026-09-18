# Implementation Fix Spec - DM-02

## 1. Logic Thay Đổi (Logic Changes)
Như đã được phân tích ở bước RCA và được User phê duyệt (Điểm 10/10), nguyên nhân gây ra hình ảnh "bị nhiễu/glitch" hoàn toàn xuất phát từ việc sử dụng filter `testsrc` của FFmpeg (mặc định chứa sọc màu và dải static noise cuộn ở mép dưới).

Để giải quyết, tôi đã thay thế filter này bằng một filter khác sạch sẽ hơn. Thay vì rewrite lại cả project bằng OpenCV như phỏng đoán ban đầu của Bug Report, tôi giữ nguyên kiến trúc `lavfi` siêu nhẹ.

## 2. Danh sách file đã sửa (Modified Files)
- `src/pipeline/video_assembler.py`

**Chi tiết Code thay đổi:**
```python
- stream = ffmpeg.input('testsrc=duration=3:size=1280x720:rate=30', f='lavfi')
+ stream = ffmpeg.input('color=c=black:size=1280x720:duration=3:rate=30', f='lavfi')
```

## 3. Kết quả mong đợi (Expected Results)
- Không thêm bất cứ thư viện nào ngoài `ffmpeg-python`.
- File MP4 sinh ra vẫn là `yuv420p`, dung lượng siêu nhỏ.
- Khi mở lên bằng trình phát video, hình ảnh sẽ là **màu đen tuyền (solid black)** trong suốt 3 giây, hoàn toàn biến mất dải hạt nhiễu (glitch/noise) gây khó chịu cho User.

*(Trạng thái: Đã sửa code, chờ User Confirm để chuyển sang bước QA / Test case)*
