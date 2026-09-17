# Implementation - 01_PERSISTENCE

## Danh sách file đã tạo/sửa
1. `src/models/job.py`: Chứa class `Job` và enum `JobStatus` sử dụng Pydantic v2.
2. `src/repositories/job_repository.py`: Định nghĩa abstract class `JobRepository` và implement `InMemoryJobRepository` với các hàm CRUD.
3. `src/main.py`: Khởi tạo app FastAPI và route cơ bản.

## Dependency Injection
- Do chưa yêu cầu implement endpoint sử dụng DI trong ticket này, chúng ta chỉ mới khai báo models và repositories.

## Ghi chú
- Code tuân thủ strict type hint và sử dụng Pydantic v2 validation.
