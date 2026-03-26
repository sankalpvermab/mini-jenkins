from typing import Dict, List, Any
from datetime import datetime
import json


class Pipeline:
    """Represents a CI/CD pipeline with multiple stages"""
    
    def __init__(self, pipeline_id: str, name: str):
        self.pipeline_id = pipeline_id
        self.name = name
        self.stages: List[Dict[str, Any]] = []
        self.created_at = datetime.now()
        self.execution_history: List[Dict[str, Any]] = []
    
    def add_stage(self, stage_name: str, steps: List[str]) -> None:
        """Add a stage with multiple steps"""
        stage = {
            "name": stage_name,
            "steps": steps,
            "order": len(self.stages) + 1
        }
        self.stages.append(stage)
        print(f"Added stage '{stage_name}' with {len(steps)} step(s)")
    
    def execute(self) -> Dict[str, Any]:
        """Execute the entire pipeline"""
        execution_id = len(self.execution_history) + 1
        start_time = datetime.now()
        stage_results = []
        overall_success = True
        
        print(f"\n{'='*70}")
        print(f"Executing Pipeline: {self.name}")
        print(f"{'='*70}\n")
        
        for stage in self.stages:
            print(f">>> Stage: {stage['name']}")
            stage_output = []
            stage_success = True
            
            for i, step in enumerate(stage['steps'], 1):
                print(f"    [{i}/{len(stage['steps'])}] Running: {step}")
                
                import subprocess
                try:
                    result = subprocess.run(
                        step,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    stage_output.append({
                        "step": i,
                        "command": step,
                        "returncode": result.returncode,
                        "stdout": result.stdout[:500],  # Limit output
                        "stderr": result.stderr[:500]
                    })
                    
                    if result.returncode != 0:
                        stage_success = False
                        print(f"    [FAILED] Step {i} exited with code {result.returncode}")
                        break
                    else:
                        print(f"    [OK] Step {i} completed")
                
                except subprocess.TimeoutExpired:
                    stage_success = False
                    print(f"    [TIMEOUT] Step {i} exceeded timeout")
                    break
                except Exception as e:
                    stage_success = False
                    print(f"    [ERROR] {str(e)}")
                    break
            
            stage_results.append({
                "stage_name": stage['name'],
                "status": "success" if stage_success else "failed",
                "steps_count": len(stage['steps']),
                "output": stage_output
            })
            
            print(f"    Stage Status: {'SUCCESS' if stage_success else 'FAILED'}\n")
            
            if not stage_success:
                overall_success = False
                break  # Stop pipeline on failure
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        execution = {
            "execution_id": execution_id,
            "pipeline_id": self.pipeline_id,
            "pipeline_name": self.name,
            "status": "success" if overall_success else "failed",
            "stages_executed": len(stage_results),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "stage_results": stage_results
        }
        
        self.execution_history.append(execution)
        print(f"{'='*70}")
        print(f"Pipeline Result: {execution['status'].upper()}")
        print(f"Duration: {duration:.2f}s")
        print(f"{'='*70}\n")
        
        return execution
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert pipeline to dictionary"""
        return {
            "pipeline_id": self.pipeline_id,
            "name": self.name,
            "stages_count": len(self.stages),
            "created_at": self.created_at.isoformat(),
            "executions_count": len(self.execution_history),
            "stages": [{"name": s['name'], "steps_count": len(s['steps'])} for s in self.stages]
        }
