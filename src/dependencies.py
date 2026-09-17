from src.repositories.job_repository import InMemoryJobRepository

# Global instance
_job_repository = InMemoryJobRepository()

def get_job_repository() -> InMemoryJobRepository:
    return _job_repository
