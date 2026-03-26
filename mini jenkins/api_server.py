from flask import Flask, jsonify, request
from flask_cors import CORS
from job_manager import JobManager
from pipeline import Pipeline
import json

app = Flask(__name__)
CORS(app)

# Global job manager
job_manager = JobManager()
pipelines = {}
pipeline_counter = 0


# ============ JOB ENDPOINTS ============

@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all jobs"""
    return jsonify({
        "success": True,
        "jobs": job_manager.list_jobs()
    })


@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job"""
    data = request.json
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({"success": False, "error": "Job name required"}), 400
    
    job = job_manager.create_job(name, description)
    return jsonify({
        "success": True,
        "job": job.to_dict()
    }), 201


@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    """Get job details"""
    job = job_manager.get_job(job_id)
    if not job:
        return jsonify({"success": False, "error": "Job not found"}), 404
    
    return jsonify({
        "success": True,
        "job": job.to_dict()
    })


@app.route('/api/jobs/<job_id>/steps', methods=['POST'])
def add_step(job_id):
    """Add a build step to a job"""
    job = job_manager.get_job(job_id)
    if not job:
        return jsonify({"success": False, "error": "Job not found"}), 404
    
    data = request.json
    command = data.get('command')
    
    if not command:
        return jsonify({"success": False, "error": "Command required"}), 400
    
    job.add_step(command)
    return jsonify({
        "success": True,
        "message": f"Step added to job {job_id}"
    })


@app.route('/api/jobs/<job_id>/run', methods=['POST'])
def run_job(job_id):
    """Run a specific job"""
    job = job_manager.get_job(job_id)
    if not job:
        return jsonify({"success": False, "error": "Job not found"}), 404
    
    result = job_manager.run_job(job_id)
    return jsonify({
        "success": True,
        "result": result
    })


@app.route('/api/jobs/<job_id>/history', methods=['GET'])
def get_job_history(job_id):
    """Get build history for a job"""
    job = job_manager.get_job(job_id)
    if not job:
        return jsonify({"success": False, "error": "Job not found"}), 404
    
    return jsonify({
        "success": True,
        "job_id": job_id,
        "history": job_manager.get_job_history(job_id)
    })


@app.route('/api/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job"""
    success = job_manager.delete_job(job_id)
    if not success:
        return jsonify({"success": False, "error": "Job not found"}), 404
    
    return jsonify({"success": True, "message": "Job deleted"})


# ============ PIPELINE ENDPOINTS ============

@app.route('/api/pipelines', methods=['GET'])
def list_pipelines():
    """List all pipelines"""
    return jsonify({
        "success": True,
        "pipelines": [p.to_dict() for p in pipelines.values()]
    })


@app.route('/api/pipelines', methods=['POST'])
def create_pipeline():
    """Create a new pipeline"""
    global pipeline_counter
    
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({"success": False, "error": "Pipeline name required"}), 400
    
    pipeline_counter += 1
    pipeline_id = f"pipeline-{pipeline_counter}"
    pipeline = Pipeline(pipeline_id, name)
    pipelines[pipeline_id] = pipeline
    
    return jsonify({
        "success": True,
        "pipeline": pipeline.to_dict()
    }), 201


@app.route('/api/pipelines/<pipeline_id>/stages', methods=['POST'])
def add_stage(pipeline_id):
    """Add a stage to a pipeline"""
    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        return jsonify({"success": False, "error": "Pipeline not found"}), 404
    
    data = request.json
    stage_name = data.get('stage_name')
    steps = data.get('steps', [])
    
    if not stage_name or not steps:
        return jsonify({"success": False, "error": "Stage name and steps required"}), 400
    
    pipeline.add_stage(stage_name, steps)
    return jsonify({
        "success": True,
        "message": f"Stage '{stage_name}' added to pipeline"
    })


@app.route('/api/pipelines/<pipeline_id>/run', methods=['POST'])
def run_pipeline(pipeline_id):
    """Execute a pipeline"""
    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        return jsonify({"success": False, "error": "Pipeline not found"}), 404
    
    result = pipeline.execute()
    return jsonify({
        "success": True,
        "result": result
    })


# ============ STATISTICS ENDPOINTS ============

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    stats = job_manager.get_statistics()
    
    pipeline_stats = {
        "total_pipelines": len(pipelines),
        "total_executions": sum(len(p.execution_history) for p in pipelines.values())
    }
    
    return jsonify({
        "success": True,
        "jobs": stats,
        "pipelines": pipeline_stats
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "message": "Mini Jenkins API is running"
    })


# ============ DASHBOARD ENDPOINTS ============

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Get dashboard data"""
    jobs_stats = job_manager.get_statistics()
    
    recent_builds = []
    for job in job_manager.jobs.values():
        if job.build_history:
            recent_builds.append(job.build_history[-1])
    
    recent_builds.sort(key=lambda x: x['end_time'], reverse=True)
    recent_builds = recent_builds[:10]  # Last 10 builds
    
    return jsonify({
        "success": True,
        "stats": jobs_stats,
        "recent_builds": recent_builds,
        "total_jobs": len(job_manager.jobs),
        "total_pipelines": len(pipelines)
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
