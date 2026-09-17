# Hướng dẫn Test tay (Manual Test) - 03_AI-CORE-RETRY

Tài liệu này hướng dẫn người dùng cách kiểm tra tính năng Guardrails (chặn Ảo giác) và cơ chế tự động Retry của AI bằng cách can thiệp nhẹ vào mã nguồn để ép AI luôn trả về kết quả sai.

## 1. Kịch bản 1: AI hoạt động hoàn hảo (Happy Path)
Trạng thái mặc định: Hàm giả lập AI hiện tại luôn trả về kết quả chứa từ khóa hóa học (`oxi hóa khử`), do đó sẽ Pass ngay từ lần thử đầu tiên.

**Bước 1:** Khởi chạy server:
```bash
uvicorn src.main:app --reload
```

**Bước 2:** Bắn request:
```cmd
curl -X POST http://localhost:8000/api/v1/jobs -H "Content-Type: application/json" -d "{\"query\": \"Giải thích phản ứng Oxi hóa khử\"}"
```

**Bước 3:** Kiểm tra Log Terminal
- Bạn sẽ thấy Job chạy mượt mà, gọi qua `AIVideoGenerator` và kết thúc bằng `COMPLETED` mà không có lỗi nào được log ra.

## 2. Kịch bản 2: AI bị ảo giác (Fail liên tục 3 lần -> FAILED)
Đây là cách tốt nhất để test vòng lặp Retry.

**Bước 1: Chỉnh sửa mã nguồn giả lập lỗi**
Mở file `src/ai/video_generator.py`, tìm hàm `_mock_ai_call` và sửa dòng return thành chuỗi không chứa từ khóa hóa học:
```python
    async def _mock_ai_call(self, query: str) -> str:
        await asyncio.sleep(2)
        # ÉP LỖI: Trả về chuỗi rác không có từ khóa Hóa học
        return f"Một kịch bản về Toán học và Ngữ văn." 
```

**Bước 2:** Lưu file (Uvicorn sẽ tự động reload).

**Bước 3:** Bắn lại request:
```cmd
curl -X POST http://localhost:8000/api/v1/jobs -H "Content-Type: application/json" -d "{\"query\": \"Giải thích phản ứng Oxi hóa khử\"}"
```

**Bước 4:** Quan sát Terminal Log
Bạn sẽ thấy rõ ràng quá trình AI cố gắng tự phục hồi 3 lần trước khi bỏ cuộc:
```text
WARNING:src.ai.video_generator:AI generation failed on attempt 1/3: Output does not contain chemistry keywords (Hallucination detected)
WARNING:src.ai.video_generator:AI generation failed on attempt 2/3: Output does not contain chemistry keywords (Hallucination detected)
WARNING:src.ai.video_generator:AI generation failed on attempt 3/3: Output does not contain chemistry keywords (Hallucination detected)
```

**Bước 5:** Lấy ID Job vừa gửi ở Bước 3, kiểm tra status:
```cmd
curl -X GET http://localhost:8000/api/v1/jobs/<id_cua_ban>
```
*Kỳ vọng:* Hệ thống tự động catch lỗi ở nỗ lực cuối cùng và bảo vệ an toàn cho State Machine bằng cách đưa Job về trạng thái `"status": "FAILED"`, `"error_message": "Output does not contain chemistry keywords..."*.

> **Ghi chú:** Sau khi test xong, đừng quên sửa lại file `video_generator.py` về nguyên bản nhé!
