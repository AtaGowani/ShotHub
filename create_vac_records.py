from main import db, vaccines, Patient, Vaccine
import random

patients_file = open("./script-outputs/patients.txt")

for patient_data in patients_file:
  if random.randint(0,10) < 8:
    continue

  cleaned_data = patient_data.strip("\n")
  phone = cleaned_data.split(" ")[0]

  vaccine = Vaccine.query.filter(Vaccine.id == 7).first()
  patient = Patient.query.filter(Patient.phone == phone).first()

  vaccine.patients.append(patient)
  db.session.commit()