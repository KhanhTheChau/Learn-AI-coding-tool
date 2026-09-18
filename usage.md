# Hướng dẫn sử dụng Multi-Agent Workflow (AI Chemistry - LITE VERSION)

> 📌 **Tối ưu hóa Quota (Prototype):** Phiên bản này đã cắt bỏ các khâu CI/CD rườm rà (Git Branch, Docker, MR, Release Note). Tuy nhiên, **chất lượng phân tích và triển khai code vẫn phải giữ nguyên độ chi tiết và nghiêm ngặt** để đảm bảo sản phẩm hoạt động hoàn hảo.

---

## 1. Cơ chế Anti-Drift (Bắt Buộc)

Khi xử lý một chức năng, Agent rất dễ bị "ảo giác" (hallucinate) hoặc quên bối cảnh do giới hạn context window. Vì vậy:
1. **Khởi tạo trạng thái:** Ngay khi nhận yêu cầu, copy `docs/templates/workflow-state.md` thành `docs/tickets/[ticket-number]_[TICKET-ID]/workflow-state.md`.
2. **Cập nhật liên tục:** Đánh dấu `✅ done` vào file này ngay sau mỗi bước hoàn thành.
3. **Đọc trước khi làm:** Nếu session bị ngắt quãng, Agent phải tự giác đọc lại file trạng thái này trước khi tiếp tục code, không tự ý đoán tiến độ.
4. **Quy tắc Dừng (STRICT STOP):** Tại cuối mỗi bước lớn (Bước 1, 2, 3, 4), Agent **TUYỆT ĐỐI KHÔNG ĐƯỢC** tự động làm tiếp. Agent **phải dừng lại**, trình bày kết quả và **chỉ được phép thực hiện bước tiếp theo khi User gõ chính xác chữ "Confirm"** (hoặc đồng ý rõ ràng). Dù User có nói "thực thi đi" nhưng chưa nghiệm thu bước hiện tại, Agent cũng phải hỏi lại để đảm bảo User đã review file output.
5. **Ghi nhận Lỗi & Cập nhật Memory (RCA):** Nếu có bất kỳ lỗi chung nào xảy ra trong quá trình thực thi (ví dụ: lỗi cấu hình, sai sót quy trình, anti-pattern) mà có khả năng lặp lại ở các ticket sau, Agent **PHẢI** lưu chi tiết lỗi và kết quả phân tích nguyên nhân (RCA) vào thư mục `.memory/` (tạo file markdown lưu kinh nghiệm) để hệ thống tự động học hỏi cho các phiên sau. Không tự ý đoán mò sửa lỗi khi chưa được Confirm.

---

## 2. Quy trình 4 Bước Cốt Lõi (Chi tiết)

### Bước 0: Chuẩn bị Môi trường (Git Sync)
**Mục tiêu:** Đảm bảo Agent làm việc trên nhánh độc lập, luôn lấy code mới nhất và không gây conflict.
**Chi tiết công việc:**
1. Chuyển về nhánh chính và cập nhật: `git checkout main` -> `git pull`.
2. Tạo và chuyển sang nhánh mới cho riêng ticket này: `git checkout -b feature/<ticket-number>-<ticket-id>`.

### Bước 1: Phân tích & Thiết kế Kiến trúc (Senior BA & Architect)
**Mục tiêu:** Hiểu rõ yêu cầu và chốt hạ toàn bộ kiến trúc & API Contract trước khi viết code. Đảm bảo kế thừa trọn vẹn tri thức từ các ticket trước.
**Chi tiết công việc:**
0. **[RẤT QUAN TRỌNG]:** BẮT BUỘC phải đọc file `.memory/tickets_requirements_snapshot.md` và `.memory/workflow_rules.md` để nắm được bức tranh tổng thể, kiến trúc Mock Mode Fallback, Audio gTTS, Pillow Caching và các Anti-patterns cần tránh. Nếu bỏ qua bước này, hệ thống sẽ gãy đổ.
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
3. Viết tài liệu Hướng dẫn Test tay (Manual Test) cho người dùng tại `docs/tickets/[ticket-number]_[TICKET-ID]/manual_test.md` (bao gồm các bước tương tác với API bằng cURL/Postman, cách check log, xác minh DB).
4. **Commit & Chuẩn bị MR (Merge Request):** Khi code đã pass mọi bài test:
   - **BẮT BUỘC:** Phải cập nhật file `workflow-state.md` thành `✅ done` cho tất cả các mục của Bước 4 (bao gồm cả mục 4.4 Git Commit) **TRƯỚC KHI** chạy lệnh commit.
   - Thực hiện add và commit code theo chuẩn Conventional Commits (ví dụ: `feat(#ticket-id): add job pipeline`).
   - Đẩy code lên GitHub (`git push -u origin <branch-name>`).
   - **BẮT BUỘC:** Cung cấp cho user **đường link tạo Pull Request** (xuất hiện trong log Terminal khi push).
   - **BẮT BUỘC:** Sinh ra phần **Nội dung (Description) của Pull Request** và bọc trong một khối code Markdown (` ```markdown `) ngay tại giao diện chat. Nội dung này phải có cấu trúc chuyên nghiệp (Tóm tắt, Các thay đổi chính, Checklist) để user chỉ việc ấn Copy và dán thẳng vào ô "Add a description" trên GitHub.
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
