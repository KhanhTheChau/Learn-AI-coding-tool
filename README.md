# AI Chemistry Video Service

Đây là dịch vụ Backend (FastAPI) chịu trách nhiệm tự động tạo ra các video giáo dục Hóa học thông qua AI. Dự án sử dụng mô hình Async/Await để đảm bảo tính non-blocking, quản lý trạng thái qua một State Machine vòng đời, và bảo vệ hệ thống chặt chẽ với Guardrails.

## 1. Yêu cầu & Thiết lập (Setup)

**Môi trường:**
- Python 3.10+
- (Tuỳ chọn nhưng Khuyến nghị) FFMPEG đã được cài đặt và thiết lập biến môi trường (PATH) để có thể ghép video thực tế.

**Cài đặt:**
```bash
# 1. Tạo môi trường ảo
python -m venv venv
venv\Scripts\activate  # Trên Windows
# source venv/bin/activate  # Trên Linux/Mac

# 2. Cài đặt thư viện
pip install -r requirements.txt
```

## 2. Khởi chạy Dịch vụ (Run)

Sử dụng uvicorn để khởi chạy server ở chế độ reload (dành cho môi trường dev):
```bash
uvicorn src.main:app --reload
```
Server mặc định chạy tại: `http://localhost:8000`

## 3. Hướng dẫn Sử dụng API (Usage)

### 3.1. Submit Job Tạo Video
Hãy sử dụng cURL để submit một query cho AI. Hệ thống đang hỗ trợ 3 chủ đề chuyên sâu: `Thang đo pH`, `Liên kết cộng hóa trị`, `Liên kết ion`.

```cmd
curl -X POST http://localhost:8000/api/v1/jobs -H "Content-Type: application/json" -d "{\"query\": \"Thang đo pH\"}"
```

### 3.2. Kiểm tra trạng thái Job
Sử dụng ID trả về từ bước 3.1:
```cmd
curl -X GET http://localhost:8000/api/v1/jobs/<job_id>
```

### 3.3. Xem Video
Khi Job có status `COMPLETED`, bạn có thể lấy thuộc tính `artifact_path` và truy cập trực tiếp bằng trình duyệt để tải về:
```text
http://localhost:8000/static/videos/<job_id>.mp4
```

## 4. Architecture Note (Thiết kế hệ thống)

**Vòng đời Job (Job Lifecycle):**
Hệ thống quản lý Job qua 3 trạng thái chính (State Machine):
- `PENDING`: Ngay sau khi API trả về HTTP 202. Job được ghi nhận và đẩy vào `BackgroundTasks`.
- `PROCESSING`: Job bắt đầu được AI xử lý. Nếu AI sinh nội dung rác (Hallucination), module `AIVideoGenerator` sẽ tự động Retry tối đa 3 lần.
- `COMPLETED`: Xử lý thành công. Pipeline ghép nối Video đã hoàn tất.
- `FAILED`: Xử lý thất bại sau khi hết số lần thử hoặc có ngoại lệ hệ thống.

**Ranh giới Lưu trữ (Storage Boundaries):**
- **In-Memory Repository:** Metadata của Job (ID, trạng thái, query) được lưu tạm trong bộ nhớ (RAM). Dữ liệu này sẽ mất khi restart server.
- **File System (Disk):** Các Video (`.mp4`) sinh ra được lưu trực tiếp trên ổ cứng tại thư mục `/static/videos/`. Nếu server thiếu `ffmpeg`, luồng xử lý I/O vẫn được đảm bảo nhờ cơ chế sinh file dự phòng (Dummy hex signature).
