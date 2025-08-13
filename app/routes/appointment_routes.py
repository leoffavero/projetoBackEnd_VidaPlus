from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.appointment_schema import AppointmentCreate, AppointmentResponse
from typing import List, Optional
from datetime import datetime

router = APIRouter()

@router.get("/appointments")
def get_appointments(
    db: Session = Depends(get_db),
    date: Optional[str] = Query(None, description="Filtra por data (YYYY-MM-DD)"),
    patient_name: Optional[str] = Query(None, description="Filtra pelo nome do paciente"),
    doctor_specialty: Optional[str] = Query(None, description="Filtra pela especialidade do médico")
):
    query = (
        db.query(
            Appointment.id,
            Appointment.date,
            Appointment.description,
            Patient.name.label("patient_name"),
            Doctor.name.label("doctor_name"),
            Doctor.specialty.label("doctor_specialty")
        )
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
    )

    # Aplica filtros se enviados
    if date:
        query = query.filter(Appointment.date.like(f"{date}%"))
    if patient_name:
        query = query.filter(Patient.name.ilike(f"%{patient_name}%"))
    if doctor_specialty:
        query = query.filter(Doctor.specialty.ilike(f"%{doctor_specialty}%"))

    results = query.all()

    return [
        {
            "id": r.id,
            "date": r.date,
            "description": r.description,
            "patient_name": r.patient_name,
            "doctor_name": r.doctor_name,
            "doctor_specialty": r.doctor_specialty
        }
        for r in results
    ]

@router.post("/appointments", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    # Verifica se o paciente existe
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Verifica se o médico existe
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    # Cria a consulta
    new_appointment = Appointment(
        date=appointment.date,
        description=appointment.description,
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment

@router.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(appointment_id: int, updated_data: AppointmentCreate, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    # Atualiza os dados
    appointment.date = updated_data.date
    appointment.description = updated_data.description
    appointment.patient_id = updated_data.patient_id
    appointment.doctor_id = updated_data.doctor_id

    db.commit()
    db.refresh(appointment)
    return appointment

@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    db.delete(appointment)
    db.commit()
    return {"message": "Consulta excluída com sucesso"}
