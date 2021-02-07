from os import name
from main import db, Vaccine

vac_file = open("vaccines.txt")

for vac in vac_file:
  cleaned_vac = vac.strip("\n")
  vaccine = cleaned_vac.split(",")

  try:
    vac_obj = Vaccine (
      name = vaccine[0],
      number_of_doses = vaccine[1]
    )

    db.session.add(vac_obj)
    db.session.commit()
    db.session.close()

    print(vaccine[0] + " added successfully")
  except:
    print("Vaccinee not added properly.")