# Requirements - 06_PROFESSIONAL-VIDEO

## 1. Thông tin chung
- **Ticket:** #06
- **Người yêu cầu (Actor):** End-user
- **Mục tiêu:** Cải tiến chất lượng video đạt mức Professional (Render text động, Word-wrap, UI đẹp, Tiếng Việt chuẩn).

## 2. Kiến trúc & Acceptance Criteria (AC)
- [x] AC 1: Áp dụng kiến trúc Rendering theo Layer:
  - Cache Base Background (Gradient lưới) bằng NumPy.
  - Vẽ giao diện UI Card (Bóng đổ Gaussian Blur, Khung bo góc) và dán lên static layer.
- [x] AC 2: Thiết lập xử lý tiến trình FFmpeg an toàn: Bắt buộc đẩy luồng log `stderr` vào một text file độc lập, không dùng `subprocess.PIPE` để tránh treo tiến trình.
- [x] AC 3: Xử lý Text & Tiếng Việt:
  - Tích hợp font Roboto (`.ttf` lưu ở `src/assets/fonts/`) để hiển thị Unicode có dấu đầy đủ.
  - Tự động Word-wrap text (xuống dòng nếu độ dài vượt khung hình) và căn chỉnh Layout bounding box từ trước. 
  - KHÔNG đo kích thước chữ trên từng frame để tối ưu FPS.
- [x] AC 4: Thuật toán Scene Splitting: Đoạn text của AI dài quá giới hạn chữ (khoảng 40 từ) phải tự bẻ thành các Scene liên tiếp (tự sinh thêm cảnh), với duration tự động theo số chữ (1 từ = ~0.4s).
- [x] AC 5: Thêm Animation nhẹ nhàng (Subtle easing): Frame đầu có Question fade in ở giữa. Các frame trả lời thì Question thu nhỏ và Answer Text được slide-up + fade-in từ dưới lên thông qua thuật toán mix kênh alpha.
- [x] AC 6: Giữ nguyên luồng BackgroundTasks và state machine của các tính năng trước đó.

## 3. Scope & Out of Scope
- **In Scope:** Visual Upgrade, Unicode, Scene parser, Layer caching trong `video_assembler.py`.
- **Out of Scope:** Không làm âm thanh, không đổi DB Schema.
