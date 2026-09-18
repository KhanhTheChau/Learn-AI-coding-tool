import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from src.main import app
from src.models.job import JobStatus
from src.dependencies import get_job_repository
from src.services.video_service import process_video_job

client = TestClient(app)

# --- 1. TEST API ENDPOINTS ---

@patch("src.routers.job_router.BackgroundTasks.add_task")
def test_submit_job_success(mock_add_task):
    response = client.post("/api/v1/jobs", json={"query": "A valid query here"})
    assert response.status_code == 202
    data = response.json()
    assert "id" in data
    assert data["query"] == "A valid query here"
    assert data["status"] == "PENDING"
    
    # Ensure background task was triggered
    mock_add_task.assert_called_once()

def test_submit_job_validation_error():
    # Query too short (< 5 chars)
    res_short = client.post("/api/v1/jobs", json={"query": "Hi"})
    assert res_short.status_code == 422
    
    # Query empty
    res_empty = client.post("/api/v1/jobs", json={"query": ""})
    assert res_empty.status_code == 422

def test_get_all_jobs():
    response = client.get("/api/v1/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_job_not_found():
    response = client.get("/api/v1/jobs/fake-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}

# --- 2. TEST BACKGROUND TASK (process_video_job) ---

@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_process_video_job_success(mock_sleep):
    # Setup
    repo = get_job_repository()
    # Mocking app context or just using the repo directly
    # Create a job manually
    from src.models.job import Job
    job = Job(query="Test video process")
    repo.create(job)
    
    # Execute the service directly
    from src.ai.video_generator import AIVideoGenerator
    from src.pipeline.video_assembler import VideoAssembler
    ai_gen = AsyncMock(spec=AIVideoGenerator)
    ai_gen.generate_with_retry.return_value = "Mock script"
    assembler = AsyncMock(spec=VideoAssembler)
    assembler.assemble_video.return_value = f"exported_videos/{job.id}.mp4"
    
    await process_video_job(job.id, repo, ai_gen, assembler)
    
    # Verify
    updated_job = repo.get(job.id)
    assert updated_job.status == JobStatus.COMPLETED
    assert updated_job.artifact_path == f"/static/videos/{job.id}.mp4"

@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_process_video_job_failure(mock_sleep):
    # Setup
    repo = get_job_repository()
    from src.models.job import Job
    job = Job(query="Test video process fail")
    repo.create(job)
    
    # Simulate a timeout or error inside AI service
    from src.ai.video_generator import AIVideoGenerator
    from src.pipeline.video_assembler import VideoAssembler
    ai_gen = AsyncMock(spec=AIVideoGenerator)
    ai_gen.generate_with_retry.side_effect = Exception("Simulated AI Error")
    assembler = AsyncMock(spec=VideoAssembler)
    
    # Execute (should catch exception and update state)
    await process_video_job(job.id, repo, ai_gen, assembler)
    
    # Verify State Machine resilience
    updated_job = repo.get(job.id)
    assert updated_job.status == JobStatus.FAILED
    assert updated_job.error_message == "Simulated AI Error"
