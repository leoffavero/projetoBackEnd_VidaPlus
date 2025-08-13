from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Doctor(Base):
    __tablename__ = "doctors"
    appointments = relationship("Appointment", back_populates="doctor")

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    crm = Column(String(20), unique=True, nullable=False)
    specialty = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    
