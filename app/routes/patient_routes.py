from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.patient import Patient

router = APIRouter()

# Função para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/patients")
def list_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return patients
