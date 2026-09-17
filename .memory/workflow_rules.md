# Quy tắc Dừng & Ghi nhận lỗi (Anti-Drift Extension)

Kinh nghiệm rút ra từ Ticket #01:
Để tránh AI tự động chạy qua lỗi mà không báo cáo, bắt buộc tuân thủ quy tắc sau:

1. **Quy tắc Dừng (STRICT STOP):** Tại cuối mỗi bước lớn (Bước 1, 2, 3, 4) trong `usage.md`, Agent TUYỆT ĐỐI KHÔNG ĐƯỢC tự động làm tiếp. Agent phải dừng lại, trình bày kết quả và chỉ được phép thực hiện bước tiếp theo khi User gõ chính xác chữ "Confirm" (hoặc đồng ý rõ ràng).
2. **Ghi nhận Lỗi (Error Logging):** Nếu có bất kỳ lỗi nào xảy ra trong quá trình thực thi (test thất bại, lỗi linter, ngoại lệ hệ thống...), Agent PHẢI lưu chi tiết lỗi và kết quả phân tích nguyên nhân (RCA) vào file trạng thái của ticket (hoặc tạo file lỗi riêng) trước khi dừng lại báo cáo cho User. Không tự ý đoán mò sửa lỗi khi chưa được Confirm.
