from pydantic import BaseModel
from datetime import datetime

class AppointmentBase(BaseModel):
    date: datetime
    reason: str
    patient_id: int
    doctor_id: int

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
