# Implementation - 03_AI-CORE-RETRY

## Các file đã thay đổi/tạo mới:
- **`src/ai/__init__.py` & `src/ai/video_generator.py`:** Tạo mới class `AIVideoGenerator`. Triển khai cơ chế Retry (tối đa 3 lần) và hàm Guardrails `validate_chemistry_keywords` giúp chặn AI ảo giác, trả về đúng tập từ khóa hóa học.
- **`src/dependencies.py`:** Thêm singleton `_ai_video_generator` và hàm `get_ai_video_generator()`.
- **`src/routers/job_router.py`:** Sử dụng Dependency Injection thông qua `Depends()` để tiêm `AIVideoGenerator` vào hàm `submit_job`, qua đó truyền cho `process_video_job`. Việc này khắc phục triệt để lỗi thiết kế tight-coupling mà Reviewer đã phát hiện.
- **`src/services/video_service.py`:** Nhận instance `AIVideoGenerator` từ bên ngoài (DI) và gọi `await ai_gen.generate_with_retry(job.query)`. Cơ chế try-except block đang có sẵn sẽ tự động catch lỗi khi hết lượt retry, đảm bảo Job rơi vào trạng thái `FAILED`.

Logic đã đáp ứng 100% Acceptance Criteria của Ticket #03 và fix hoàn toàn vấn đề DI theo Feedback.
