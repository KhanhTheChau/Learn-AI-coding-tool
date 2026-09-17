from src.repositories.job_repository import InMemoryJobRepository
from src.ai.video_generator import AIVideoGenerator

# Global instances
_job_repository = InMemoryJobRepository()
_ai_video_generator = AIVideoGenerator()

def get_job_repository() -> InMemoryJobRepository:
    return _job_repository

def get_ai_video_generator() -> AIVideoGenerator:
    return _ai_video_generator
