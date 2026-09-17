# Workflow State — 05_RELEASE-DOCS (#05)

> 📌 **Nguồn Sự Thật Tiến Độ (LITE VERSION):** Dù đã cắt giảm các bước DevOps rườm rà cho Prototype, bảng tiến độ này vẫn phải được track cực kỳ chi tiết để chống AI mất bối cảnh (Anti-Drift). Trước khi làm bước tiếp theo hoặc khi resume session, BẮT BUỘC đọc file này.

**Ticket:** #05 — 05_RELEASE-DOCS — Hoàn thiện Logging, Viết tài liệu & Export Artifacts
**Branch:** main
**Cập nhật lần cuối:** 2026-09-17

## Tiến độ theo usage.md (Micro-Checklist)

| Bước | Mô tả chi tiết | Trạng thái | File output | Ngày xong |
|---|---|---|---|---|
| **0.1** | Sync Git (Pull main, tạo nhánh `feature/...`) | ⬜ pending | Local Repo | |
| **1.1** | Phân tích yêu cầu & Bóc tách Acceptance Criteria (AC) | ✅ done | `docs/tickets/05_RELEASE-DOCS/requirements.md` | 2026-09-17 |
| **1.2** | Thiết kế Pydantic Schemas (Request/Response) | ⬜ pending / N/A| *Ghi chung vào design.md* | |
| **1.3** | Thiết kế luồng xử lý Asynchronous (Background Task) | ⬜ pending / N/A| *Ghi chung vào design.md* | |
| **2.1** | Setup Thư mục, File & Dependency Injection (Depends) | ⬜ pending | `docs/features/05_RELEASE-DOCS/implementation.md` | |
| **2.2** | Triển khai Logic API & Background Task gọi LLM | ⬜ pending | *Mã nguồn Python* | |
| **2.3** | Bắt Exception & Quản lý State (FAILED/COMPLETED) | ⬜ pending | *Mã nguồn Python* | |
| **3.1** | Audit Type Hints (Mypy/Ruff) | ⬜ pending | `docs/testing/05_RELEASE-DOCS/testing.md` | |
| **3.2** | Viết Pytest & Mocking (AsyncMock) External APIs | ⬜ pending | `tests/test_...py` | |
| **4.1** | Kiểm tra & Cập nhật `requirements.txt` | ⬜ pending | `requirements.txt` | |
| **4.2** | Viết lệnh cURL mẫu & Hướng dẫn khởi chạy | ⬜ pending | `README.md` (root) | |
| **4.3** | Viết tài liệu Hướng dẫn Test tay (Manual Test) | ⬜ pending | `docs/tickets/05_RELEASE-DOCS/manual_test.md` | |
| **4.4** | Git Commit & Tạo Merge Request (MR) | ⬜ pending | Repo GitHub | |

**Quy ước trạng thái:** `⬜ pending` -> `⏳ in_progress` -> `✅ done`
Chỉ đánh `✅ done` khi **đã lưu file output** VÀ **user đã confirm** hạng mục đó.
**BẮT BUỘC:** Phải hoàn thành tích hết toàn bộ các bước mới được tạo MR code (Riêng các mục của Bước 4 cho phép đánh `✅ done` trước khi thực sự chạy lệnh Git Commit/MR).

## Ghi chú gián đoạn (Điền khi task bị ngắt giữa chừng)
- Lần cuối làm tới: [Tạo requirement]
- Việc cần làm tiếp theo: Thực hiện cập nhật logging và README
