# AI Chemistry Video Service (Prototype)

## Giới thiệu
Đây là bản nguyên mẫu (Prototype) Backend cho dịch vụ tạo video AI giáo dục (môn Hóa học). Hệ thống cung cấp API RESTful cho phép người dùng gửi yêu cầu giải thích một khái niệm, sau đó xử lý ngầm (background job) để tạo video và trả về kết quả mà không làm nghẽn (block) luồng chính.

## Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.10+
- **Framework:** FastAPI, Pydantic v2
- **Server:** Uvicorn
- **Testing:** Pytest

## Cấu trúc tài liệu & Đánh giá (Dành cho AI Reviewer)
Dự án này được thiết kế để các hệ thống AI khác có thể dễ dàng đọc, hiểu và chấm điểm.
- **Yêu cầu gốc:** Xem `docs/TALOTRACE_CHALLENGE.md`
- **Tiêu chuẩn Kiến trúc & Chấm điểm:** Xem `architecture.md` (Tiêu chí đánh giá tính nhất quán, hiệu suất).
- **Quy tắc Coding:** Xem `ai-chemistry-backend-rules.md`.

## Hướng dẫn chạy thử (Local)
*(Sẽ được tự động cập nhật bởi Senior DevOps Agent sau khi hoàn thành code ở Bước 4).*
