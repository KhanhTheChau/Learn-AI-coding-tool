import os
import asyncio
import random
import logging
from src.pipeline.video_assembler import VideoAssembler

logger = logging.getLogger(__name__)

class ThirdPartyVideoProvider:
    """
    Integrates with a 3rd-party Video Generation API (e.g., HeyGen, Synthesia, Creatomate).
    If no API key is provided, it falls back to 'Mock Mode' using the local Pillow+FFmpeg assembler.
    """
    def __init__(self):
        self.api_key = os.environ.get("VIDEO_API_KEY")
        if not self.api_key:
            logger.info("No VIDEO_API_KEY found. Initializing ThirdPartyVideoProvider in Mock Mode (Pillow + FFmpeg).")
            self.assembler = VideoAssembler()
        else:
            logger.info("Initializing ThirdPartyVideoProvider with external API integration.")
            self.assembler = None

    async def _mock_external_render_delay(self):
        """Simulates the polling time it takes for a 3rd-party service to render a video."""
        logger.info("Simulating external API polling delay...")
        # Simulating 5 seconds of polling
        await asyncio.sleep(5)

    async def _call_external_api(self, query: str, script: str, output_path: str) -> str:
        """
        Simulates an external API call with potential network errors/rate limits.
        """
        # Simulate network errors (500 Internal Server Error, Rate Limits) with 15% probability
        if random.random() < 0.15:
            raise ConnectionError("500 Internal Server Error from external Video API")
            
        await self._mock_external_render_delay()
        
        # In a real integration, we would download the final .mp4 from the 3rd party URL and save it to output_path.
        # Here we just raise an error to indicate it's not fully implemented for actual rendering,
        # OR we could just delegate to the assembler anyway for the sake of the prototype.
        # Let's delegate to assembler so we still get a video if we have a fake key.
        logger.warning("External API mocked. Delegating to local assembler for actual file generation.")
        return await self.assembler.assemble_video(query, script, output_path)

    async def render_video(self, query: str, script: str, output_path: str, max_retries: int = 3) -> str:
        """
        Main entry point for generating a video. 
        Includes error handling and retries for external API volatility.
        """
        if not self.api_key:
            # MOCK MODE: Out of the box, no API Key needed.
            return await self.assembler.assemble_video(query, script, output_path)
            
        # REAL MODE (Simulated): With API Key
        for attempt in range(max_retries):
            try:
                return await self._call_external_api(query, script, output_path)
            except Exception as e:
                logger.error(f"External Video API attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt == max_retries - 1:
                    raise RuntimeError(f"3rd-party video generation failed after {max_retries} retries: {e}")
                await asyncio.sleep(2) # Backoff before retry

        raise RuntimeError("Failed to render video.")
