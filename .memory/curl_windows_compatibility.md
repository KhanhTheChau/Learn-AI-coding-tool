# Bài học: Cú pháp cURL trên Windows (CMD / PowerShell)

## 1. Vấn đề (Bug/Defect)
Khi cung cấp tài liệu hướng dẫn test (cURL commands) cho người dùng, nếu sử dụng cú pháp chuẩn của Bash (Linux/Mac) thì sẽ gặp lỗi vỡ chuỗi JSON hoặc `URL rejected` trên môi trường Windows (CMD hoặc PowerShell).

- **Cú pháp gây lỗi:**
  ```bash
  curl -X POST http://localhost:8000/api/v1/jobs \
    -H "Content-Type: application/json" \
    -d '{"query": "Oxi hóa khử"}'
  ```
- **Lý do lỗi (Root Cause):** 
  - Ký tự gạch chéo ngược `\` để ngắt dòng không hoạt động trong PowerShell (dùng `` ` ``) hoặc CMD (dùng `^`).
  - Dấu nháy đơn `' '` bọc chuỗi JSON body không được CMD/PowerShell hỗ trợ đúng chuẩn, khiến các tham số bị cắt vụn và sai định dạng JSON.

## 2. Giải pháp (Best Practice)
Trong MỌI TÀI LIỆU (như `README.md`, `manual_test.md`), khi sinh lệnh cURL để đưa người dùng chạy:
- **BẮT BUỘC** viết trên 1 dòng duy nhất (inline) để tránh lỗi ngắt dòng đa nền tảng.
- **BẮT BUỘC** sử dụng dấu ngoặc kép (`"`) cho cả lớp bọc ngoài cùng và escape các ngoặc kép bên trong JSON (`\"`).

- **Cú pháp chuẩn đa nền tảng (Windows/Mac/Linux):**
  ```cmd
  curl -X POST http://localhost:8000/api/v1/jobs -H "Content-Type: application/json" -d "{\"query\": \"Oxi hóa khử\"}"
  ```

## 3. Quy tắc áp dụng
Kể từ nay, Agent **PHẢI** luôn format mọi mã cURL JSON theo định dạng chuẩn 1 dòng và dùng `\"` khi hướng dẫn người dùng chạy lệnh trên Terminal.
