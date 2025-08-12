from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from app.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    notes = Column(Text)
