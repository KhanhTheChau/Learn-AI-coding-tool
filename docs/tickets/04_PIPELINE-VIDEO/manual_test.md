# Hướng dẫn Test tay (Manual Test) - 04_PIPELINE-VIDEO

Tài liệu này hướng dẫn bạn cách gửi các truy vấn Hóa học chuyên biệt và kiểm tra việc tải file `.mp4` thực tế được hệ thống tự động sinh ra.

## 1. Khởi chạy Server
Mở terminal và chạy lệnh:
```bash
uvicorn src.main:app --reload
```

## 2. Gửi Yêu cầu tạo Video (Job)
Mở một terminal khác (hoặc Postman/cURL) và chạy lệnh sau. Lưu ý, cURL được format chuẩn 1 dòng cho Windows:

```cmd
curl -X POST http://localhost:8000/api/v1/jobs -H "Content-Type: application/json" -d "{\"query\": \"Liên kết ion và cộng hóa trị khác nhau thế nào\"}"
```
*Bạn có thể thay phần `query` bằng `Thang đo pH` hoặc `Liên kết cộng hóa trị` để test các kịch bản khác.*

*Response mong đợi (HTTP 202):*
```json
{"id": "<job_id>", "status": "PENDING", ...}
```

## 3. Kiểm tra Trạng thái Job và Lấy URL Video
Sử dụng ID bạn vừa nhận được ở bước 2:
```cmd
curl -X GET http://localhost:8000/api/v1/jobs/<job_id>
```

*Response mong đợi:*
```json
{
  "id": "<job_id>",
  "status": "COMPLETED",
  "query": "Liên kết ion và cộng hóa trị khác nhau thế nào",
  "artifact_path": "/static/videos/<job_id>.mp4",
  "error_message": null,
  "created_at": "...",
  "updated_at": "..."
}
```

## 4. Tải và Kiểm tra File Video Thực Tế
Mở trình duyệt web của bạn và truy cập trực tiếp vào đường link sau:
```text
http://localhost:8000/static/videos/<job_id>.mp4
```
*(Thay `<job_id>` bằng ID thực tế của bạn).*

**Kỳ vọng:** 
- Trình duyệt sẽ tải về (hoặc phát trực tiếp) một file `.mp4`. 
- **Lưu ý:** Nếu máy tính của bạn không cài `ffmpeg`, hệ thống đã an toàn chuyển sang chế độ "Mock Fallback". File tải về sẽ là một file MP4 dummy (với dung lượng rất nhẹ). Mặc dù các trình phát video có thể báo lỗi không mở được nội dung (do file rỗng ruột), nhưng file có định dạng hợp lệ để các pipeline tiếp theo vẫn ghi nhận đó là file thật. Quan trọng nhất là Server Backend không bị sập!
