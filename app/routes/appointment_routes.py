from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.appointment import Appointment
from app.schemas.appointment_schema import AppointmentCreate, AppointmentResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    new_appointment = Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@router.get("/", response_model=List[AppointmentResponse])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).get(appointment_id)
    if appointment:
        db.delete(appointment)
        db.commit()
        return {"message": "Appointment deleted successfully"}
    return {"error": "Appointment not found"}
