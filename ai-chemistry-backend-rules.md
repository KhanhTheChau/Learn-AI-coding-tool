# Coding Rules & Debug - AI Chemistry Video Service Backend

Tài liệu này định nghĩa tiêu chuẩn lập trình và gỡ lỗi cho dự án Backend Prototype xây dựng bằng **FastAPI** và **Python 3.10+**.

## 1. Công nghệ & Framework
- **Core:** Python 3.10+, FastAPI, Pydantic v2.
- **Server:** Uvicorn.
- **Testing:** Pytest, httpx (cho TestClient).
- **Typing/Linting:** Strict Type Hints, Ruff (hoặc Flake8/Black).
- **Dependency Management:** Sử dụng `requirements.txt` làm chuẩn duy nhất để đảm bảo tính khả thi triển khai.

## 2. Cấu trúc Dự án
```
src/
├── api/          # FastAPI Routers
├── core/         # Config, Exceptions
├── models/       # Pydantic schemas
├── services/     # AI Video Generation Logic
├── repositories/ # Storage (In-memory/File)
└── main.py       # FastAPI entrypoint
tests/
```

## 3. Quy tắc Fix Bug / Debug
- **RCA Documentation:** Trước khi đổi code, luôn viết RCA (Root Cause Analysis). Đọc trực tiếp code router và traceback, không giả định.
- **Traceability:** Nếu gặp bug về async task (Job bị kẹt ở PROCESSING), kiểm tra ngay việc có sử dụng hàm blocking (như `time.sleep`) trong thread của asyncio hay không.
- **API Contracts:** Lỗi liên quan đến Validation Body/Query Parameter thường nằm ở khai báo Pydantic. Hãy kiểm tra các file `models/` trước khi check logic router.
- **Không "Swallow" Exception:** Khi fix bug do crash, không được bọc bằng `except Exception: pass`. Phải log lỗi và cập nhật state của Job thành `FAILED`.

## 4. Trạng thái Job Bắt buộc
Mỗi Job (Video Task) đi qua các trạng thái: `PENDING` -> `PROCESSING` -> `COMPLETED` (có artifact_path) hoặc `FAILED` (có error_message).
Bất kỳ bug fix nào cũng không được phá vỡ state machine này.
