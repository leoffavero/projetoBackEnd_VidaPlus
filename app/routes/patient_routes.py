from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.patient import Patient
from pydantic import BaseModel
from typing import Optional
from datetime import date

router = APIRouter()

# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo Pydantic para criar paciente
class PatientCreate(BaseModel):
    name: str
    cpf: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[date] = None

# Modelo Pydantic para atualizar paciente
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[date] = None


# ===================== ROTAS =====================

# Listar pacientes
@router.get("/patients")
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

# Criar paciente
@router.post("/patients")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = Patient(
        name=patient.name,
        cpf=patient.cpf,
        email=patient.email,
        birth_date=patient.birth_date
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {"message": "Paciente criado com sucesso!", "patient": new_patient}

# Atualizar paciente
@router.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Atualiza apenas os campos enviados
    for key, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return {"message": "Paciente atualizado com sucesso!", "patient": db_patient}

# Deletar paciente
@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    db.delete(db_patient)
    db.commit()
    return {"message": "Paciente deletado com sucesso!"}
