import asyncio
from src.pipeline.video_assembler import VideoAssembler
import os
import time

async def generate_mock_videos():
    assembler = VideoAssembler()
    
    test_cases = [
        {
            "filename": "demo_test1_short.mp4",
            "query": "What is pH?",
            "script": "pH is a measure of acidity."
        },
        {
            "filename": "demo_test2_medium.mp4",
            "query": "How does ionic bond work?",
            "script": "Ionic bonding is the complete transfer of valence electron(s) between atoms. It is a type of chemical bond that generates two oppositely charged ions."
        },
        {
            "filename": "demo_test3_long.mp4",
            "query": "Explain covalent bonding in detail",
            "script": "A covalent bond is a chemical bond that involves the sharing of electron pairs between atoms. These electron pairs are known as shared pairs or bonding pairs. The stable balance of attractive and repulsive forces between atoms, when they share electrons, is known as covalent bonding. For many molecules, the sharing of electrons allows each atom to attain the equivalent of a full valence shell, corresponding to a stable electronic configuration."
        },
        {
            "filename": "demo_test4_unicode.mp4",
            "query": "Thang đo pH là gì?",
            "script": "Thang đo pH là thước đo mức độ axit hoặc bazơ của một dung dịch. Nó thường chạy từ 0 đến 14, trong đó 7 là trung tính. Nước tinh khiết có pH bằng 7. Các chất có pH dưới 7 có tính axit, và các chất có pH trên 7 có tính kiềm."
        }
    ]
    
    os.makedirs("output/exported_videos", exist_ok=True)
    
    for case in test_cases:
        path = os.path.join("output/exported_videos", case["filename"])
        print(f"Generating for {case['query']} at {path}...")
        start_t = time.time()
        await assembler.assemble_video(case["query"], case["script"], path)
        print(f"Successfully created {path} in {time.time() - start_t:.2f}s")

if __name__ == "__main__":
    asyncio.run(generate_mock_videos())
