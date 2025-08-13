from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.doctor import Doctor
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DoctorCreate(BaseModel):
    name: str
    specialty: Optional[str] = None
    email: Optional[str] = None
    crm: Optional[str] = None  # Registro profissional

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    email: Optional[str] = None
    crm: Optional[str] = None


# Listar médicos
@router.get("/doctors")
def list_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()

# Criar médico
@router.post("/doctors")
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = Doctor(
        name=doctor.name,
        specialty=doctor.specialty,
        email=doctor.email,
        crm=doctor.crm
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return {"message": "Médico criado com sucesso!", "doctor": new_doctor}

# Atualizar médico
@router.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    for key, value in doctor.dict(exclude_unset=True).items():
        setattr(db_doctor, key, value)

    db.commit()
    db.refresh(db_doctor)
    return {"message": "Médico atualizado com sucesso!", "doctor": db_doctor}

# Deletar médico
@router.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    db.delete(db_doctor)
    db.commit()
    return {"message": "Médico deletado com sucesso!"}
