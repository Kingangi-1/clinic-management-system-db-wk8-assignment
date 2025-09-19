from sqlalchemy.orm import Session
import models, schemas

# ---- Patients ----
def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patients(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Patients).offset(skip).limit(limit).all()

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patients).filter(models.Patients.patient_id == patient_id).first()

def update_patient(db: Session, patient_id: int, patient: schemas.PatientCreate):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        for key, value in patient.dict().items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient

# ---- Appointments ----
def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointments(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Appointments).offset(skip).limit(limit).all()
