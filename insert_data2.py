from app.database import SessionLocal
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from datetime import date, datetime

# Criar sessão
db = SessionLocal()

try:
    # Criar usuários
    user1 = User(username="admin", password="1234")
    user2 = User(username="john_doe", password="abcd")

    # Criar médicos
    doctor1 = Doctor(name="Dr. House", crm="12345", specialty="Diagnóstico")
    doctor2 = Doctor(name="Dra. Grey", crm="67890", specialty="Cirurgia Geral")

    # Criar pacientes
    patient1 = Patient(name="Maria Silva", birthdate=date(1985, 5, 10))
    patient2 = Patient(name="João Souza", birthdate=date(1992, 8, 25))

    # Criar consultas
    appointment1 = Appointment(
        patient=patient1,
        doctor=doctor1,
        date=datetime(2025, 8, 15, 10, 0),
        description="Consulta de rotina"
    )
    appointment2 = Appointment(
        patient=patient2,
        doctor=doctor2,
        date=datetime(2025, 8, 16, 14, 30),
        description="Revisão pós-operatória"
    )

    # Adicionar tudo na sessão
    db.add_all([user1, user2, doctor1, doctor2, patient1, patient2, appointment1, appointment2])

    # Confirmar no banco
    db.commit()
    print("✅ Dados inseridos com sucesso!")

except Exception as e:
    print("❌ Erro ao inserir dados:", e)
    db.rollback()

finally:
    db.close()
