from app.database import Base, engine
import sys
import os
from fastapi import FastAPI
from app.routes import patient_routes, doctor_routes, appointment_routes, report_routes

app = FastAPI()
#resgitra as rotas
app.include_router(patient_routes.router, prefix="/api", tags=["Patients"])
app.include_router(doctor_routes.router, prefix="/api", tags=["Doctors"])
app.include_router(appointment_routes.router, prefix="/api", tags=["Appointments"])
app.include_router(report_routes.router, prefix="/api", tags=["Reports"])


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Creating tables...")
Base.metadata.create_all(bind=engine)
