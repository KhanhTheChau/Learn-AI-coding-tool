from src.repositories.job_repository import InMemoryJobRepository
from src.ai.video_generator import AIVideoGenerator
from src.pipeline.video_assembler import VideoAssembler

# Global instances
_job_repository = InMemoryJobRepository()
_ai_video_generator = AIVideoGenerator()
_video_assembler = VideoAssembler()

def get_job_repository() -> InMemoryJobRepository:
    return _job_repository

def get_ai_video_generator() -> AIVideoGenerator:
    return _ai_video_generator

def get_video_assembler() -> VideoAssembler:
    return _video_assembler
