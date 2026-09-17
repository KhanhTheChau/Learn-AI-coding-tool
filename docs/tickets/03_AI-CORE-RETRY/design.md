# Architecture & AI Core Design - 03_AI-CORE-RETRY

## 1. Mục tiêu (Objective)
Cung cấp một service wrapper (`AIVideoGenerator`) đóng vai trò giao tiếp (mock) với External AI APIs. Đảm bảo nội dung trả về là chính xác (thông qua validation từ khóa Hóa học) và có cơ chế tự phục hồi (Retry) khi có lỗi.

## 2. Kiến trúc & Logic

### 2.1. Thư mục & File
- Tạo thư mục con: `src/ai/`
- Tạo file: `src/ai/video_generator.py`

### 2.2. Hàm Validation: `validate_chemistry_keywords(output: str)`
- **Nhiệm vụ:** Chống AI "ảo giác" (Hallucination) hoặc trả về nội dung không liên quan.
- **Logic:**
  - Định nghĩa 1 danh sách các từ khóa Hóa học cơ bản (VD: `["oxi", "khử", "electron", "phản ứng", "axit", "bazơ", "muối", "nguyên tử"]`).
  - Kiểm tra xem chuỗi `output` có chứa ít nhất 1 từ khóa trong tập trên hay không (case-insensitive).
  - Nếu không chứa: `raise ValueError("Output does not contain chemistry keywords (Hallucination detected)")`.

### 2.3. Class `AIVideoGenerator`
- **Phương thức `async def _mock_ai_call(self, query: str) -> str`**: 
  - Mô phỏng quá trình gọi LLM (`asyncio.sleep(2)`).
  - Trả về một kịch bản giả lập (ví dụ: f"Kịch bản về {query} với các phản ứng oxi hóa khử.").
- **Phương thức chính `async def generate_with_retry(self, query: str, max_retries: int = 3) -> str`**:
  - Khởi tạo vòng lặp `for attempt in range(max_retries):`.
  - Trong vòng lặp, bọc bằng `try...except Exception as e`.
  - Gọi `_mock_ai_call()`, sau đó gọi `validate_chemistry_keywords()` trên kết quả.
  - Nếu thành công, return kết quả luôn (break vòng lặp).
  - Nếu thất bại và `attempt < max_retries - 1`, log cảnh báo (Warning) và tiếp tục lặp.
  - Nếu thất bại ở vòng lặp cuối (attempt 3), dùng lệnh `raise` để đẩy Exception ra ngoài.

### 2.4. Tích hợp vào Background Task hiện tại
- **File:** `src/services/video_service.py` và `src/routers/job_router.py`
- Sửa hàm `process_video_job`: 
  - Khai báo tham số `ai_gen: AIVideoGenerator` được truyền từ Router vào.
  - Thay vì gọi `await asyncio.sleep(5)`, sẽ gọi `await ai_gen.generate_with_retry(job.query)`.
  - Nếu `generate_with_retry` ném Exception (sau khi đã thử lại 3 lần mà vẫn thất bại), block `except Exception as e:` đang có sẵn ở Ticket 02 sẽ tự động catch và chuyển trạng thái Job thành `FAILED`.
- Trong Router: Sử dụng Dependency Injection (`Depends()`) để tiêm `AIVideoGenerator` vào endpoint `POST /jobs` và truyền cho hàm `process_video_job`.

## 3. Testing Strategy
- Viết Unit Test cho `validate_chemistry_keywords` (Test case chứa từ khóa -> Pass, không chứa -> Raise Error).
- Viết Unit Test cho `generate_with_retry`:
  - Dùng `AsyncMock` để patch `_mock_ai_call` trả về kết quả sai 2 lần đầu và đúng ở lần 3 -> Check số lần gọi là 3 và hàm chạy thành công.
  - Dùng `AsyncMock` trả về kết quả sai cả 3 lần -> Check hàm bắn ra Exception hợp lệ.
