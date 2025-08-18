from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.schemas.appointment_schema import DoctorReport, PatientReport, SpecialtyReport

router = APIRouter()

# Relatório por Médico
@router.get("/reports/by-doctor", response_model=list[DoctorReport])
def report_by_doctor(db: Session = Depends(get_db)):
    results = (
        db.query(
            Doctor.name.label("doctor_name"),
            Doctor.specialty.label("specialty"),
            func.count(Appointment.id).label("total_appointments")
        )
        .join(Appointment, Appointment.doctor_id == Doctor.id)
        .group_by(Doctor.id)
        .all()
    )

    # Converte cada linha do SQLAlchemy em DoctorReport
    return [
        DoctorReport(
            doctor_name=r.doctor_name,
            specialty=r.specialty,
            total_appointments=r.total_appointments
        )
        for r in results
    ]

# Relatório por Paciente
@router.get("/reports/by-patient", response_model=list[PatientReport])
def report_by_patient(db: Session = Depends(get_db)):
    results = (
        db.query(
            Patient.name.label("patient_name"),
            func.count(Appointment.id).label("total_appointments")
        )
        .join(Appointment, Appointment.patient_id == Patient.id)
        .group_by(Patient.id)
        .all()
    )

    return [
        PatientReport(
            patient_name=r.patient_name,
            total_appointments=r.total_appointments
        )
        for r in results
    ]

# Relatório por Especialidade
@router.get("/reports/by-specialty", response_model=list[SpecialtyReport])
def report_by_specialty(db: Session = Depends(get_db)):
    results = (
        db.query(
            Doctor.specialty.label("specialty"),
            func.count(Appointment.id).label("total_appointments")
        )
        .join(Appointment, Appointment.doctor_id == Doctor.id)
        .group_by(Doctor.specialty)
        .all()
    )

    return [
        SpecialtyReport(
            specialty=r.specialty,
            total_appointments=r.total_appointments
        )
        for r in results
    ]
