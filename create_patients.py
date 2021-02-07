import hashlib
from main import db, Patient, SALT, create_patient
from random import *
import names

patients = []

# HELPER FUNCTIONS START #

def create_dob():
  month = str(randint(1,12))
  day = str(randint(1,28))
  year = str(randint(1950, 2002))

  dob = month + "/" + day + "/" + year
  
  return dob

def create_phone(f_name, l_name):
  phone = str(randint(0000000000, 9999999999))
  return phone

def create_password():
  password = randint(10000000, 999999999)
  return str(password)

# HELPER FUNCTIONS END #

for i in range(100):
  f_name = names.get_first_name()
  l_name = names.get_last_name()

  try:
    phone = create_phone(f_name, l_name)
    pw = create_password()
    dob = create_dob()

    create_patient(f_name, l_name, phone, dob, pw=pw)
    patients.append([phone, pw])
  except:
    print("Creation of " + f_name + " " + l_name + " failed.")

count = str(len(patients))
print(count + " new patients created!")

# PRINT OUT NEW PATIENT DETAILS IN A FILE
out = open("./script-outputs/patients.txt", "a")

for patient in patients:
  out.write(patient[0] + " " + patient[1] + "\n")

print("New patient data added to output file!")