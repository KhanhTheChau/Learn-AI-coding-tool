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
        Trong thực tế, bạn có thể gọi OpenAI API tại đây.
        """
        await asyncio.sleep(2)
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
