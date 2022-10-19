from models.scheduler import Scheduler
import time

scheduler = Scheduler()


async def test_Scheduler_successfully_schedules_job():
    uuidValue = scheduler.schedule_job("upload-service", {})
    check = False
    for item in scheduler.list_jobs():
        if uuidValue == item:
            check = True
            break
    assert check
    


async def test_Scheduler_returns_error_when_duplicate_id_is_created():
    uuidValue = scheduler.schedule_job("upload-service", {})
    assert scheduler.job_exists(uuidValue)
