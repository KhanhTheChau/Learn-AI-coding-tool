import asyncio
import logging

logger = logging.getLogger(__name__)

CHEMISTRY_KEYWORDS = [
    "oxi", "khử", "electron", "phản ứng", "axit", "bazơ", 
    "muối", "nguyên tử", "phân tử", "hóa học", "ion"
]

def validate_chemistry_keywords(output: str) -> bool:
    """
    Kiểm tra xem output có chứa ít nhất 1 từ khóa Hóa học cơ bản hay không.
    Nếu không, raise ValueError để báo hiệu AI Hallucination.
    """
    output_lower = output.lower()
    for kw in CHEMISTRY_KEYWORDS:
        if kw in output_lower:
            return True
            
    raise ValueError("Output does not contain chemistry keywords (Hallucination detected)")

class AIVideoGenerator:
    async def _mock_ai_call(self, query: str) -> str:
        """
        Mô phỏng gọi API AI tốn thời gian.
        Trả về kịch bản cứng cho 3 câu hỏi đặc thù, hoặc kịch bản chung.
        """
        await asyncio.sleep(2)
        q = query.lower()
        if "thang đo ph" in q:
            return f"Kịch bản: Thang đo pH là thước đo mức độ axit hoặc bazơ của một dung dịch. Nó phản ứng với các chất chỉ thị màu."
        elif "cộng hóa trị" in q and "ion" not in q:
            return f"Kịch bản: Liên kết cộng hóa trị hình thành do sự dùng chung các electron giữa các nguyên tử."
        elif "ion" in q and "cộng hóa trị" in q:
            return f"Kịch bản: Liên kết ion hình thành do lực hút tĩnh điện, trong khi cộng hóa trị dùng chung electron. Cả hai đều là phản ứng hóa học."
        
        return f"Kịch bản mô phỏng về {query} với các phản ứng oxi hóa khử."

    async def generate_with_retry(self, query: str, max_retries: int = 3) -> str:
        """
        Gọi LLM và tự động retry nếu bị lỗi hoặc bị ảo giác (thiếu keyword).
        """
        for attempt in range(max_retries):
            try:
                # Gọi AI
                output = await self._mock_ai_call(query)
                
                # Kiểm duyệt kết quả
                validate_chemistry_keywords(output)
                
                # Nếu không raise lỗi, trả về kết quả
                return output
                
            except Exception as e:
                logger.warning(f"AI generation failed on attempt {attempt + 1}/{max_retries}: {str(e)}")
                if attempt == max_retries - 1:
                    # Hết cơ hội, ném lỗi ra ngoài cho Background Task catch
                    raise
                
        # Thực tế sẽ không bao giờ chạy đến dòng này do lệnh raise bên trên
        raise RuntimeError("Failed to generate video script after max retries")
