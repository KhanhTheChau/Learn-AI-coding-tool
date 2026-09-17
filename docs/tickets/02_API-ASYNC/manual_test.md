# Hướng dẫn Test tay (Manual Test) - 02_API-ASYNC

Tài liệu này hướng dẫn người dùng (hoặc QA manual) cách kiểm tra chức năng Background Tasks và API bằng Postman hoặc cURL một cách thủ công, xác minh dữ liệu thực tế thay vì chỉ dựa vào Unit Test.

## 1. Chuẩn bị
Khởi chạy server FastAPI ở chế độ reload:
```bash
uvicorn src.main:app --reload
```
Đảm bảo server đang chạy ở `http://localhost:8000`.

## 2. Kịch bản 1: Luồng thành công (Happy Path)
**Bước 1: Submit một Job tạo video**
Mở Terminal mới và gọi lệnh:
```bash
curl -X POST http://localhost:8000/api/v1/jobs -H "Content-Type: application/json" -d "{\"query\": \"Giải thích phản ứng Oxi hóa khử\"}"
```
*Kỳ vọng:* Bạn sẽ nhận được HTTP 202 Accepted NGAY LẬP TỨC (không bị delay), JSON trả về có `status: "PENDING"`. 
Hãy copy chuỗi `id` trong kết quả trả về.

**Bước 2: Kiểm tra trạng thái đang xử lý**
Gần như ngay lập tức sau Bước 1, chạy lệnh kiểm tra ID đó (thay `<id>` bằng ID đã copy):
```bash
curl -X GET http://localhost:8000/api/v1/jobs/<id>
```
*Kỳ vọng:* Trạng thái sẽ là `PROCESSING`.

**Bước 3: Chờ 5 giây và kiểm tra lại (Video hoàn thành)**
Sau 5 giây, chạy lại lệnh GET ở Bước 2.
*Kỳ vọng:* Trạng thái sẽ chuyển thành `COMPLETED`, và có thêm trường `artifact_path: "https://dummy-bucket/videos/<id>.mp4"`.

**Bước 4: Thử lấy thông tin Video**
```bash
curl -X GET http://localhost:8000/api/v1/videos/<id>
```
*Kỳ vọng:* HTTP 200 kèm thông báo `"message": "Video is available at ..."`

## 3. Kịch bản 2: Validation chống rác (Security)
Gửi một request rỗng hoặc quá ngắn (dưới 5 ký tự) để kiểm tra Pydantic Validation.
```bash
curl -X POST http://localhost:8000/api/v1/jobs -H "Content-Type: application/json" -d "{\"query\": \"Oxi\"}"
```
*Kỳ vọng:* HTTP 422 Unprocessable Entity kèm thông báo lỗi của Pydantic giải thích rằng `query` phải lớn hơn hoặc bằng 5 ký tự.

## 4. Kiểm tra Console Log
Trong màn hình Terminal đang chạy lệnh `uvicorn`, bạn không được phép nhìn thấy bất kỳ lỗi Error traceback nào (do đã bọc `try-except`). Mọi thứ phải diễn ra mượt mà và không block các request khác.
