# AI Chemistry Video Service (Prototype)

## Giới thiệu
Đây là bản nguyên mẫu (Prototype) Backend cho dịch vụ tạo video AI giáo dục (môn Hóa học). Hệ thống cung cấp API RESTful cho phép người dùng gửi yêu cầu giải thích một khái niệm, sau đó xử lý ngầm (background job) để tạo video và trả về kết quả mà không làm nghẽn (block) luồng chính.

## Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.10+
- **Framework:** FastAPI, Pydantic v2
- **Server:** Uvicorn
- **Testing:** Pytest

## Cấu trúc tài liệu & Đánh giá (Dành cho AI Reviewer)
Dự án này được thiết kế để các hệ thống AI khác có thể dễ dàng đọc, hiểu và chấm điểm.
- **Yêu cầu gốc:** Xem `docs/TALOTRACE_CHALLENGE.md`
- **Tiêu chuẩn Kiến trúc & Chấm điểm:** Xem `architecture.md` (Tiêu chí đánh giá tính nhất quán, hiệu suất).
- **Quy tắc Coding:** Xem `ai-chemistry-backend-rules.md`.

## Hướng dẫn chạy thử (Local)
### 1. Setup môi trường
```bash
pip install -r requirements.txt
```

### 2. Khởi chạy server
```bash
uvicorn src.main:app --reload
```
Server sẽ chạy tại `http://localhost:8000`. Kiểm tra API Health Check:
```bash
curl http://localhost:8000/health
```

### 3. API Tham khảo
Lệnh cURL mẫu để Submit Video Job:
```bash
curl -X POST http://localhost:8000/api/v1/jobs -H "Content-Type: application/json" -d "{\"query\": \"Giải thích phản ứng Oxi hóa khử\"}"
```

Lệnh cURL mẫu để Check Status Job:
```bash
curl -X GET http://localhost:8000/api/v1/jobs/{job_id}
```
