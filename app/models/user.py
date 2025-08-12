from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class UserType(enum.Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    person_id = Column(Integer, nullable=True)  # Referência cruzada com paciente ou médico
