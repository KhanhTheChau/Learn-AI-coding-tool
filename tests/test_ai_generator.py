import pytest
from unittest.mock import AsyncMock
from src.ai.video_generator import AIVideoGenerator, validate_chemistry_keywords

def test_validate_chemistry_keywords_success():
    # Chứa từ khóa 'oxi'
    assert validate_chemistry_keywords("Quá trình oxi hóa xảy ra") == True

def test_validate_chemistry_keywords_failure():
    # Không chứa từ khóa Hóa học -> ném lỗi
    with pytest.raises(ValueError, match="Hallucination detected"):
        validate_chemistry_keywords("Đây là một video về Toán học")

@pytest.mark.asyncio
async def test_generate_with_retry_fails_after_3_attempts():
    ai_gen = AIVideoGenerator()
    
    # Mock AI luôn trả về kết quả ảo giác
    ai_gen._mock_ai_call = AsyncMock(return_value="Nội dung tào lao không liên quan")
    
    # Kỳ vọng hàm sẽ quăng ra lỗi ValueError sau khi đã thử đủ 3 lần
    with pytest.raises(ValueError, match="Hallucination detected"):
        await ai_gen.generate_with_retry("Một query bất kỳ", max_retries=3)
        
    # Xác nhận hàm gọi AI bị ép chạy đúng 3 lần
    assert ai_gen._mock_ai_call.call_count == 3

@pytest.mark.asyncio
async def test_generate_with_retry_succeeds_on_second_attempt():
    ai_gen = AIVideoGenerator()
    
    # Lần 1 trả về rác, Lần 2 trả về đúng
    ai_gen._mock_ai_call = AsyncMock(side_effect=[
        "Kết quả rác không có từ khóa",
        "Kịch bản có phản ứng oxi hóa khử"
    ])
    
    result = await ai_gen.generate_with_retry("query", max_retries=3)
    
    # Trả về thành công
    assert "oxi hóa khử" in result
    # Gọi chính xác 2 lần
    assert ai_gen._mock_ai_call.call_count == 2
