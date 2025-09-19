from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from database import Base
import enum

class GenderEnum(enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class Patients(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    phone = Column(String(20), unique=True)
    email = Column(String(100), unique=True)
    address = Column(String(255))

    appointments = relationship("Appointments", back_populates="patient")


class Appointments(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    doctor_id = Column(Integer, nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="Scheduled")
    notes = Column(Text)

    patient = relationship("Patients", back_populates="appointments")
