from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from job_manager import JobManager
from typing import Dict, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobScheduler:
    """Manages scheduled job execution"""
    
    def __init__(self, job_manager: JobManager):
        self.job_manager = job_manager
        self.scheduler = BackgroundScheduler()
        self.scheduled_jobs: Dict[str, str] = {}  # job_id -> schedule_id
    
    def schedule_job(self, job_id: str, cron_expression: str) -> bool:
        """
        Schedule a job with a cron expression
        
        Examples:
        - "0 0 * * *" - every day at midnight
        - "0 */6 * * *" - every 6 hours
        - "0 9 * * MON" - every Monday at 9 AM
        - "*/15 * * * *" - every 15 minutes
        """
        job = self.job_manager.get_job(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return False
        
        try:
            if not self.scheduler.running:
                self.scheduler.start()
            
            schedule_id = f"{job_id}_scheduled"
            
            # Remove existing schedule if present
            if schedule_id in self.scheduled_jobs:
                self.scheduler.remove_job(schedule_id)
            
            self.scheduler.add_job(
                func=self.job_manager.run_job,
                args=(job_id,),
                trigger=CronTrigger.from_crontab(cron_expression),
                id=schedule_id,
                name=f"Scheduled: {job.name}",
                replace_existing=True
            )
            
            self.scheduled_jobs[job_id] = schedule_id
            logger.info(f"Scheduled job {job_id} with cron: {cron_expression}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to schedule job {job_id}: {str(e)}")
            return False
    
    def unschedule_job(self, job_id: str) -> bool:
        """Unschedule a job"""
        if job_id not in self.scheduled_jobs:
            return False
        
        try:
            schedule_id = self.scheduled_jobs[job_id]
            self.scheduler.remove_job(schedule_id)
            del self.scheduled_jobs[job_id]
            logger.info(f"Unscheduled job {job_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to unschedule job {job_id}: {str(e)}")
            return False
    
    def list_scheduled_jobs(self):
        """List all scheduled jobs"""
        if not self.scheduler.running:
            return []
        
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "trigger": str(job.trigger),
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None
            })
        return jobs
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
