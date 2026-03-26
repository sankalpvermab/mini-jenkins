#!/usr/bin/env python3
"""
Mini Jenkins Demo - Command Line Interface
Shows how to use the mini Jenkins system
"""

from job_manager import JobManager
from pipeline import Pipeline
from scheduler import JobScheduler


def demo_jobs(job_manager: JobManager):
    """Demonstrate job creation and execution"""
    print("\n" + "="*70)
    print("DEMO 1: Creating and Running Jobs")
    print("="*70 + "\n")
    
    # Create a build job
    build_job = job_manager.create_job("Build Python App", "Compile and build the application")
    build_job.add_step("echo 'Starting build...'")
    build_job.add_step("python --version")
    build_job.add_step("echo 'Build completed successfully!'")
    
    # Create a test job
    test_job = job_manager.create_job("Run Tests", "Execute unit tests")
    test_job.add_step("echo 'Running tests...'")
    test_job.add_step("python -m pytest --version")
    test_job.add_step("echo 'All tests passed!'")
    
    # Create a deploy job (this will fail for demo purposes)
    deploy_job = job_manager.create_job("Deploy App", "Deploy to production")
    deploy_job.add_step("echo 'Preparing deployment...'")
    deploy_job.add_step("echo 'Deploying to server...'")
    deploy_job.add_step("exit 1")  # Intentional failure
    
    print("\nRunning Build Job:")
    job_manager.run_job(build_job.job_id)
    
    print("\nRunning Test Job:")
    job_manager.run_job(test_job.job_id)
    
    print("\nRunning Deploy Job (will fail):")
    job_manager.run_job(deploy_job.job_id)


def demo_pipelines():
    """Demonstrate pipeline creation and execution"""
    print("\n" + "="*70)
    print("DEMO 2: Creating and Running Pipelines")
    print("="*70 + "\n")
    
    # Create a full CI/CD pipeline
    pipeline = Pipeline("pipeline-1", "Complete CI/CD Pipeline")
    
    # Add build stage
    pipeline.add_stage("Build", [
        "echo 'Building application...'",
        "python --version",
        "echo 'Build successful!'"
    ])
    
    # Add test stage
    pipeline.add_stage("Test", [
        "echo 'Running unit tests...'",
        "echo 'Tests passed!'",
        "echo 'Running integration tests...'",
        "echo 'All tests passed!'"
    ])
    
    # Add deploy stage
    pipeline.add_stage("Deploy", [
        "echo 'Preparing deployment...'",
        "echo 'Deployed to staging environment!'"
    ])
    
    # Execute the pipeline
    result = pipeline.execute()


def demo_scheduler(job_manager: JobManager):
    """Demonstrate job scheduling"""
    print("\n" + "="*70)
    print("DEMO 3: Job Scheduling")
    print("="*70 + "\n")
    
    # Create a simple job to schedule
    scheduled_job = job_manager.create_job("Scheduled Backup", "Backup database")
    scheduled_job.add_step("echo 'Backing up database...'")
    scheduled_job.add_step("echo 'Backup completed!'")
    
    # Initialize scheduler
    scheduler = JobScheduler(job_manager)
    
    # Schedule the job (every day at midnight)
    # NOTE: This won't actually run in this demo since we stop the scheduler
    scheduler.schedule_job(scheduled_job.job_id, "0 0 * * *")
    
    print(f"Job scheduled! View scheduled jobs:")
    scheduled = scheduler.list_scheduled_jobs()
    for job in scheduled:
        print(f"  - {job['name']}: {job['trigger']}")


def demo_stats(job_manager: JobManager):
    """Display statistics"""
    print("\n" + "="*70)
    print("DEMO 4: Statistics & Reporting")
    print("="*70 + "\n")
    
    stats = job_manager.get_statistics()
    print(f"Total Jobs: {stats['total_jobs']}")
    print(f"Total Builds: {stats['total_builds']}")
    print(f"Successful Builds: {stats['successful_builds']}")
    print(f"Failed Builds: {stats['failed_builds']}")
    print(f"Success Rate: {stats['success_rate']:.1f}%")
    
    print("\nAll Jobs:")
    for job in job_manager.list_jobs():
        print(f"  - {job['name']}: {job['status']} ({job['build_count']} builds)")


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("MINI JENKINS - DEMONSTRATION")
    print("="*70)
    
    # Initialize job manager
    job_manager = JobManager()
    
    # Run demos
    demo_jobs(job_manager)
    demo_pipelines()
    demo_scheduler(job_manager)
    demo_stats(job_manager)
    
    print("\n" + "="*70)
    print("DEMO COMPLETED!")
    print("="*70)
    print("\nTo start the REST API server, run:")
    print("  python api_server.py")
    print("\nAPI will be available at: http://localhost:5000")


if __name__ == "__main__":
    main()
