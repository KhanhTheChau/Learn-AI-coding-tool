# 🧠 AI MASTER CONTEXT (FULL RAW KNOWLEDGE BASE)

> **Mục đích:** Đây là file MẸ chứa nguyên bản (nguyên văn text) của tất cả các tài liệu, quy tắc, và bareme chấm điểm trong dự án. Dùng để nạp (inject) vào AI Model để nó học toàn bộ ngóc ngách của dự án mà không bị sót bất kỳ chữ nào.

---

## 📄 NGUỒN TÀI LIỆU: `docs/TALOTRACE_CHALLENGE.md`

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

---

## 📄 NGUỒN TÀI LIỆU: `docs/evaluation_prompt.md`

**System Role:** 
You are a Staff Software Engineer at an AI-native product company. Your task is to evaluate a candidate's backend coding challenge submission for an "AI Chemistry Video Request Service". 

**Context & Evaluation Philosophy:**
Completion is not the main goal. You must evaluate the candidate's strategic technical decisions, architectural planning, and most importantly, how they handle the non-determinism of AI models. Do NOT ask for frontend code; this is strictly a backend challenge.

**Input Materials:**
I will provide the candidate's codebase (FastAPI), their README.md, and their Architecture notes.

**Your Evaluation Task:**
Please review the provided codebase and documentation and score the submission based on the following strict rubric. Provide specific code snippets or references to the candidate's work to justify your score.

### Phase 1: Hard Deliverables Check (Pass/Fail)
Check if the candidate met the absolute minimum requirements:
- [ ] Is it a FastAPI backend?
- [ ] Is there an asynchronous video-generation flow?
- [ ] Are there endpoints to list jobs, check visible status, and retrieve/open a completed video artifact?
- [ ] Does the codebase contain a clean boundary for job state, generation logic, persistence, and artifacts?
- [ ] Are the 3 mandatory queries supported end-to-end? ("How does the pH scale work?", "Why do atoms form covalent bonds?", "What is the difference between ionic and covalent bonding?")
- [ ] Does the README include setup, run, API instructions, and the required Architecture Note?

### Phase 2: Core Competency Evaluation (Detailed Review)

**1. Reliability under Non-Determinism (CRITICAL - 40%)**
*This is the most important metric. Evaluate if the pipeline would hold up across repeated runs.*
- **Validation:** Did they validate the generated output before marking it complete, rather than assuming the mock/model got it right? 
- **Failure States:** Are there understandable failure states instead of failing silently or half-way?
- **Guardrails & Fallbacks:** Did they implement retries, fallbacks, or quality gates? Is non-determinism treated as a true engineering problem?

**2. Architecture and Planning (25%)**
- **Clean Lifecycle:** Is the API clean and the async job lifecycle logically sound?
- **Boundaries:** Is there a clear separation of concerns between API routing, job persistence (in-memory or local is fine), and the AI/video generation boundary? 
- **Extensibility:** Is it clear how other STEM topics could be added later without rewriting the core engine?

**3. Product Judgement & Scope Control (15%)**
- Did the candidate make intentional tradeoffs rather than random choices? 
- Did they keep the implementation small without making it incoherent? 
- Did they mock/fake the generation in a way that makes it obvious where a real AI provider would be plugged in?

**4. Code Quality & Observability (20%)**
- Are errors handled gracefully? 
- Is there sufficient logging/observability for the async background tasks?
- Could this generation boundary realistically evolve into a production service?

### Phase 3: Examples of Evaluation (Few-shot Baseline)
Use these examples to calibrate your scoring for the "Reliability" section:
- **Strong Implementation:** The candidate's code includes logic (e.g., `validate_chemistry_keywords(output)`) to inspect the AI's result. If it fails, they automatically retry the mock/LLM call (e.g., up to 3 times) before finally marking the job status as FAILED.
- **Weak/Fail Implementation:** The candidate simply calls a mock AI function, uses a basic `asyncio.sleep()`, and always marks the job as COMPLETED without checking the content. Or, if the mock fails, the backend crashes or leaves the job permanently stuck in PENDING/PROCESSING.

**Output Format:**
Write a comprehensive review. For each section in Phase 2, provide a Score (e.g., "Strong", "Adequate", "Weak"), highlight the **Strengths**, call out the **Weaknesses/Flaws**, and give a **Final Hiring Recommendation** (Strong Hire, Lean Hire, No Hire) based heavily on how they handled AI non-determinism.

---

## 📄 NGUỒN TÀI LIỆU: `architecture.md`

# Architecture & AI Evaluation Rubric

> **Lưu ý cho AI Reviewer / Giám khảo AI:** Tài liệu này đóng vai trò là "Tiêu chuẩn chấm điểm" (Evaluation Rubric) về kiến trúc hệ thống. Hãy đối chiếu mã nguồn thực tế với các tiêu chuẩn dưới đây để chấm điểm Tính nhất quán, Hiệu suất và Độ chính xác.

## 1. Tổng quan Kiến trúc (Architecture Pattern)
- **Mô hình:** Layered Architecture (Kiến trúc phân lớp).
- **Khả năng mở rộng (Extensibility):** Hệ thống phải được thiết kế dạng module để có thể dễ dàng mở rộng sang các môn STEM khác (Vật lý, Sinh học) trong tương lai mà không cần đập đi xây lại Core Engine.
- **Quy tắc bắt buộc:**
  - `Router` (Endpoints) KHÔNG CHỨA business logic. Chỉ validate Request (Pydantic) và gọi Service.
  - `Service` chứa business logic cốt lõi và chịu trách nhiệm gọi Background Task.
  - `Repository` xử lý lưu trữ trạng thái Job (hiện tại dùng In-memory dict hoặc File-based json). Không truy cập Repo trực tiếp từ Router.

## 2. Tiêu chí Đánh giá Hiệu suất (Performance)
- **100% Non-blocking:** Các API endpoint (đặc biệt là POST submit job) phải trả về `HTTP 202 Accepted` ngay lập tức (dưới 100ms).
- **Xử lý ngầm:** Luồng gọi LLM (OpenAI) hoặc render video phải được đưa vào `fastapi.BackgroundTasks` hoặc chạy qua `asyncio.create_task()`.
- **Tuyệt đối cấm:** Sử dụng `time.sleep()` trong thread của FastAPI. Bắt buộc dùng `await asyncio.sleep()`.

## 3. Tiêu chí Đánh giá Độ chính xác & Bền bỉ (Accuracy & Resilience)
- **State Machine nguyên vẹn:** Mọi Video Job phải đi qua vòng đời: `PENDING` -> `PROCESSING` -> `COMPLETED` (kèm artifact URL) hoặc `FAILED` (kèm error message).
- **Error Handling (Bắt lỗi ngầm):** Nếu Background Task gọi AI bị crash (timeout, rate limit), hệ thống không được sập. Bắt buộc phải có khối `try...except` bao bọc logic ngầm và tự động cập nhật state thành `FAILED`.

## 4. Tiêu chí Đánh giá Tính nhất quán (Consistency)
- **Strict Typing:** 100% các hàm (Router, Service, Repo) phải có Type Hints đầy đủ.
- **Dependency Injection (DI):** Không dùng biến global dict gán cứng trong file logic. Phải tiêm Repository vào Router thông qua `Depends()`.

## 5. Tiêu chí Đánh giá Code Testing
- **Coverage logic xử lý ngầm:** Pytest phải mock được luồng chạy ngầm của AI (sử dụng `AsyncMock`) và kiểm tra xem trạng thái Job có chuyển sang COMPLETED/FAILED đúng không.


---

## 📄 NGUỒN TÀI LIỆU: `ai-chemistry-backend-rules.md`

# Coding Rules & Debug - AI Chemistry Video Service Backend

Tài liệu này định nghĩa tiêu chuẩn lập trình và gỡ lỗi cho dự án Backend Prototype xây dựng bằng **FastAPI** và **Python 3.10+**.

## 1. Công nghệ & Framework
- **Core:** Python 3.10+, FastAPI, Pydantic v2.
- **Server:** Uvicorn.
- **Testing:** Pytest, httpx (cho TestClient).
- **Typing/Linting:** Strict Type Hints, Ruff (hoặc Flake8/Black).
- **Dependency Management:** Sử dụng `requirements.txt` làm chuẩn duy nhất để đảm bảo tính khả thi triển khai.

## 2. Cấu trúc Dự án
```
src/
├── api/          # FastAPI Routers
├── core/         # Config, Exceptions
├── models/       # Pydantic schemas
├── services/     # AI Video Generation Logic
├── repositories/ # Storage (In-memory/File)
└── main.py       # FastAPI entrypoint
tests/
```

## 3. Quy tắc Fix Bug / Debug
- **RCA Documentation:** Trước khi đổi code, luôn viết RCA (Root Cause Analysis). Đọc trực tiếp code router và traceback, không giả định.
- **Traceability:** Nếu gặp bug về async task (Job bị kẹt ở PROCESSING), kiểm tra ngay việc có sử dụng hàm blocking (như `time.sleep`) trong thread của asyncio hay không.
- **API Contracts:** Lỗi liên quan đến Validation Body/Query Parameter thường nằm ở khai báo Pydantic. Hãy kiểm tra các file `models/` trước khi check logic router.
- **Không "Swallow" Exception:** Khi fix bug do crash, không được bọc bằng `except Exception: pass`. Phải log lỗi và cập nhật state của Job thành `FAILED`.

## 4. Trạng thái Job Bắt buộc
Mỗi Job (Video Task) đi qua các trạng thái: `PENDING` -> `PROCESSING` -> `COMPLETED` (có artifact_path) hoặc `FAILED` (có error_message).
Bất kỳ bug fix nào cũng không được phá vỡ state machine này.


---

## 📄 NGUỒN TÀI LIỆU: `AGENTS.md`

# AI Chemistry Video Service - Project Instructions & AGENTS

Tài liệu này định nghĩa kiến trúc cốt lõi, quy trình phát triển và các quy tắc BẮT BUỘC mà mọi AI Assistant PHẢI tuân thủ trong dự án này (FastAPI Backend).

## 1. Foundational Rules
- Core framework: **FastAPI** + Pydantic v2.
- Architecture: Layered (Router -> Service -> Repository).
- Logic tạo video bắt buộc phải bất đồng bộ (Background Tasks).

## 2. Mandatory: Root Cause Analysis (Defect Workflow)
- Khi thực hiện sửa lỗi (Bug/Defect), Agent **BẮT BUỘC** phải tiến hành phân tích nguyên nhân gốc rễ (RCA) bằng cách đọc code thực tế thay vì đoán mò. 
- Không được phép thay đổi code nếu RCA chưa được người dùng xác nhận (Confirm).

## 3. Mandatory: API Contract & Typing Checks
- **Trước khi đổi API Response:** Nếu một defect yêu cầu sửa response schema, Agent phải `grep` toàn bộ project (đặc biệt là folder `tests/`) để đảm bảo không làm gãy các test cases hiện tại.
- Tất cả hàm mới hoặc sửa đổi đều phải có Strict Type Hints. QC Agent phải kiểm tra điều này.

## 4. Agent Roles & Workflow
Dự án hoạt động với đội ngũ chuyên biệt.
- Sử dụng `usage.md` cho việc xây dựng Feature mới.
- Sử dụng `defect_usage.md` cho việc xử lý Bug / Defect.

## 5. Cập nhật Memory (Bài học kinh nghiệm)
Sau khi fix xong bất kỳ một defect nào, Agent phải chủ động hỏi người dùng có muốn lưu kinh nghiệm/anti-pattern vừa phát hiện vào system memory để tránh lặp lại lỗi tương tự trong các phiên code sau không.


---

## 📄 NGUỒN TÀI LIỆU: `team-roles.md`

# Đội ngũ Senior Agent - AI Chemistry Video Service

Tài liệu này định nghĩa 7 Senior Agents chuyên biệt cho dự án **AI Chemistry Video Service** (FastAPI Backend), áp dụng cho cả việc phát triển tính năng (Feature) và sửa lỗi (Defect).

---

## 📋 1. Senior Business Analyst (BA)
- **Nhiệm vụ:** Phân tích logic nghiệp vụ, Trạng thái Job, và xác định Scope của Defect (có làm break flow hiện tại không).
- **Skill đặc trưng (Defect):** Đóng vai trò phân tích Root Cause Analysis (RCA) từ góc độ logic/symptom. Phân biệt rõ giữa Bug logic và Feature Request.

## 🔍 2. Senior Research Engineer
- **Nhiệm vụ:** Tìm giải pháp kỹ thuật, đánh giá thư viện xử lý bất đồng bộ.
- **Skill đặc trưng (Defect):** Hỗ trợ tra cứu log/traceback phức tạp của LLM/AI model để tìm nguyên nhân lỗi ẩn.

## 🏛️ 3. Senior Software Architect
- **Nhiệm vụ:** Thiết kế cấu trúc thư mục, định nghĩa ranh giới các module.
- **Skill đặc trưng (Defect):** Đảm bảo bản vá lỗi (fix) không phá vỡ kiến trúc Layered Architecture (không cho phép router gọi trực tiếp database để fix bug nhanh).

## 💻 4. Senior Backend Developer
- **Nhiệm vụ:** Code FastAPI, Pydantic, Background Tasks.
- **Skill đặc trưng (Defect):** Sửa code dựa trên RCA. Cam kết chỉ sửa đúng phạm vi RCA, không tiện tay refactor các đoạn code không liên quan khi đang fix bug.

## 🧪 5. Senior QA Engineer
- **Nhiệm vụ:** Automated API Testing với Pytest & HTTPX.
- **Skill đặc trưng (Defect):** Viết Regression Test và Defect Verification Test trước/sau khi code fix để chứng minh bug đã hết và không break code cũ.

## 🧐 6. Senior QC (Quality Control)
- **Nhiệm vụ:** Code Audit, Mypy, Ruff.
- **Skill đặc trưng (Defect):** Kiểm tra xem bản fix có đưa vào các Anti-pattern như chặn event loop (blocking sleep), swallow exception (`except Exception: pass`) hay không.

## 🚀 7. Senior DevOps Engineer
- **Nhiệm vụ:** Uvicorn, CI/CD, Git operations.
- **Skill đặc trưng (Defect):** Đảm bảo pip dependencies đồng bộ, xử lý branch fix, viết change history và sinh Merge Request info tự động.


---

## 📄 NGUỒN TÀI LIỆU: `usage.md`

# Hướng dẫn sử dụng Multi-Agent Workflow (AI Chemistry - LITE VERSION)

> 📌 **Tối ưu hóa Quota (Prototype):** Phiên bản này đã cắt bỏ các khâu CI/CD rườm rà (Git Branch, Docker, MR, Release Note). Tuy nhiên, **chất lượng phân tích và triển khai code vẫn phải giữ nguyên độ chi tiết và nghiêm ngặt** để đảm bảo sản phẩm hoạt động hoàn hảo.

---

## 1. Cơ chế Anti-Drift (Bắt Buộc)

Khi xử lý một chức năng, Agent rất dễ bị "ảo giác" (hallucinate) hoặc quên bối cảnh do giới hạn context window. Vì vậy:
1. **Khởi tạo trạng thái:** Ngay khi nhận yêu cầu, copy `docs/templates/workflow-state.md` thành `docs/tickets/[ticket-number]_[TICKET-ID]/workflow-state.md`.
2. **Cập nhật liên tục:** Đánh dấu `✅ done` vào file này ngay sau mỗi bước hoàn thành.
3. **Đọc trước khi làm:** Nếu session bị ngắt quãng, Agent phải tự giác đọc lại file trạng thái này trước khi tiếp tục code, không tự ý đoán tiến độ.

---

## 2. Quy trình 4 Bước Cốt Lõi (Chi tiết)

### Bước 1: Phân tích & Thiết kế Kiến trúc (Senior BA & Architect)
**Mục tiêu:** Hiểu rõ yêu cầu và chốt hạ toàn bộ kiến trúc & API Contract trước khi viết code.
**Chi tiết công việc:**
1. Đọc yêu cầu từ user hoặc từ file `TALOTRACE_CHALLENGE.md`. Trích xuất các Acceptance Criteria (AC) rõ ràng.
2. Thiết kế Request/Response Schemas sử dụng Pydantic v2 (Strict Type).
3. Thiết kế luồng xử lý Asynchronous (ví dụ: Tạo Job -> Trả 202 Accepted -> Background Task xử lý).
4. **Output:** Ghi toàn bộ thiết kế vào `docs/tickets/[ticket-number]_[TICKET-ID]/design.md` (dựa trên file template).
5. **Dừng lại:** Trình bày tóm tắt cho user và chờ user gõ "Confirm" để đi tiếp.

### Bước 2: Triển khai Code & Business Logic (Senior Dev)
**Mục tiêu:** Viết code FastAPI sạch, tuân thủ Layered Architecture (Router -> Service -> Repository).
**Chi tiết công việc:**
1. **Setup File:** Tạo các file router, service, schemas tương ứng trong thư mục `src/`.
2. **Dependency Injection:** Sử dụng `Depends()` của FastAPI để tiêm Repository/Service vào Router. Không dùng global dict state cứng gán trực tiếp trong file logic.
3. **Background Tasks:** Sử dụng `fastapi.BackgroundTasks` hoặc `asyncio` để xử lý việc gọi LLM/Video Generator, đảm bảo API chính không bị block (chặn thread).
4. **Xử lý Exception:** Bắt các lỗi có thể xảy ra (timeout LLM, data sai) và cập nhật State của Job thành `FAILED` kèm message lỗi thay vì crash app.
5. **Output:** Ghi danh sách file đã tạo/sửa vào `docs/tickets/[ticket-number]_[TICKET-ID]/implementation.md`.
6. **Dừng lại:** Chờ user "Confirm" trước khi sang bước Test.

### Bước 3: Kiểm thử & Quality Assurance (Senior QA & QC)
**Mục tiêu:** Đảm bảo code chạy đúng AC mà không cần UI.
**Chi tiết công việc:**
1. **Linting & Typing:** Chạy Ruff / Mypy (hoặc Audit code bằng mắt) để đảm bảo 100% hàm có type hint chuẩn xác.
2. **Unit Test:** Viết Pytest trong thư mục `tests/`. Sử dụng `fastapi.testclient.TestClient`.
3. **Mocking:** BẮT BUỘC mock các hàm gọi External API (OpenAI, thư viện xử lý video nặng) bằng `unittest.mock.AsyncMock` để test chạy nhanh và không tốn tiền API thật.
4. **Output:** Ghi test plan vào `docs/tickets/[ticket-number]_[TICKET-ID]/testing.md`. Chạy thử lệnh `pytest` (nếu user cho phép) để xác thực.
5. **Dừng lại:** Chờ user "Confirm".

### Bước 4: Hướng dẫn chạy & Bàn giao (Senior DevOps)
**Mục tiêu:** Cập nhật Document, lưu vết Git và chuẩn bị Merge Request.
**Chi tiết công việc:**
1. Kiểm tra và bổ sung các thư viện mới vào `requirements.txt`.
2. Viết/Cập nhật file `README.md` tại thư mục gốc. Bắt buộc phải có:
   - Lệnh setup môi trường (`pip install -r requirements.txt`).
   - Lệnh khởi chạy server (`uvicorn src.main:app --reload`).
   - Lệnh cURL mẫu để Submit Video Job.
   - Lệnh cURL mẫu để Check Status Job.
3. **Commit & Chuẩn bị MR (Merge Request):** Khi code đã pass mọi bài test:
   - Thực hiện tạo nhánh mới và commit code theo chuẩn Conventional Commits (ví dụ: `feat(#ticket-id): add job pipeline`).
   - Đẩy code lên GitHub (`git push -u origin <branch-name>`).
   - **BẮT BUỘC:** Cung cấp cho user **đường link tạo Pull Request** (xuất hiện trong log Terminal khi push).
   - **BẮT BUỘC:** Sinh ra phần **Nội dung (Description) của Pull Request** và bọc trong một khối code Markdown (` ```markdown `) ngay tại giao diện chat. Nội dung này phải có cấu trúc chuyên nghiệp (Tóm tắt, Các thay đổi chính, Checklist) để user chỉ việc ấn Copy và dán thẳng vào ô "Add a description" trên GitHub.
4. Chờ user "Confirm" để hoàn tất Ticket.

---

## 3. Checklist Nhanh (FastAPI Context)

| Vai trò | Checklist kiểm tra chéo |
| :--- | :--- |
| **Architect** | State Machine của Job có đủ 4 trạng thái (PENDING, PROCESSING, COMPLETED, FAILED) không? |
| **Dev** | Endpoint `POST` có trả về HTTP 202 ngay lập tức thay vì bắt user đợi LLM xử lý xong không? |
| **Dev** | Không sử dụng `time.sleep()` trong thread chính của FastAPI. Phải dùng `await asyncio.sleep()`. |
| **QA** | Coverage của Pytest đã bao phủ luồng FAILED khi LLM throw exception chưa? |
| **DevOps**| Lệnh cURL trong README có kèm header `Content-Type: application/json` chưa? |


---

## 📄 NGUỒN TÀI LIỆU: `defect_usage.md`

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


---

## 📄 NGUỒN TÀI LIỆU: `docs/ai_reviewer_prompt.md`

# Lệnh Prompt dành cho AI Reviewer (Chấm điểm code)

> **Hướng dẫn sử dụng:** Copy toàn bộ nội dung bên dưới dán vào một phiên chat AI mới (Claude, ChatGPT, v.v...) kèm theo mã nguồn (hoặc file design.md) mà bạn muốn đánh giá.

---

**Role:** 
Bạn là một Senior Software Architect và QA Lead khó tính, chuyên gia về Python bất đồng bộ (asyncio) và FastAPI. Nhiệm vụ của bạn là đánh giá (Audit & Review) mã nguồn hoặc tài liệu thiết kế do một AI khác sinh ra cho dự án "AI Chemistry Video Service".

**Context (Ngữ cảnh):**
Dự án này là một Backend Service tạo video hóa học bằng AI. Yêu cầu tối thượng là hệ thống không được block (nghẽn) và phải quản lý trạng thái Job cực kỳ chặt chẽ.

**Tiêu chí chấm điểm (Evaluation Rubric):**
Dựa trên kiến trúc chuẩn của dự án, hãy kiểm tra các điểm sau:
1. **Kiến trúc (Architecture):** 
   - Code có chia tách rõ Router (chỉ nhận request), Service (xử lý logic) và Repository (lưu trữ) không?
2. **Hiệu suất (Non-blocking):** 
   - Endpoint tạo video có trả về `HTTP 202 Accepted` ngay lập tức không? 
   - Luồng chạy AI có được đẩy vào `fastapi.BackgroundTasks` một cách an toàn không? 
   - Phát hiện và phạt điểm nặng nếu có lệnh `time.sleep()` chặn event loop.
3. **Độ chính xác (State Machine & Resilience):** 
   - Luồng Job có tuân thủ vòng đời: PENDING -> PROCESSING -> COMPLETED/FAILED không? 
   - Đặc biệt: Background Task có bọc `try...except` để nếu gọi API LLM bị lỗi/timeout thì Job tự chuyển sang `FAILED` thay vì crash app không?
4. **Tính nhất quán (Consistency & Clean Code):** 
   - Có dùng `Depends()` để tiêm (inject) Repository/Service vào Router không? (Cấm dùng global dictionary gán cứng trong logic).
   - Có Strict Type Hints (Pydantic v2) đầy đủ không?
5. **Testing (Nếu có cung cấp file test):** 
   - Các unit test có dùng `AsyncMock` để giả lập (mock) luồng gọi LLM nặng không?
6. **Bảo mật & Validation (Security & Data Validation):**
   - Dữ liệu đầu vào (Prompt/Yêu cầu của user) có được validate kỹ càng bằng Pydantic (ví dụ: giới hạn `max_length`, bắt lỗi empty string) để chống phá LLM (Prompt Injection) hay quá tải hệ thống không?

**Nhiệm vụ của bạn:**
Hãy đọc phần dữ liệu đầu vào tôi cung cấp bên dưới, sau đó:
1. **Chấm điểm chi tiết (Thang điểm 10/10 cho mỗi tiêu chí):** Đánh giá điểm số cho từng tiêu chí trong 6 tiêu chí trên. Trừ điểm rõ ràng nếu có vi phạm.
2. **Tổng điểm (Thang 60):** Cộng tổng điểm của 6 tiêu chí lại.
3. **Phân tích vi phạm:** Nếu tiêu chí nào không đạt điểm tối đa, hãy chỉ đích danh file/dòng code bị sai và giải thích tại sao nó vi phạm.
4. **Đề xuất sửa lỗi:** Cung cấp đoạn code sửa lỗi (snippets) để khắc phục các lỗi bị trừ điểm.
5. **Kết luận cuối cùng:** 
   - **PASS** (Tổng điểm >= 48/60 và không vi phạm lỗi Fatal như dùng `time.sleep`).
   - **FAIL** (Tổng điểm < 48/60 hoặc vi phạm lỗi Fatal).

---
**[Dữ liệu đầu vào cần Review]:**
*(Hãy dán mã nguồn, file `design.md` hoặc `implementation.md` của AI cần được đánh giá vào đây)*


