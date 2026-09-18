# Bài Học Kinh Nghiệm (Lessons Learned) - DM-01

## 1. Tránh Lỗi False Positive & Bảo Vệ Kiến Trúc (Anti-Hallucination)
**Tình huống:** Người dùng báo cáo một lỗi không tồn tại trong hệ thống (VD: API sinh MP3 không phát được, trong khi hệ thống chỉ có logic sinh MP4).
**Kinh nghiệm:**
- **Tuyệt đối không đoán mò (No Guessing):** Khi nhận được báo cáo Bug, phải thực hiện `grep` toàn bộ dự án để kiểm tra tính năng/đoạn code đó có thực sự tồn tại trong repository hay không.
- **Không tùy tiện thêm code (No Ad-hoc Feature):** Nếu lỗi báo cáo thuộc về một miền nghiệp vụ khác hoặc tính năng chưa từng được design, Agent phải thông báo đó là "False Positive" và yêu cầu chuyển sang quy trình tạo Feature mới (`usage.md`), tuyệt đối không được tự ý viết thêm module/API mới vào nhánh fix bug.

## 2. Cách Mock File Video Hợp Lệ (Playable Mock Video)
**Tình huống:** Khi máy tính không có thư viện xử lý media (ví dụ thiếu `ffmpeg`), lập trình viên thường dùng Fallback ghi một chuỗi bytes giả (`mp4_signature`) để tạo file dummy qua mặt các bước check I/O file.
**Vấn đề:** Mặc dù hệ thống Backend không crash, nhưng khi Frontend/User tải file dummy này về, nó sẽ hoàn toàn không thể phát được bằng bất kỳ trình Media Player nào (gây ra sự cố giả như trên).
**Kinh nghiệm/Giải pháp chuẩn:**
- KHÔNG sử dụng chuỗi hex tĩnh (static hex bytes) cho các tệp media có tính tương tác.
- Dùng các bộ lọc (filter) tích hợp sẵn trong thư viện để sinh ra một file media thực thụ nhưng siêu nhỏ.
- **Mẫu Code chuẩn với `ffmpeg-python`:**
```python
# Thay vì raise Error hay ghi byte thô, hãy dùng lavfi testsrc
import ffmpeg

def create_playable_mock_video(output_path: str):
    # Sinh video đen (hoặc test pattern) dài 3 giây chuẩn YUV420p
    stream = ffmpeg.input('testsrc=duration=3:size=1280x720:rate=30', f='lavfi')
    audio = ffmpeg.input('anoisesrc=duration=3:color=brown', f='lavfi')
    stream = ffmpeg.output(stream, audio, output_path, vcodec='libx264', acodec='aac', pix_fmt='yuv420p', shortest=None)
    ffmpeg.run(stream, quiet=True, overwrite_output=True)
```
Quy chuẩn này phải được ghi nhớ và áp dụng nếu sau này dự án yêu cầu viết bất cứ đoạn Mock Fallback nào liên quan đến Video/Audio.
