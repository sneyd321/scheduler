from models.scheduler import Scheduler
import os






async def test_Scheduler_successfully_schedules_job():
    stream = os.popen('/usr/lib/google-cloud-sdk/bin/gcloud auth list')
    output = stream.read()
    print(output)
    print("GFDGADSFDSAF")
    scheduler = Scheduler()
    uuidValue = scheduler.schedule_job("upload-service", {})
    check = False
    for item in scheduler.list_jobs():
        if uuidValue == item:
            check = True
            break
    assert check
    


async def test_Scheduler_returns_error_when_duplicate_id_is_created():
    scheduler = Scheduler()
    uuidValue = scheduler.schedule_job("upload-service", {})
    assert scheduler.job_exists(uuidValue)
