from app.database import SessionLocal
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker("pt_BR")

db = SessionLocal()

try:
#criar médicos
    doctors = []
    for _ in range(5):
        doctor = Doctor(
            name=fake.name(),
            crm=str(fake.random_int(min=10000, max=99999)),
            specialty=random.choice(["Cardiologia", "Ortopedia", "Pediatria", "Clínico Geral"]),
            email=fake.unique.email()
        )
        doctors.append(doctor)
        db.add(doctor)

#criar pacientes
    patients = []
    for _ in range(10):
        patient = Patient(
            name=fake.name(),
            cpf=fake.cpf(),
            email=fake.unique.email(),
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=90)
        )
        patients.append(patient)
        db.add(patient)

    db.commit()

#Criar consultas
    for _ in range(15):
        appointment = Appointment(
            patient_id=random.choice(patients).id,
            doctor_id=random.choice(doctors).id,
            date=datetime.now() + timedelta(days=random.randint(1, 30)),
            description=fake.sentence() 
        )
        db.add(appointment)

    db.commit()
    print("Dados aleatórios inseridos com sucesso!")

except Exception as e:
    print("Erro ao inserir dados:", e)
    db.rollback()

finally:
    db.close()
