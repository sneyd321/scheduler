from fastapi import FastAPI
from models.scheduler import Scheduler
from models.schemas import  LeaseSchema, LeaseScheduleSchema, MaintenanceTicketUploadSchema, AddTenantEmailSchema, SignLeaseSchema
import uvicorn, os


app = FastAPI()
scheduler = Scheduler()

@app.get("/Health")
async def health_check():
    return {"status": 200}

@app.post("/SignLease")
async def sign_lease(request: SignLeaseSchema):
    scheduler.schedule_sign_lease_tenant(request.dict())
    return {"status": "Job scheduled successfully"}

@app.post("/AddTenantEmail")
async def add_tenant_email(request: AddTenantEmailSchema):
    scheduler.schedule_add_tenant_email_job(request.dict())
    return {"status": "Job scheduled successfully"}

@app.post("/Lease/Ontario")
async def create_lease(request: LeaseScheduleSchema):
    scheduler.schedule_lease_ticket_job(request.dict())
    return {"status": "Job scheduled successfully"}

@app.post('/MaintenanceTicket')
async def upload_maintenance_ticket(request: MaintenanceTicketUploadSchema):
    scheduler.schedule_maintenance_ticket_job(request.dict())
    return {"status": "Job scheduled successfully"}

if __name__ == '__main__':
    
    uvicorn.run(app, port=int(os.environ.get("PORT", 8084)))