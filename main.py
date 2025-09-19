from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Date, Enum, TIMESTAMP, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from datetime import datetime, date
from pydantic import BaseModel
import enum

# =========================
# Database Setup
# =========================
DATABASE_URL = "mysql+pymysql://root:Kazungu08@localhost/Clinic_Booking_System"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# Models
# =========================
class GenderEnum(str, enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    address = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    appointments = relationship("Appointment", back_populates="patient")


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    appointment_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="appointments")


# Create tables if not exist
Base.metadata.create_all(bind=engine)


# =========================
# Schemas
# =========================
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    dob: date
    gender: str
    phone: str
    email: str
    address: str


class AppointmentCreate(BaseModel):
    patient_id: int
    appointment_date: datetime = None


# =========================
# FastAPI App
# =========================
app = FastAPI(title="Clinic Booking System API")


# =========================
# Root Endpoint
# =========================
@app.get("/")
def root():
    return {"message": "✅ Clinic Booking System API is running!"}


# =========================
# CRUD for Patients
# =========================
@app.post("/patients")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        dob=patient.dob,
        gender=patient.gender,
        phone=patient.phone,
        email=patient.email,
        address=patient.address,
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {"message": "✅ Patient added successfully", "patient_id": new_patient.patient_id}


@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return [
        {
            "patient_id": p.patient_id,
            "first_name": p.first_name,
            "last_name": p.last_name,
            "dob": p.dob,
            "gender": p.gender,
            "phone": p.phone,
            "email": p.email,
            "address": p.address,
            "created_at": p.created_at,
        }
        for p in patients
    ]


@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="❌ Patient not found")
    return {
        "patient_id": patient.patient_id,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "dob": patient.dob,
        "gender": patient.gender,
        "phone": patient.phone,
        "email": patient.email,
        "address": patient.address,
        "created_at": patient.created_at,
    }


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="❌ Patient not found")
    db.delete(patient)
    db.commit()
    return {"message": "🗑️ Patient deleted successfully"}


# =========================
# CRUD for Appointments
# =========================
@app.post("/appointments")
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        appointment_date=appointment.appointment_date or datetime.utcnow(),
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return {"message": "✅ Appointment created", "appointment_id": new_appointment.appointment_id}


@app.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return [
        {
            "appointment_id": a.appointment_id,
            "patient_id": a.patient_id,
            "appointment_date": a.appointment_date,
        }
        for a in appointments
    ]
