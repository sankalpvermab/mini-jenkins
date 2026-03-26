from typing import Dict, List, Optional
from job import Job, JobStatus


class JobManager:
    """Manages all jobs in mini Jenkins"""
    
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self.job_counter = 0
    
    def create_job(self, name: str, description: str = "") -> Job:
        """Create a new job"""
        self.job_counter += 1
        job_id = f"job-{self.job_counter}"
        job = Job(job_id, name, description)
        self.jobs[job_id] = job
        print(f"Created job: {name} (ID: {job_id})")
        return job
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get a job by ID"""
        return self.jobs.get(job_id)
    
    def list_jobs(self) -> List[Dict]:
        """List all jobs with their details"""
        return [job.to_dict() for job in self.jobs.values()]
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            print(f"Deleted job: {job_id}")
            return True
        return False
    
    def run_job(self, job_id: str) -> Optional[Dict]:
        """Run a specific job"""
        job = self.get_job(job_id)
        if not job:
            return None
        
        print(f"\n{'='*60}")
        print(f"Starting job: {job.name} (ID: {job_id})")
        print(f"{'='*60}")
        
        result = job.run()
        
        print(f"\n{'='*60}")
        print(f"Job completed! Status: {result['status']}")
        print(f"Duration: {result['duration_seconds']:.2f}s")
        print(f"{'='*60}\n")
        
        return result
    
    def get_job_history(self, job_id: str) -> List[Dict]:
        """Get build history for a job"""
        job = self.get_job(job_id)
        if not job:
            return []
        return job.build_history
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        total_jobs = len(self.jobs)
        total_builds = sum(len(job.build_history) for job in self.jobs.values())
        
        successful_builds = 0
        failed_builds = 0
        
        for job in self.jobs.values():
            for build in job.build_history:
                if build["status"] == JobStatus.SUCCESS.value:
                    successful_builds += 1
                elif build["status"] == JobStatus.FAILED.value:
                    failed_builds += 1
        
        return {
            "total_jobs": total_jobs,
            "total_builds": total_builds,
            "successful_builds": successful_builds,
            "failed_builds": failed_builds,
            "success_rate": (successful_builds / total_builds * 100) if total_builds > 0 else 0
        }
