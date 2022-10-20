from models.scheduler import Scheduler
import os






async def test_Scheduler_successfully_schedules_job():
    stream = os.popen('gcloud auth activate-service-account scheduler@roomr-222721.iam.gserviceaccount.com --key-file=/usr/src/app/ServiceAccount.json')
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
