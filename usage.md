# Hướng dẫn sử dụng Multi-Agent Workflow (AI Chemistry - LITE VERSION)

> 📌 **Tối ưu hóa Quota (Prototype):** Phiên bản này đã cắt bỏ các khâu CI/CD rườm rà (Git Branch, Docker, MR, Release Note). Tuy nhiên, **chất lượng phân tích và triển khai code vẫn phải giữ nguyên độ chi tiết và nghiêm ngặt** để đảm bảo sản phẩm hoạt động hoàn hảo.

---

## 1. Cơ chế Anti-Drift (Bắt Buộc)

Khi xử lý một chức năng, Agent rất dễ bị "ảo giác" (hallucinate) hoặc quên bối cảnh do giới hạn context window. Vì vậy:
1. **Khởi tạo trạng thái:** Ngay khi nhận yêu cầu, copy `docs/templates/workflow-state.md` thành `docs/tickets/[ticket-number]_[TICKET-ID]/workflow-state.md`.
2. **Cập nhật liên tục:** Đánh dấu `✅ done` vào file này ngay sau mỗi bước hoàn thành.
3. **Đọc trước khi làm:** Nếu session bị ngắt quãng, Agent phải tự giác đọc lại file trạng thái này trước khi tiếp tục code, không tự ý đoán tiến độ.

---

## 2. Quy trình 4 Bước Cốt Lõi (Chi tiết)

### Bước 1: Phân tích & Thiết kế Kiến trúc (Senior BA & Architect)
**Mục tiêu:** Hiểu rõ yêu cầu và chốt hạ toàn bộ kiến trúc & API Contract trước khi viết code.
**Chi tiết công việc:**
1. Đọc yêu cầu từ user hoặc từ file `TALOTRACE_CHALLENGE.md`. Trích xuất các Acceptance Criteria (AC) rõ ràng.
2. Thiết kế Request/Response Schemas sử dụng Pydantic v2 (Strict Type).
3. Thiết kế luồng xử lý Asynchronous (ví dụ: Tạo Job -> Trả 202 Accepted -> Background Task xử lý).
4. **Output:** Ghi toàn bộ thiết kế vào `docs/tickets/[ticket-number]_[TICKET-ID]/design.md` (dựa trên file template).
5. **Dừng lại:** Trình bày tóm tắt cho user và chờ user gõ "Confirm" để đi tiếp.

### Bước 2: Triển khai Code & Business Logic (Senior Dev)
**Mục tiêu:** Viết code FastAPI sạch, tuân thủ Layered Architecture (Router -> Service -> Repository).
**Chi tiết công việc:**
1. **Setup File:** Tạo các file router, service, schemas tương ứng trong thư mục `src/`.
2. **Dependency Injection:** Sử dụng `Depends()` của FastAPI để tiêm Repository/Service vào Router. Không dùng global dict state cứng gán trực tiếp trong file logic.
3. **Background Tasks:** Sử dụng `fastapi.BackgroundTasks` hoặc `asyncio` để xử lý việc gọi LLM/Video Generator, đảm bảo API chính không bị block (chặn thread).
4. **Xử lý Exception:** Bắt các lỗi có thể xảy ra (timeout LLM, data sai) và cập nhật State của Job thành `FAILED` kèm message lỗi thay vì crash app.
5. **Output:** Ghi danh sách file đã tạo/sửa vào `docs/tickets/[ticket-number]_[TICKET-ID]/implementation.md`.
6. **Dừng lại:** Chờ user "Confirm" trước khi sang bước Test.

### Bước 3: Kiểm thử & Quality Assurance (Senior QA & QC)
**Mục tiêu:** Đảm bảo code chạy đúng AC mà không cần UI.
**Chi tiết công việc:**
1. **Linting & Typing:** Chạy Ruff / Mypy (hoặc Audit code bằng mắt) để đảm bảo 100% hàm có type hint chuẩn xác.
2. **Unit Test:** Viết Pytest trong thư mục `tests/`. Sử dụng `fastapi.testclient.TestClient`.
3. **Mocking:** BẮT BUỘC mock các hàm gọi External API (OpenAI, thư viện xử lý video nặng) bằng `unittest.mock.AsyncMock` để test chạy nhanh và không tốn tiền API thật.
4. **Output:** Ghi test plan vào `docs/tickets/[ticket-number]_[TICKET-ID]/testing.md`. Chạy thử lệnh `pytest` (nếu user cho phép) để xác thực.
5. **Dừng lại:** Chờ user "Confirm".

### Bước 4: Hướng dẫn chạy & Bàn giao (Senior DevOps)
**Mục tiêu:** Cập nhật Document, lưu vết Git và chuẩn bị Merge Request.
**Chi tiết công việc:**
1. Kiểm tra và bổ sung các thư viện mới vào `requirements.txt`.
2. Viết/Cập nhật file `README.md` tại thư mục gốc. Bắt buộc phải có:
   - Lệnh setup môi trường (`pip install -r requirements.txt`).
   - Lệnh khởi chạy server (`uvicorn src.main:app --reload`).
   - Lệnh cURL mẫu để Submit Video Job.
   - Lệnh cURL mẫu để Check Status Job.
3. **Commit & Tạo MR (Merge Request):** Khi code đã pass mọi bài test, thực hiện commit code theo chuẩn Conventional Commits (ví dụ: `feat(#ticket-id): add job pipeline`) và hướng dẫn user cách đẩy code/mở MR tự động.
4. Chờ user "Confirm" để hoàn tất Ticket.

---

## 3. Checklist Nhanh (FastAPI Context)

| Vai trò | Checklist kiểm tra chéo |
| :--- | :--- |
| **Architect** | State Machine của Job có đủ 4 trạng thái (PENDING, PROCESSING, COMPLETED, FAILED) không? |
| **Dev** | Endpoint `POST` có trả về HTTP 202 ngay lập tức thay vì bắt user đợi LLM xử lý xong không? |
| **Dev** | Không sử dụng `time.sleep()` trong thread chính của FastAPI. Phải dùng `await asyncio.sleep()`. |
| **QA** | Coverage của Pytest đã bao phủ luồng FAILED khi LLM throw exception chưa? |
| **DevOps**| Lệnh cURL trong README có kèm header `Content-Type: application/json` chưa? |
