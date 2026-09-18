from src.repositories.job_repository import InMemoryJobRepository
from src.ai.video_generator import AIVideoGenerator
from src.pipeline.third_party_provider import ThirdPartyVideoProvider

# Global instances
_job_repository = InMemoryJobRepository()
_ai_video_generator = AIVideoGenerator()
_video_provider = ThirdPartyVideoProvider()

def get_job_repository() -> InMemoryJobRepository:
    return _job_repository

def get_ai_video_generator() -> AIVideoGenerator:
    return _ai_video_generator

def get_video_provider() -> ThirdPartyVideoProvider:
    return _video_provider
