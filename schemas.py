from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    dob: date
    gender: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    patient_id: int
    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    doctor_id: int
    appointment_date: datetime
    status: Optional[str] = "Scheduled"
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    patient_id: int

class Appointment(AppointmentBase):
    appointment_id: int
    patient_id: int
    class Config:
        orm_mode = True
