# Root Cause Analysis (RCA) - DM-01 (Lỗi file MP3 không thể mở/phát)

## 1. Triệu chứng (Symptom)
- User báo cáo: Hệ thống có API dùng AI để generate file `.mp3`. API trả về 200/Thành công và sinh ra file `.mp3`, nhưng file không thể mở hoặc phát được bằng trình phát audio. Yêu cầu debug toàn bộ flow từ AI/TTS service, decode, ghi file, MIME type, v.v.

## 2. Quá trình Điều tra (Investigation)
Theo đúng quy trình RCA, tôi đã tiến hành grep và quét toàn bộ mã nguồn của dự án (thư mục `src/`, `scripts/`, `tests/`):
- **Tìm kiếm từ khoá `mp3`, `tts`, `audio`:** KHÔNG CÓ bất kỳ API, Controller, hay Service nào trong dự án hiện tại (AI Chemistry Video Service) đảm nhiệm việc gọi AI Text-to-Speech (TTS) để sinh file `.mp3`.
- **Logic hiện tại của dự án:** Hệ thống backend hiện hành chỉ có duy nhất 1 API `POST /api/v1/jobs` dùng AI để sinh **kịch bản Text** (qua `AIVideoGenerator`) sau đó gọi `VideoAssembler` để ghép nối thành file video `.mp4`.
- **Trường hợp Fallback MP4:** Trong trường hợp server thiếu `ffmpeg`, `VideoAssembler` sẽ sinh ra một file dummy `.mp4` rỗng chỉ chứa Hex-header (magic bytes) để tránh crash hệ thống. Nhưng đây là đuôi `.mp4` và là Video, không phải API sinh `.mp3` độc lập.

## 3. Nguyên nhân gốc rễ (Root Cause)
**False Positive / Lệch Context dự án:** Lỗi được mô tả **không tồn tại** trong mã nguồn của kho chứa (Repository) `Learn-AI-coding-tool` hiện tại. Rất có thể bug này thuộc về một microservice khác (ví dụ: Audio Service) hoặc một repository khác mà hệ thống của tôi chưa được mount vào (hoặc là một bài test giả lập bug).

## 4. Đề xuất Hướng xử lý
Vì không có mã nguồn liên quan đến TTS / MP3 trong dự án này, tôi không thể sửa trực tiếp. Tôi đề xuất 2 phương án:
1. **Xác nhận lại thư mục/repo:** Bạn vui lòng cung cấp đường dẫn chính xác tới file Python đang xử lý sinh MP3 (nếu nó nằm ở một nhánh khác hoặc dự án khác).
2. **Xây dựng tính năng mới:** Nếu bạn muốn tôi **tạo mới** API sinh `.mp3` chuẩn xác với MIME type `audio/mpeg` và luồng ghi binary đúng đắn vào dự án này, chúng ta sẽ chuyển sang quy trình thêm Feature (`usage.md`) thay vì Fix Bug.

*(Trạng thái: Chờ User Confirm RCA)*
