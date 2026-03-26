# Mini Jenkins - A Lightweight CI/CD System

A simplified implementation of Jenkins CI/CD system in Python with job execution, pipelines, scheduling, and REST API.

## Features

- **Job Management**: Create, configure, and run CI/CD jobs
- **Pipelines**: Multi-stage pipelines with sequential execution
- **Scheduling**: Schedule jobs with cron expressions
- **REST API**: Full RESTful API for integration
- **Build History**: Track and view build results
- **Statistics**: Real-time metrics and reporting
- **Web Dashboard**: Monitor builds and pipelines in real-time

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Running the Demo

See basic usage examples:

```bash
python demo.py
```

This will demonstrate:
- Creating and running jobs
- Building multi-stage pipelines
- Job scheduling
- Statistics and reporting

### 2. Starting the REST API Server

Start the Flask API server:

```bash
python api_server.py
```

The API will be available at `http://localhost:5000`

## Core Components

### Job (`job.py`)

Represents a single CI/CD job with steps:

```python
from job_manager import JobManager

manager = JobManager()
job = manager.create_job("Build App", "Compile and build")
job.add_step("python --version")
job.add_step("echo 'Building...'")

result = manager.run_job(job.job_id)
```

### Pipeline (`pipeline.py`)

Multi-stage pipeline execution:

```python
from pipeline import Pipeline

pipeline = Pipeline("pipeline-1", "CI/CD Pipeline")
pipeline.add_stage("Build", ["echo 'Building...'"])
pipeline.add_stage("Test", ["echo 'Testing...'"])
pipeline.add_stage("Deploy", ["echo 'Deploying...'"])

result = pipeline.execute()
```

### Job Scheduler (`scheduler.py`)

Schedule jobs with cron expressions:

```python
from scheduler import JobScheduler

scheduler = JobScheduler(manager)
scheduler.schedule_job(job.job_id, "0 0 * * *")  # Daily at midnight
scheduler.start()
```

## REST API Endpoints

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs` | List all jobs |
| POST | `/api/jobs` | Create a new job |
| GET | `/api/jobs/<job_id>` | Get job details |
| POST | `/api/jobs/<job_id>/steps` | Add step to job |
| POST | `/api/jobs/<job_id>/run` | Run a job |
| GET | `/api/jobs/<job_id>/history` | Get build history |
| DELETE | `/api/jobs/<job_id>` | Delete a job |

### Pipelines

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/pipelines` | List all pipelines |
| POST | `/api/pipelines` | Create a new pipeline |
| POST | `/api/pipelines/<pipeline_id>/stages` | Add stage to pipeline |
| POST | `/api/pipelines/<pipeline_id>/run` | Execute pipeline |

### Statistics & Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Overall statistics |
| GET | `/api/dashboard` | Dashboard data |
| GET | `/api/health` | Health check |

## API Examples

### Create a Job

```bash
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Build App",
    "description": "Compile application"
  }'
```

### Add Steps to Job

```bash
curl -X POST http://localhost:5000/api/jobs/job-1/steps \
  -H "Content-Type: application/json" \
  -d '{
    "command": "echo Building..."
  }'
```

### Run a Job

```bash
curl -X POST http://localhost:5000/api/jobs/job-1/run
```

### Get Job History

```bash
curl http://localhost:5000/api/jobs/job-1/history
```

### Get Statistics

```bash
curl http://localhost:5000/api/stats
```

### Create a Pipeline

```bash
curl -X POST http://localhost:5000/api/pipelines \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Full CI/CD"
  }'
```

### Add Stage to Pipeline

```bash
curl -X POST http://localhost:5000/api/pipelines/pipeline-1/stages \
  -H "Content-Type: application/json" \
  -d '{
    "stage_name": "Build",
    "steps": [
      "echo Building...",
      "python --version"
    ]
  }'
```

### Run Pipeline

```bash
curl -X POST http://localhost:5000/api/pipelines/pipeline-1/run
```

## Project Structure

```
mini-jenkins/
├── job.py              # Job model and execution
├── job_manager.py      # Job management
├── pipeline.py         # Pipeline definition and execution
├── scheduler.py        # Job scheduling with cron
├── api_server.py       # Flask REST API
├── demo.py             # CLI demonstration
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Job Status Values

- `idle`: Job ready to run
- `running`: Job currently executing
- `success`: Job completed successfully
- `failed`: Job failed during execution

## Build Output

Build results include:
- Status (success/failed)
- Start and end times
- Duration in seconds
- Step-by-step output (stdout, stderr, return codes)

## Cron Expression Examples

| Expression | Description |
|-----------|-------------|
| `0 0 * * *` | Every day at midnight |
| `0 */6 * * *` | Every 6 hours |
| `0 9 * * MON` | Every Monday at 9 AM |
| `*/15 * * * *` | Every 15 minutes |
| `0 12 * * 1-5` | Weekdays at noon |

## Error Handling

- Jobs handle timeouts (default 300s per job)
- Failed steps stop pipeline execution
- All errors are logged and returned in responses

## Future Enhancements

- [ ] Web UI Dashboard
- [ ] Artifact storage and retrieval
- [ ] Webhook triggers
- [ ] Email notifications
- [ ] User authentication
- [ ] Job triggers and dependencies
- [ ] Container support (Docker)
- [ ] Distributed agent support

## License

MIT

## Author

Mini Jenkins - Simplified CI/CD System
