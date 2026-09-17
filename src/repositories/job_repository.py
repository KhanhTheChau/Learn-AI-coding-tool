from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from src.models.job import Job

class JobRepository(ABC):
    @abstractmethod
    def create(self, job: Job) -> Job:
        pass

    @abstractmethod
    def get(self, job_id: str) -> Optional[Job]:
        pass

    @abstractmethod
    def update(self, job: Job) -> Job:
        pass

    @abstractmethod
    def list(self) -> List[Job]:
        pass

class InMemoryJobRepository(JobRepository):
    def __init__(self) -> None:
        self._storage: Dict[str, Job] = {}

    def create(self, job: Job) -> Job:
        self._storage[job.id] = job
        return job

    def get(self, job_id: str) -> Optional[Job]:
        return self._storage.get(job_id)

    def update(self, job: Job) -> Job:
        if job.id not in self._storage:
            raise ValueError(f"Job with id {job.id} not found.")
        self._storage[job.id] = job
        return job

    def list(self) -> List[Job]:
        return list(self._storage.values())
