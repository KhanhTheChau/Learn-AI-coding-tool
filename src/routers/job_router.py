from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from src.models.job import Job, JobCreateRequest, JobStatus
from src.repositories.job_repository import JobRepository
from src.services.video_service import process_video_job
from src.dependencies import get_job_repository

router = APIRouter(prefix="/api/v1")

@router.post("/jobs", response_model=Job, status_code=status.HTTP_202_ACCEPTED)
async def submit_job(
    request: JobCreateRequest,
    background_tasks: BackgroundTasks,
    repo: JobRepository = Depends(get_job_repository)
):
    """Submit a new video generation job."""
    job = Job(query=request.query)
    repo.create(job)
    
    background_tasks.add_task(process_video_job, job.id, repo)
    return job

@router.get("/jobs", response_model=List[Job])
def get_all_jobs(repo: JobRepository = Depends(get_job_repository)):
    """Get all jobs."""
    return repo.list()

@router.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str, repo: JobRepository = Depends(get_job_repository)):
    """Get a job by its ID."""
    job = repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/videos/{job_id}")
def get_video(job_id: str, repo: JobRepository = Depends(get_job_repository)):
    """Get the video artifact for a job."""
    job = repo.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if not job.artifact_path:
        raise HTTPException(status_code=404, detail="Video is not available yet")
        
    return {"message": f"Video is available at {job.artifact_path}"}
