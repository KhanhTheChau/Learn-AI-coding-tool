import os
import pytest
from src.pipeline.video_assembler import VideoAssembler
from unittest.mock import patch

@pytest.mark.asyncio
async def test_assemble_video_fallback(tmp_path):
    assembler = VideoAssembler()
    output_path = tmp_path / "test_video.mp4"
    
    # Ép ffmpeg.probe sinh lỗi FileNotFoundError (giả lập máy không có ffmpeg)
    with patch("src.pipeline.video_assembler.ffmpeg.probe", side_effect=FileNotFoundError):
        result = await assembler.assemble_video("kịch bản test", str(output_path))
        
    assert result == str(output_path)
    assert os.path.exists(output_path)
    
    # Đảm bảo file dummy có hex header chuẩn
    with open(output_path, "rb") as f:
        content = f.read()
        assert content.startswith(bytes.fromhex("000000206674797069736f6d0000020069736f6d69736f32617663316d703431"))
