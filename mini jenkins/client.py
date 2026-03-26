"""
Mini Jenkins Client - Python client library for REST API
"""

import requests
import json
from typing import Dict, List, Optional


class MiniJenkinsClient:
    """Client for interacting with Mini Jenkins API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    # ============ JOB METHODS ============
    
    def create_job(self, name: str, description: str = "") -> Dict:
        """Create a new job"""
        response = self.session.post(
            f"{self.base_url}/api/jobs",
            json={"name": name, "description": description}
        )
        return response.json()
    
    def list_jobs(self) -> List[Dict]:
        """List all jobs"""
        response = self.session.get(f"{self.base_url}/api/jobs")
        return response.json()["jobs"]
    
    def get_job(self, job_id: str) -> Dict:
        """Get job details"""
        response = self.session.get(f"{self.base_url}/api/jobs/{job_id}")
        return response.json()["job"]
    
    def add_step(self, job_id: str, command: str) -> Dict:
        """Add a step to a job"""
        response = self.session.post(
            f"{self.base_url}/api/jobs/{job_id}/steps",
            json={"command": command}
        )
        return response.json()
    
    def run_job(self, job_id: str) -> Dict:
        """Run a job"""
        response = self.session.post(f"{self.base_url}/api/jobs/{job_id}/run")
        return response.json()["result"]
    
    def get_job_history(self, job_id: str) -> List[Dict]:
        """Get build history for a job"""
        response = self.session.get(f"{self.base_url}/api/jobs/{job_id}/history")
        return response.json()["history"]
    
    def delete_job(self, job_id: str) -> Dict:
        """Delete a job"""
        response = self.session.delete(f"{self.base_url}/api/jobs/{job_id}")
        return response.json()
    
    # ============ PIPELINE METHODS ============
    
    def create_pipeline(self, name: str) -> Dict:
        """Create a new pipeline"""
        response = self.session.post(
            f"{self.base_url}/api/pipelines",
            json={"name": name}
        )
        return response.json()
    
    def list_pipelines(self) -> List[Dict]:
        """List all pipelines"""
        response = self.session.get(f"{self.base_url}/api/pipelines")
        return response.json()["pipelines"]
    
    def add_stage(self, pipeline_id: str, stage_name: str, steps: List[str]) -> Dict:
        """Add a stage to a pipeline"""
        response = self.session.post(
            f"{self.base_url}/api/pipelines/{pipeline_id}/stages",
            json={"stage_name": stage_name, "steps": steps}
        )
        return response.json()
    
    def run_pipeline(self, pipeline_id: str) -> Dict:
        """Run a pipeline"""
        response = self.session.post(
            f"{self.base_url}/api/pipelines/{pipeline_id}/run"
        )
        return response.json()["result"]
    
    # ============ STATISTICS METHODS ============
    
    def get_stats(self) -> Dict:
        """Get overall statistics"""
        response = self.session.get(f"{self.base_url}/api/stats")
        return response.json()
    
    def get_dashboard(self) -> Dict:
        """Get dashboard data"""
        response = self.session.get(f"{self.base_url}/api/dashboard")
        return response.json()
    
    def health_check(self) -> Dict:
        """Check API health"""
        response = self.session.get(f"{self.base_url}/api/health")
        return response.json()


# Example usage
if __name__ == "__main__":
    client = MiniJenkinsClient()
    
    print("Mini Jenkins Client Example")
    print("="*50)
    
    # Check health
    print("\n1. Health Check:")
    health = client.health_check()
    print(f"   Status: {health['status']}")
    
    # Create a job
    print("\n2. Creating job:")
    job = client.create_job("Test Job", "Sample build job")
    print(f"   Job ID: {job['job']['job_id']}")
    print(f"   Name: {job['job']['name']}")
    
    # Add steps
    print("\n3. Adding steps:")
    client.add_step(job['job']['job_id'], "echo 'Step 1'")
    client.add_step(job['job']['job_id'], "echo 'Step 2'")
    print("   Steps added")
    
    # Get dashboard
    print("\n4. Dashboard:")
    dashboard = client.get_dashboard()
    print(f"   Total Jobs: {dashboard['total_jobs']}")
    print(f"   Total Pipelines: {dashboard['total_pipelines']}")
