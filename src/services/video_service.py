import asyncio
import logging
from src.models.job import JobStatus
from src.repositories.job_repository import JobRepository

logger = logging.getLogger(__name__)

async def process_video_job(job_id: str, repo: JobRepository):
    """
    Background task to process a video generation job.
    """
    try:
        # Lấy job ra
        job = repo.get(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return
            
        # Cập nhật status thành PROCESSING
        job.status = JobStatus.PROCESSING
        repo.update(job)
        
        # Giả lập logic sinh video AI tốn thời gian
        await asyncio.sleep(5)
        
        # Cập nhật status thành COMPLETED kèm artifact path giả lập
        job.status = JobStatus.COMPLETED
        job.artifact_path = f"https://dummy-bucket/videos/{job_id}.mp4"
        repo.update(job)
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        # QUAN TRỌNG: Đảm bảo job được đánh dấu FAILED nếu có lỗi
        job = repo.get(job_id)
        if job:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            repo.update(job)
