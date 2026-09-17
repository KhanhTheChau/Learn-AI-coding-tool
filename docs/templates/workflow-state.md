# Workflow State — [TICKET-ID] (#[ticket-number])

> 📌 **Nguồn Sự Thật Tiến Độ (LITE VERSION):** Dù đã cắt giảm các bước DevOps rườm rà cho Prototype, bảng tiến độ này vẫn phải được track cực kỳ chi tiết để chống AI mất bối cảnh (Anti-Drift). Trước khi làm bước tiếp theo hoặc khi resume session, BẮT BUỘC đọc file này.

**Ticket:** #[ticket-number] — [TICKET-ID] — [Tên tính năng]
**Branch:** [tên-branch] (Hoặc làm trực tiếp trên main)
**Cập nhật lần cuối:** [YYYY-MM-DD HH:mm]

## Tiến độ theo usage.md (Micro-Checklist)

| Bước | Mô tả chi tiết | Trạng thái | File output | Ngày xong |
|---|---|---|---|---|
| **1.1** | Phân tích yêu cầu & Bóc tách Acceptance Criteria (AC) | ⬜ pending | `docs/tickets/[ticket-number]_[TICKET-ID]/requirements.md` | |
| **1.2** | Thiết kế Pydantic Schemas (Request/Response) | ⬜ pending | `docs/tickets/[ticket-number]_[TICKET-ID]/design.md` | |
| **1.3** | Thiết kế luồng xử lý Asynchronous (Background Task) | ⬜ pending | *Ghi chung vào design.md* | |
| **2.1** | Setup Thư mục, File & Dependency Injection (Depends) | ⬜ pending | `docs/tickets/[ticket-number]_[TICKET-ID]/implementation.md` | |
| **2.2** | Triển khai Logic API & Background Task gọi LLM | ⬜ pending | *Mã nguồn Python* | |
| **2.3** | Bắt Exception & Quản lý State (FAILED/COMPLETED) | ⬜ pending | *Mã nguồn Python* | |
| **3.1** | Audit Type Hints (Mypy/Ruff) | ⬜ pending | `docs/tickets/[ticket-number]_[TICKET-ID]/testing.md` | |
| **3.2** | Viết Pytest & Mocking (AsyncMock) External APIs | ⬜ pending | `tests/test_...py` | |
| **4.1** | Kiểm tra & Cập nhật `requirements.txt` | ⬜ pending | `requirements.txt` | |
| **4.2** | Viết lệnh cURL mẫu & Hướng dẫn khởi chạy | ⬜ pending | `README.md` (root) | |

**Quy ước trạng thái:** `⬜ pending` -> `⏳ in_progress` -> `✅ done`
Chỉ đánh `✅ done` khi **đã lưu file output** VÀ **user đã confirm** hạng mục đó.

## Ghi chú gián đoạn (Điền khi task bị ngắt giữa chừng)
- Lần cuối làm tới: [Bước X.Y — mô tả]
- Việc cần làm tiếp theo: [...]
- Lưu ý/blocker còn tồn đọng: (Ví dụ: Đang kẹt ở lỗi Pydantic Validation, cần fix type hint...)
