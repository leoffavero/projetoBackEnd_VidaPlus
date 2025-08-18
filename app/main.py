from app.database import Base, engine
from app.models import user, patient, doctor, appointment
import sys
import os
from fastapi import FastAPI
from app.routes import patient_routes, doctor_routes, appointment_routes, report_routes

app = FastAPI()
#resgitra as rotas
app.include_router(patient_routes.router, tags=["Patients"])
app.include_router(doctor_routes.router, tags=["Doctors"])
app.include_router(appointment_routes.router, tags=["Appointments"])
app.include_router(report_routes.router, tags=["Reports"])


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Creating tables...")
Base.metadata.create_all(bind=engine)
