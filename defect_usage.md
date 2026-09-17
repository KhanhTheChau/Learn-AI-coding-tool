# Hướng dẫn xử lý Defect / Bug (AI Chemistry Video Service Backend)

> **Scope:** Tài liệu này dành riêng cho các **Defect** và **Bug** phát sinh trên Backend FastAPI — không áp dụng cho Feature mới. Nếu defect yêu cầu thay đổi thiết kế kiến trúc hoặc logic lớn → chuyển sang dùng `usage.md` (full workflow).

---

## 0. Nguyên tắc chung

| Nguyên tắc | Chi tiết |
| :--- | :--- |
| **Thuộc về ticket cha** | Mọi defect **phải liên kết** với task/feature ban đầu |
| **Không redesign** | Defect chỉ sửa đúng lỗi code Python / Pydantic — không refactor kiến trúc |
| **RCA bắt buộc** | Phải tìm ra root cause bằng cách đọc code thực tế, không đoán mò |
| **Docs trước, code sau** | Ghi tài liệu RCA ra file → chờ confirm → mới code |

---

## 1. Cấu trúc thư mục Docs cho Defect

```
docs/
└── tickets/
    └── [US-ID]/                          ← Thư mục ticket cha (US hoặc EPIC)
        └── defects/
            └── [DM-ID]/                  ← Ví dụ: DM-01-async-timeout
                ├── rca.md               ← Root Cause Analysis (Bước 1)
                ├── fix.md               ← Implementation Fix Spec (Bước 2)
                ├── test-case.md         ← Test cases verify fix (Bước 3)
                └── release.md           ← Release note defect (Bước 4)
```

---

## 2. Workflow xử lý Defect

### Bước 0 — Khởi tạo & Cập nhật môi trường (Senior DevOps)

Trước khi fix bug, cần đảm bảo môi trường local (Python packages) đang ở trạng thái mới nhất.
- **Agent hỏi:** *"Bạn đã cập nhật `requirements.txt` / pip install mới nhất chưa?"*
- Checkout nhánh mới với định dạng: `fix/[DM-ID]-[mô-tả-ngắn]` (Ví dụ: `fix/DM01-fix-pydantic-validation`).

### Bước 1 — Root Cause Analysis / RCA (Senior BA + Senior Dev)

Xác định chính xác **nguyên nhân gốc rễ** trước khi code.
**Yêu cầu tài liệu:** `docs/tickets/[US-ID]/defects/[DM-ID]/rca.md`
- Đọc code router, service, background tasks.
- Nếu lỗi liên quan đến AI generation, kiểm tra xem có phải do timeout hoặc API schema thay đổi không.
- Đề xuất hướng fix (không code). Trình bày và chờ Confirm.

### Bước 2 — Fix & Implementation (Senior Dev)

Sửa đúng theo RCA đã confirm.
**Yêu cầu tài liệu:** `docs/tickets/[US-ID]/defects/[DM-ID]/fix.md`
- Sửa code FastAPI, cập nhật Pydantic Model nếu cần.
- Nếu thay đổi endpoint response, phải grep toàn bộ project để kiểm tra các file tests có parse sai shape mới không.
- Lưu danh sách file đã đổi và logic thay đổi. Chờ Confirm.

### Bước 3 — Verify & Test (Senior QA)

Viết Pytest nhắm thẳng vào lỗi đã fix.
**Yêu cầu tài liệu:** `docs/tickets/[US-ID]/defects/[DM-ID]/test-case.md`
- Viết test case verify bằng `httpx` / `TestClient`.
- Đảm bảo regression test các luồng API Job PENDING -> PROCESSING không bị ảnh hưởng.
- Chạy `pytest` để xác thực.

### Bước 3.Memory — Cập nhật Bài học kinh nghiệm
- Agent hỏi user có muốn lưu lỗi này (vd: quên `await` asyncio, sai type Pydantic) vào memory không để tránh lặp lại.

### Bước 4 & 5 — Commit, Release Note & Sinh MR (Senior DevOps)
- Ghi `change_history.md`.
- Tạo file `release.md`.
- Sinh thông tin Merge Request để user copy.
