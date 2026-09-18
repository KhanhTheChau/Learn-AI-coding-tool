import asyncio
import os
import time
from src.pipeline.third_party_provider import ThirdPartyVideoProvider
from src.ai.video_generator import AIVideoGenerator

async def test_other_query():
    os.makedirs("output/exported_videos", exist_ok=True)
    
    ai_gen = AIVideoGenerator()
    provider = ThirdPartyVideoProvider()
    
    query = "What are atoms and molecules?"
    filename = "demo_test4_other.mp4"
    
    path = os.path.join("output/exported_videos", filename)
    print(f"Generating for {query} at {path}...")
    start_t = time.time()
    
    # Generate script using AI with retry logic
    script = await ai_gen.generate_with_retry(query)
    
    # Render using the provider
    await provider.render_video(query, script, path)
    
    print(f"Successfully created {path} in {time.time() - start_t:.2f}s")

if __name__ == "__main__":
    asyncio.run(test_other_query())
