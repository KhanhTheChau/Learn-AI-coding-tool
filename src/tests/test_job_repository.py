import pytest
from src.models.job import Job, JobStatus
from src.repositories.job_repository import InMemoryJobRepository

def test_in_memory_repository_create() -> None:
    repo = InMemoryJobRepository()
    job = Job(query="Create a video about water")
    
    created_job = repo.create(job)
    assert created_job.id == job.id
    assert created_job.query == "Create a video about water"
    assert created_job.status == JobStatus.PENDING

def test_in_memory_repository_get() -> None:
    repo = InMemoryJobRepository()
    job = Job(query="Test query")
    repo.create(job)
    
    fetched_job = repo.get(job.id)
    assert fetched_job is not None
    assert fetched_job.id == job.id
    
    # Not found
    assert repo.get("invalid_id") is None

def test_in_memory_repository_update() -> None:
    repo = InMemoryJobRepository()
    job = Job(query="Test")
    repo.create(job)
    
    job.status = JobStatus.PROCESSING
    updated_job = repo.update(job)
    
    assert updated_job.status == JobStatus.PROCESSING
    
    fetched_job = repo.get(job.id)
    assert fetched_job is not None
    assert fetched_job.status == JobStatus.PROCESSING

def test_in_memory_repository_update_not_found() -> None:
    repo = InMemoryJobRepository()
    job = Job(query="Test")
    
    with pytest.raises(ValueError, match="not found"):
        repo.update(job)

def test_in_memory_repository_list() -> None:
    repo = InMemoryJobRepository()
    assert len(repo.list()) == 0
    
    repo.create(Job(query="Job 1"))
    repo.create(Job(query="Job 2"))
    
    jobs = repo.list()
    assert len(jobs) == 2
