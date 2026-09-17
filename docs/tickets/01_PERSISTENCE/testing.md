# Testing Plan - 01_PERSISTENCE

## 1. Mục tiêu kiểm thử (Test Objectives)
- Đảm bảo tính toàn vẹn của Pydantic schema `Job` và các trạng thái `JobStatus`.
- Kiểm tra các hàm CRUD của `InMemoryJobRepository` có hoạt động chính xác hay không (create, get, update, list).
- Đảm bảo app FastAPI khởi tạo thành công và endpoint `/health` trả về kết quả đúng (`200 OK`).

## 2. Các kịch bản kiểm thử (Test Cases)
1. `test_in_memory_repository_create`: Job mới phải được tạo ra thành công với status mặc định là `PENDING`.
2. `test_in_memory_repository_get`: Lấy một Job bằng ID. Nếu ID không tồn tại, trả về `None`.
3. `test_in_memory_repository_update`: Cập nhật trạng thái của Job và xác minh lưu trữ đã được cập nhật. Nếu Job không tồn tại, phải ném ra ngoại lệ `ValueError`.
4. `test_in_memory_repository_list`: Liệt kê toàn bộ Job hiện có trong repo.
5. `test_health_check`: Gọi API `/health` qua TestClient, kỳ vọng status `200` và body JSON.

## 3. Mocking & External APIs
- Trong phạm vi ticket `01_PERSISTENCE`, chúng ta chưa tích hợp thư viện gọi API bên ngoài (OpenAI/Video Gen). Do đó, phần Mocking bằng `AsyncMock` hiện tại là N/A (Out of scope).

## 4. Kết quả thực thi
- Lệnh chạy: `pytest`
- Số lượng test: 6 tests chạy thành công.
- Tỷ lệ passed: 100%.
- Kiểm tra Typing: Đã audit bằng mắt và tất cả các hàm đều có type hints.
