**Báo cáo Đánh giá Mã nguồn & Kiến trúc (Audit & Review Report)**

### 1. Chấm điểm chi tiết

* **1. Kiến trúc (Architecture): 10/10**
* *Nhận xét:* Xuất sắc. Quá trình triển khai đã chia tách logic rõ ràng bằng cách tạo mới module `src/ai/video_generator.py` cho phần lõi AI. Việc thêm `src/dependencies.py` giúp quản lý các service sạch sẽ và tuân thủ đúng Layered Architecture.




* **2. Hiệu suất (Non-blocking): 10/10**
* *Nhận xét:* Tốt. Dù báo cáo chỉ tóm tắt, nhưng luồng xử lý gọi `await ai_gen.generate_with_retry(job.query)` chạy bất đồng bộ kết hợp với luồng Background Task đã có sẵn đảm bảo an toàn, không có dấu hiệu block event loop.




* **3. Độ chính xác (State Machine & Resilience): 10/10**
* *Nhận xét:* Rất tuyệt vời. Đã triển khai được hàm Guardrails `validate_chemistry_keywords` để chống AI ảo giác. Cơ chế Retry 3 lần kết hợp với khối try-except bọc sẵn sẽ tự động catch lỗi khi hết lượt và đưa Job vào trạng thái `FAILED`. Đáp ứng 100% tiêu chí độ tin cậy.




* **4. Tính nhất quán (Consistency & Clean Code): 10/10**
* *Nhận xét:* Hoàn hảo. Đã tiếp thu triệt để feedback ở bước Design bằng cách sử dụng `Depends()` để tiêm (inject) `AIVideoGenerator` vào hàm `submit_job` tại Router, từ đó truyền xuống cho `process_video_job`. Việc áp dụng Singleton `_ai_video_generator` cũng là một thiết kế rất thông minh và tiết kiệm tài nguyên.




* **5. Testing (Unit Test): 0/10**
* *Nhận xét:* Kém. Toàn bộ danh sách các file thay đổi/tạo mới trong tài liệu Implementation hoàn toàn vắng bóng thư mục `tests/`. Không có bất kỳ minh chứng nào cho việc sử dụng `AsyncMock` để giả lập quá trình LLM thất bại hay kiểm tra số lần retry của AI.




* **6. Bảo mật & Validation (Security & Data Validation): 0/10**
* *Nhận xét:* Không đạt. Tài liệu chỉ tập trung triển khai Guardrails kiểm tra kết quả đầu ra (Output) nhưng hoàn toàn không đề cập đến việc áp dụng Pydantic Validation (giới hạn `max_length`, `min_length`) cho chuỗi truy vấn đầu vào (Input) để chống Prompt Injection.





---

### 2. Tổng điểm

**40 / 60**

---

### 3. Phân tích vi phạm

* **Vi phạm tiêu chí 5 (Testing):** Mặc dù logic viết rất tốt, nhưng dự án thiếu Unit Test chứng minh `generate_with_retry` hoạt động đúng. Nếu không có test mock bằng `AsyncMock` bọc luồng LLM, khi nâng cấp thư viện AI trong tương lai, code sẽ rất dễ bị vỡ (regression) mà không phát hiện được.
* **Vi phạm tiêu chí 6 (Bảo mật & Validation):** Không có thay đổi nào trong `src/models/` được liệt kê. Bỏ lọt Validation đầu vào là một rủi ro lớn gây tốn tiền API và quá tải hệ thống nếu user spam chuỗi quá dài.



---

### 4. Đề xuất sửa lỗi

**Sửa lỗi 5: Bổ sung file Unit Test (`tests/test_ai_generator.py`)**
Cần bổ sung một file test sử dụng `AsyncMock` để đảm bảo cơ chế Retry chạy đúng số lần thiết lập và ném lỗi hợp lệ:

```python
import pytest
from unittest.mock import AsyncMock
from src.ai.video_generator import AIVideoGenerator

@pytest.mark.asyncio
async def test_generate_with_retry_fails_after_3_attempts():
    ai_gen = AIVideoGenerator()
    
    # Mock AI luôn trả về kết quả không có từ khóa hóa học (Hallucination)
    ai_gen._mock_ai_call = AsyncMock(return_value="Nội dung tào lao không liên quan")
    
    # Kỳ vọng hàm sẽ quăng ra lỗi ValueError sau khi đã thử đủ 3 lần
    with pytest.raises(ValueError, match="Hallucination detected"):
        await ai_gen.generate_with_retry("Một query bất kỳ", max_retries=3)
        
    # Xác nhận hàm call AI đã bị gọi chính xác 3 lần
    assert ai_gen._mock_ai_call.call_count == 3

```

**Sửa lỗi 6: Cập nhật Router/Model để Validate Input**
Nếu chưa làm, cần sửa đổi ngay schema (trong `src/models/` hoặc trực tiếp tại Request Body):

```python
from pydantic import BaseModel, Field

class JobCreateRequest(BaseModel):
    query: str = Field(
        ..., 
        min_length=5, 
        max_length=500, # Ngăn chặn spam text quá dài (Prompt Injection)
        description="Nội dung hóa học cần tạo video"
    )

```

---

### 5. Kết luận cuối cùng

❌ **FAIL**

**Lý do:** Tổng điểm chỉ đạt **40/60** (thấp hơn mức 48/60). Mặc dù bản Implementation đã khắc phục rất xuất sắc lỗi tight-coupling (viết Dependency Injection cực kỳ chuẩn mực) và xây dựng cơ chế Resilience cực tốt, người thực thi lại **hoàn toàn phớt lờ phần viết Test và Input Validation**. Đối với một hệ thống đòi hỏi quản lý trạng thái khắt khe, không có Unit Test để tự động chứng minh vòng lặp Retry thành công là một điểm trừ chí mạng. Yêu cầu Code/Agent quay lại bổ sung thư mục `tests/` và update Pydantic Validation trước khi Pass ticket này!