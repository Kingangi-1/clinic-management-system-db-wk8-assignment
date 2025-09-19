
-- Creating the database ----

CREATE DATABASE Clinic_Booking_System;
use Clinic_Booking_System;

-- creating tables

CREATE Table patients(
patient_id int auto_increment primary key,
first_name varchar(50) not null,
last_name varchar(50) not null,
date_of_birth date not null, 
gender enum('Male', 'female', 'other') not null, 
phone varchar(20) unique,
email varchar(100) unique,  
created_at timestamp default current_timestamp
);

CREATE Table doctors(
doctor_id int auto_increment primary key,
first_name varchar(50) not null,
last_name varchar(50) not null,
date_of_birth date not null, 
gender enum('Male', 'female', 'other') not null, 
phone varchar(20) unique,
email varchar(100) unique,  
created_at timestamp default current_timestamp
);
-- table appointment (one-to-many; Patients to appointments, doctors to appointments

CREATE table appointments(
appointment_id int auto_increment primary key,
patient_id int not null, 
doctor_id int not null,
appointment_date DATETIME not null,
status ENUM('scheduled', 'completed', 'cancelled') default 'scheduled',
notes text,
foreign key (patient_id) references patients(patient_id),
foreign key (doctor_id) references doctors(doctor_id)
);

-- table treatments (many-to-many relationship)

CREATE TABLE treatments(
treatment_id int auto_increment primary key,
treatment_name varchar(100) not null unique,
treatment_description text,
cost decimal(10,2) not null
);

-- table appointment_treatment (many-many-relationship)
CREATE TABLE appointment_treatments (
    appointment_treatment_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    treatment_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),
    FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id),
    UNIQUE (appointment_id, treatment_id) -- Prevent duplicate entries
);

-- table payments (one-to-many relationship

CREATE TABLE payments(
payment_id int auto_increment primary key,
appointment_id int not null, 
amount decimal (10,2) not null,
payment_date timestamp default current_timestamp,
method enum('cash', 'card','m-pesa','insuarance') not null,
foreign key (appointment_id) references appointment (appointment_id)
 );
 
 -- Table admins for staff 
 
 CREATE TABLE admin(
  admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('Receptionist','Manager','Accountant') DEFAULT 'Receptionist'
 );
 
Select * from payments;