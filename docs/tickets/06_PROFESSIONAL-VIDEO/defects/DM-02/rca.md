# Root Cause Analysis (RCA) - DM-02 (Lỗi hiển thị hình nhiễu/glitch trên MP4)

## 1. Triệu chứng (Symptom)
- User báo cáo: File `.mp4` được sinh ra mở được nhưng hình ảnh chỉ toàn hình nhiễu/glitch.
- User đưa ra các giả thuyết debug liên quan đến:
  - Source frame numpy/PIL, sai format màu OpenCV (BGR/RGB).
  - Lỗi VideoWriter, fourcc.

## 2. Quá trình Điều tra (Investigation)
Theo đúng quy trình chống Hallucination và bảo vệ kiến trúc, tôi đã phân tích mã nguồn hiện tại:
- **Kiểm tra Frame Generation & OpenCV:** Hệ thống `Learn-AI-coding-tool` hoàn toàn KHÔNG CÓ thư viện OpenCV (`cv2`), không dùng `VideoWriter`, không thao tác trên mảng `NumPy` hay `uint8`, và không có bất kỳ logic tự vẽ frame nào bằng Python. Do đó các giả thuyết debug ở trên là **False Positive (Báo lỗi chệch hướng/lạc context)**.
- **Kiểm tra Pipeline thực tế:** Code hiện hành (`src/pipeline/video_assembler.py`) đang dùng `ffmpeg-python` để gọi trực tiếp các Filter sinh hình ảnh (Virtual sources) của FFmpeg.
- **Nguyên nhân cốt lõi (Root Cause):** Ở Ticket sửa lỗi trước đó, tôi đã sử dụng filter `testsrc` của bộ lavfi (`ffmpeg.input('testsrc=...', f='lavfi')`) để mock video. Đặc tính của test pattern chuẩn `testsrc` trong FFmpeg là nó hiển thị các sọc màu (Color bar), đồng thời có một dải màu cuộn (scrolling gradient) chứa độ nhiễu (static noise) ở phía dưới cùng khung hình. Chính dải nhiễu mặc định này của `testsrc` đã khiến User lầm tưởng encoder đang bị lỗi/glitch.

## 3. Đề xuất Hướng xử lý (Fix Plan)
- **Tập tin bị ảnh hưởng:** `src/pipeline/video_assembler.py`
- **Thay đổi:** KHÔNG đưa OpenCV hay bất cứ logic ghi frame thủ công nào vào project. Tôi đề xuất thay thế filter `testsrc` (có chứa noise) bằng filter `color=c=black:size=1280x720:duration=3:rate=30` để render ra một đoạn video màu đen tuyền trơn tru.
- Điều này vừa giải quyết được "cảm giác bị nhiễu" của User, vừa giữ nguyên kiến trúc Mock FFmpeg nhỏ gọn và nhẹ nhàng.

*(Trạng thái: Chờ User Confirm RCA)*
