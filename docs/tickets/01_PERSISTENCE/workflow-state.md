# Workflow State — 01_PERSISTENCE (#01)

> 📌 **Nguồn Sự Thật Tiến Độ (LITE VERSION):** Dù đã cắt giảm các bước DevOps rườm rà cho Prototype, bảng tiến độ này vẫn phải được track cực kỳ chi tiết để chống AI mất bối cảnh (Anti-Drift). Trước khi làm bước tiếp theo hoặc khi resume session, BẮT BUỘC đọc file này.

**Ticket:** #01 — 01_PERSISTENCE — Khởi tạo Project FastAPI & Thiết kế Ranh giới Lưu trữ (Persistence)
**Branch:** main
**Cập nhật lần cuối:** 2026-09-17 20:50

## Tiến độ theo usage.md (Micro-Checklist)

| Bước | Mô tả chi tiết | Trạng thái | File output | Ngày xong |
|---|---|---|---|---|
| **0.1** | Sync Git (Pull main, tạo nhánh `feature/...`) | ⬜ pending | Local Repo | |
| **1.1** | Phân tích yêu cầu & Bóc tách Acceptance Criteria (AC) | ✅ done | `docs/tickets/01_PERSISTENCE/requirements.md` | 2026-09-17 |
| **1.2** | Thiết kế Pydantic Schemas (Request/Response) | ⏳ in_progress | `docs/tickets/01_PERSISTENCE/design.md` | |
| **1.3** | Thiết kế luồng xử lý Asynchronous (Background Task) | ⏳ in_progress | *Ghi chung vào design.md* | |
| **2.1** | Setup Thư mục, File & Dependency Injection (Depends) | ⬜ pending | `docs/tickets/01_PERSISTENCE/implementation.md` | |
| **2.2** | Triển khai Logic API & Background Task gọi LLM | ⬜ pending | *Mã nguồn Python* | |
| **2.3** | Bắt Exception & Quản lý State (FAILED/COMPLETED) | ⬜ pending | *Mã nguồn Python* | |
| **3.1** | Audit Type Hints (Mypy/Ruff) | ⬜ pending | `docs/tickets/01_PERSISTENCE/testing.md` | |
| **3.2** | Viết Pytest & Mocking (AsyncMock) External APIs | ⬜ pending | `tests/test_...py` | |
| **4.1** | Kiểm tra & Cập nhật `requirements.txt` | ⬜ pending | `requirements.txt` | |
| **4.2** | Viết lệnh cURL mẫu & Hướng dẫn khởi chạy | ⬜ pending | `README.md` (root) | |
| **4.3** | Git Commit & Tạo Merge Request (MR) | ⬜ pending | Repo GitHub | |

**Quy ước trạng thái:** `⬜ pending` -> `⏳ in_progress` -> `✅ done`
Chỉ đánh `✅ done` khi **đã lưu file output** VÀ **user đã confirm** hạng mục đó.

## Ghi chú gián đoạn (Điền khi task bị ngắt giữa chừng)
- Lần cuối làm tới: Hoàn thành thiết kế Bước 1, đang chờ User Confirm.
- Việc cần làm tiếp theo: Nhận lệnh "Confirm" để chuyển sang Bước 2 (Implementation).
- Lưu ý/blocker còn tồn đọng: Chưa.
