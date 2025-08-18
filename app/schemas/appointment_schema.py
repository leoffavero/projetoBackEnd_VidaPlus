from pydantic import BaseModel
from datetime import datetime

class AppointmentBase(BaseModel):
    date: datetime
    description: str
    patient_id: int
    doctor_id: int

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        from_attributes = True

class AppointmentDetailResponse(BaseModel):
    id: int
    date: datetime
    description: str
    patient_name: str
    doctor_name: str
    doctor_specialty: str

    class Config:
        from_attributes = True

class DoctorReport(BaseModel):
    doctor_name: str
    specialty: str
    total_appointments: int

    class Config:
        from_attributes = True
        
class PatientReport(BaseModel):
    patient_name: str
    total_appointments: int

    class Config:
        from_attributes = True


class SpecialtyReport(BaseModel):
    specialty: str
    total_appointments: int

    class Config:
        from_attributes = True