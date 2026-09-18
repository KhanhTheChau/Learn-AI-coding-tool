import asyncio
from src.pipeline.video_assembler import VideoAssembler
import os

async def generate_mock_videos():
    assembler = VideoAssembler()
    queries = ["Thang do pH", "Lien ket cong hoa tri", "Lien ket ion"]
    filenames = ["demo_ph.mp4", "demo_conghoatri.mp4", "demo_ion.mp4"]
    
    for q, fn in zip(queries, filenames):
        path = os.path.join("exported_videos", fn)
        print(f"Generating for {q} at {path}...")
        await assembler.assemble_video("Mock script for " + q, path)
        print(f"Successfully created {path}")

if __name__ == "__main__":
    asyncio.run(generate_mock_videos())
