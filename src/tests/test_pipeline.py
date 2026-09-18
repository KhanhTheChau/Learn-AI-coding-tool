import os
import pytest
from src.pipeline.video_assembler import VideoAssembler
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_assemble_video_success(tmp_path):
    assembler = VideoAssembler()
    output_path = tmp_path / "test_video.mp4"
    
    # Mock subprocess.Popen để không thực sự gọi FFmpeg trong Unit Test
    with patch("src.pipeline.video_assembler.subprocess.Popen") as mock_popen:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        result = await assembler.assemble_video("Câu hỏi test", "Kịch bản test", str(output_path))
        
        assert result == str(output_path)
        mock_popen.assert_called_once()
