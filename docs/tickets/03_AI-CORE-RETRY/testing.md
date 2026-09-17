# Testing Plan - 03_AI-CORE-RETRY

## 1. Mục tiêu (Objective)
Đảm bảo cơ chế AI Guardrails (chặn Hallucination) và cơ chế tự phục hồi (Retry) hoạt động chính xác thông qua Unit Test. 

## 2. Kịch bản Test (Test Cases)
File: `tests/test_ai_generator.py`

### 2.1. Test Logic Validation (Đồng bộ)
- **`test_validate_chemistry_keywords_success`**: Đầu vào có từ khóa (`oxi`) -> Trả về `True`.
- **`test_validate_chemistry_keywords_failure`**: Đầu vào rác -> Bắn `ValueError("Hallucination detected")`.

### 2.2. Test Logic Retry (Bất đồng bộ - AsyncMock)
- **`test_generate_with_retry_fails_after_3_attempts`**:
  - Dùng `AsyncMock` ép `_mock_ai_call` luôn trả về chuỗi rác.
  - Kỳ vọng: Lặp đúng 3 lần (`call_count == 3`), và ném lỗi `ValueError` ra ngoài.
- **`test_generate_with_retry_succeeds_on_second_attempt`**:
  - Dùng `side_effect` của `AsyncMock` trả về chuỗi rác lần 1, chuỗi đúng lần 2.
  - Kỳ vọng: Hàm trả về thành công ở vòng lặp thứ 2, `call_count == 2`, không ném lỗi.

## 3. Lệnh chạy và Kết quả (Verification)
Chạy lệnh `pytest tests/test_ai_generator.py -v`.
Tất cả các case bắt buộc phải PASSED.
