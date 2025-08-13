from sqlalchemy import Column, Integer, String, Date
from app.database import Base
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = "patients"
    appointments = relationship("Appointment", back_populates="patient")

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    birth_date = Column(Date)
    