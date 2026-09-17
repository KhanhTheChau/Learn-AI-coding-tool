# Tài Liệu Đặc Tả Yêu Cầu (Requirements): AI Chemistry Video Service

## 1. Tổng Quan Dự Án
Dự án yêu cầu xây dựng một bản nguyên mẫu (prototype) backend cho dịch vụ tạo video AI giáo dục[cite: 1]. Hệ thống hoạt động theo mô hình bất đồng bộ (asynchronous): tiếp nhận yêu cầu giải thích một khái niệm hóa học từ người dùng, xử lý ngầm (background job) để tạo video (bao gồm hình ảnh và âm thanh), và cho phép người dùng theo dõi trạng thái cũng như truy xuất video khi hoàn tất[cite: 1].

---

## 2. Yêu Cầu Chức Năng (Functional Requirements - FR)
Hệ thống backend phải cung cấp các API (RESTful) để thực hiện các chức năng sau:

*   **FR1 - Tạo yêu cầu (Submit Job):** Cung cấp API endpoint để client gửi yêu cầu tạo video giải thích một khái niệm hóa học cụ thể[cite: 1].
*   **FR2 - Xử lý bất đồng bộ:** Hệ thống phải tiếp nhận yêu cầu và đưa vào luồng xử lý tạo video bất đồng bộ mà không chặn (block) request của client[cite: 1].
*   **FR3 - Quản lý danh sách (List Jobs):** Cung cấp API endpoint để liệt kê các video hoặc công việc (jobs) đã được yêu cầu[cite: 1].
*   **FR4 - Truy vấn trạng thái (Check Status):** Cung cấp API để kiểm tra trạng thái hiện tại của một công việc hoặc video cụ thể một cách rõ ràng[cite: 1].
*   **FR5 - Truy xuất kết quả (Retrieve Artifact):** Cung cấp cách thức để client truy xuất, mở hoặc tải về tệp video hoàn chỉnh (bao gồm cả hình ảnh và âm thanh)[cite: 1].

---

## 3. Yêu Cầu Phi Chức Năng (Non-Functional Requirements - NFR)

*   **NFR1 - Độ tin cậy (Reliability):** Hệ thống phải xử lý được "tính không xác định" (non-determinism) của các mô hình AI/LLM[cite: 1]. Kết quả đầu ra cho cùng một khái niệm phải nhất quán qua nhiều lần chạy lặp lại[cite: 1].
*   **NFR2 - Xử lý lỗi & Rào chắn (Error Handling & Guardrails):** Hệ thống không được lỗi ngầm (fail silently) hoặc dừng giữa chừng[cite: 1]. Phải có cơ chế xác thực kết quả (validate) trước khi trả về cho người học, có khả năng thử lại (retries) hoặc dùng phương án dự phòng (fallbacks) khi AI tạo ra kết quả hỏng[cite: 1].
*   **NFR3 - Chất lượng nội dung (Quality):** Video tạo ra phải mạch lạc, hữu ích, trả lời đúng trọng tâm truy vấn và có chất lượng hình ảnh tốt (được xem là một thước đo thành công)[cite: 1].
*   **NFR4 - Khả năng mở rộng (Extensibility):** Kiến trúc backend phải được thiết kế rõ ràng để cho thấy cách tích hợp các chủ đề STEM khác trong tương lai, dù hiện tại chỉ làm về hóa học[cite: 1].
*   **NFR5 - Hiệu năng (Performance/Latency):** Thời gian phản hồi (latency) để tạo ra video không bị đặt nặng[cite: 1]. Việc hệ thống mất thời gian để xử lý là hoàn toàn được chấp nhận, miễn là trạng thái chờ được API quản lý và hiển thị rõ ràng[cite: 1].

---

## 4. Ràng Buộc Kỹ Thuật & Kiến Trúc (Technical Constraints)

*   **Công nghệ cốt lõi:** Bắt buộc sử dụng framework FastAPI cho backend[cite: 1].
*   **Giao diện người dùng:** Không được xây dựng Frontend[cite: 1]. Việc kiểm thử có thể dùng cURL, Postman hoặc một script đơn giản[cite: 1].
*   **Ranh giới hệ thống (Boundaries):** Codebase phải tách biệt rõ ràng giữa logic quản lý trạng thái công việc, logic tạo video, lớp lưu trữ dữ liệu và cách quản lý tệp (artifacts)[cite: 1].
*   **Lưu trữ (Persistence):** Cho phép lưu trữ trạng thái trên bộ nhớ tạm (in-memory) hoặc lưu file cục bộ (local file store), miễn là ranh giới hệ thống được tổ chức sạch sẽ[cite: 1].
*   **Tích hợp AI:** Cho phép giả lập (mock) một phần quá trình tạo video, nhưng thiết kế phải thể hiện rõ vị trí mà một dịch vụ AI thực tế sẽ được cắm (plugged in) vào hệ thống[cite: 1].

---

## 5. Phạm Vi Dữ Liệu Bắt Buộc (Mandatory Scope)
Hệ thống phải xử lý thành công và trọn vẹn (end-to-end) 3 truy vấn hóa học sau[cite: 1]:
1.  Thang đo pH hoạt động như thế nào?[cite: 1]
2.  Tại sao các nguyên tử lại hình thành liên kết cộng hóa trị?[cite: 1]
3.  Sự khác biệt giữa liên kết ion và liên kết cộng hóa trị là gì?[cite: 1]