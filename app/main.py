from app.database import Base, engine
from app.models import user, patient, doctor, appointment
import sys
import os
from fastapi import FastAPI
from app.routes import patient_routes, doctor_routes, appointment_routes

app = FastAPI()
#resgitra as rotas
app.include_router(patient_routes.router)
app.include_router(doctor_routes.router)
app.include_router(appointment_routes.router)


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Creating tables...")
Base.metadata.create_all(bind=engine)
