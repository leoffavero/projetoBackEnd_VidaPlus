from app.database import Base, engine
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.user import User
from app.models.appointment import Appointment

print("Apagando todas as tabelas...")
Base.metadata.drop_all(bind=engine)

print("Criando todas as tabelas...")
Base.metadata.create_all(bind=engine)

print("Banco de dados resetado com sucesso!")
