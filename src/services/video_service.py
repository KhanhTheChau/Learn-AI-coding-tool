import os
import logging
from src.models.job import JobStatus
from src.repositories.job_repository import JobRepository
from src.ai.video_generator import AIVideoGenerator
from src.pipeline.video_assembler import VideoAssembler

logger = logging.getLogger(__name__)

async def process_video_job(job_id: str, repo: JobRepository, ai_gen: AIVideoGenerator, assembler: VideoAssembler):
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
        logger.info(f"Job {job_id} transitioned to PROCESSING")
        
        # Sử dụng AIVideoGenerator (có sẵn cơ chế Retry và Validate)
        video_script = await ai_gen.generate_with_retry(job.query)
        
        # Tạo artifact path
        output_path = f"output/static/videos/{job_id}.mp4"
        relative_path = f"static/videos/{job_id}.mp4"
        absolute_path = os.path.join(os.getcwd(), output_path)
        
        # Ghép video bằng VideoAssembler
        await assembler.assemble_video(job.query, video_script, absolute_path)
        
        # Cập nhật status thành COMPLETED kèm artifact path
        job.status = JobStatus.COMPLETED
        job.artifact_path = f"/{relative_path}"
        repo.update(job)
        logger.info(f"Job {job_id} transitioned to COMPLETED. Artifact: {job.artifact_path}")
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        # QUAN TRỌNG: Đảm bảo job được đánh dấu FAILED nếu có lỗi
        job = repo.get(job_id)
        if job:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            repo.update(job)
