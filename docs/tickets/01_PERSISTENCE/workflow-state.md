# Workflow State — 01_PERSISTENCE (#01)

> 📌 **Nguồn Sự Thật Tiến Độ (LITE VERSION):** Dù đã cắt giảm các bước DevOps rườm rà cho Prototype, bảng tiến độ này vẫn phải được track cực kỳ chi tiết để chống AI mất bối cảnh (Anti-Drift). Trước khi làm bước tiếp theo hoặc khi resume session, BẮT BUỘC đọc file này.

**Ticket:** #01 — 01_PERSISTENCE — Khởi tạo Project FastAPI & Thiết kế Ranh giới Lưu trữ (Persistence)
**Branch:** main
**Cập nhật lần cuối:** 2026-09-17 20:50

## Tiến độ theo usage.md (Micro-Checklist)

| Bước | Mô tả chi tiết | Trạng thái | File output | Ngày xong |
|---|---|---|---|---|
| **0.1** | Sync Git (Pull main, tạo nhánh `feature/...`) | ✅ done | Local Repo | 2026-09-17 |
| **1.1** | Phân tích yêu cầu & Bóc tách Acceptance Criteria (AC) | ✅ done | `docs/tickets/01_PERSISTENCE/requirements.md` | 2026-09-17 |
| **1.2** | Thiết kế Pydantic Schemas (Request/Response) | ✅ done | `docs/tickets/01_PERSISTENCE/design.md` | 2026-09-17 |
| **1.3** | Thiết kế luồng xử lý Asynchronous (Background Task) | ✅ done | *Ghi chung vào design.md* | 2026-09-17 |
| **2.1** | Setup Thư mục, File & Dependency Injection (Depends) | ✅ done | `docs/tickets/01_PERSISTENCE/implementation.md` | 2026-09-17 |
| **2.2** | Triển khai Logic API & Background Task gọi LLM | ✅ done | *(Out of scope)* | 2026-09-17 |
| **2.3** | Bắt Exception & Quản lý State (FAILED/COMPLETED) | ✅ done | *(Out of scope)* | 2026-09-17 |
| **3.1** | Audit Type Hints (Mypy/Ruff) | ✅ done | `docs/tickets/01_PERSISTENCE/testing.md` | 2026-09-17 |
| **3.2** | Viết Pytest & Mocking (AsyncMock) External APIs | ✅ done | `tests/test_...py` | 2026-09-17 |
| **4.1** | Kiểm tra & Cập nhật `requirements.txt` | ✅ done | `requirements.txt` | 2026-09-17 |
| **4.2** | Viết lệnh cURL mẫu & Hướng dẫn khởi chạy | ✅ done | `README.md` (root) | 2026-09-17 |
| **4.3** | Viết tài liệu Hướng dẫn Test tay (Manual Test) | ✅ done | `docs/tickets/01_PERSISTENCE/manual_test.md` | 2026-09-17 |
| **4.4** | Git Commit & Tạo Merge Request (MR) | ✅ done | Repo GitHub | 2026-09-17 |

**Quy ước trạng thái:** `⬜ pending` -> `⏳ in_progress` -> `✅ done`
Chỉ đánh `✅ done` khi **đã lưu file output** VÀ **user đã confirm** hạng mục đó.
**BẮT BUỘC:** Phải hoàn thành tích hết toàn bộ các bước mới được tạo MR code (Riêng các mục của Bước 4 cho phép đánh `✅ done` trước khi thực sự chạy lệnh Git Commit/MR).

## Ghi chú gián đoạn (Điền khi task bị ngắt giữa chừng)
- Lần cuối làm tới: Hoàn thành toàn bộ ticket. Ticket 01_PERSISTENCE đã xong.
- Việc cần làm tiếp theo: Bắt đầu Ticket #02.
- Lưu ý/blocker còn tồn đọng: Không có.
