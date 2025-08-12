from app.database import Base, engine
from app.models import user, patient, doctor, appointment
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Creating tables...")
Base.metadata.create_all(bind=engine)
