import asyncio
import os
import time
from src.pipeline.third_party_provider import ThirdPartyVideoProvider
from src.ai.video_generator import AIVideoGenerator

async def generate_mock_videos():
    os.makedirs("output/exported_videos", exist_ok=True)
    
    ai_gen = AIVideoGenerator()
    provider = ThirdPartyVideoProvider()
    
    test_cases = [
        {
            "query": "How does the pH scale work?",
            "filename": "demo_test1_ph.mp4"
        },
        {
            "query": "Why do atoms form covalent bonds?",
            "filename": "demo_test2_covalent.mp4"
        },
        {
            "query": "What is the difference between ionic and covalent bonding?",
            "filename": "demo_test3_difference.mp4"
        }
    ]
    
    for case in test_cases:
        path = os.path.join("output/exported_videos", case["filename"])
        safe_query = case['query'].encode('ascii', 'ignore').decode('ascii')
        print(f"Generating for {safe_query} at {path}...")
        start_t = time.time()
        
        # Generate script using AI with retry logic
        script = await ai_gen.generate_with_retry(case["query"])
        
        # Render using the provider (will use mock mode if no API key)
        await provider.render_video(case["query"], script, path)
        
        print(f"Successfully created {path} in {time.time() - start_t:.2f}s")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(generate_mock_videos())
