import subprocess
import json
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any


class JobStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class Job:
    """Represents a CI/CD job in mini Jenkins"""
    
    def __init__(self, job_id: str, name: str, description: str = ""):
        self.job_id = job_id
        self.name = name
        self.description = description
        self.status = JobStatus.IDLE
        self.steps: List[str] = []
        self.created_at = datetime.now()
        self.last_run = None
        self.build_history: List[Dict[str, Any]] = []
    
    def add_step(self, command: str) -> None:
        """Add a build step to the job"""
        self.steps.append(command)
    
    def run(self) -> Dict[str, Any]:
        """Execute the job and return the result"""
        self.status = JobStatus.RUNNING
        build_id = len(self.build_history) + 1
        start_time = datetime.now()
        output = []
        success = True
        
        try:
            for i, step in enumerate(self.steps, 1):
                print(f"[{self.name}] Executing step {i}/{len(self.steps)}: {step}")
                result = subprocess.run(
                    step,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                output.append({
                    "step": i,
                    "command": step,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                })
                
                if result.returncode != 0:
                    success = False
                    print(f"[{self.name}] Step {i} failed!")
                    break
            
            self.status = JobStatus.SUCCESS if success else JobStatus.FAILED
        
        except subprocess.TimeoutExpired:
            self.status = JobStatus.FAILED
            output.append({
                "error": "Build timeout exceeded"
            })
            success = False
        except Exception as e:
            self.status = JobStatus.FAILED
            output.append({
                "error": str(e)
            })
            success = False
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        build_result = {
            "build_id": build_id,
            "job_id": self.job_id,
            "job_name": self.name,
            "status": self.status.value,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "output": output
        }
        
        self.build_history.append(build_result)
        self.last_run = end_time
        self.status = JobStatus.IDLE
        
        return build_result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary"""
        return {
            "job_id": self.job_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "steps_count": len(self.steps),
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "created_at": self.created_at.isoformat(),
            "build_count": len(self.build_history)
        }
