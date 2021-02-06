from main import db, Technician
from random import *
import names

full_names = []
companies = ["Walmart", "HEB", "Walgreens", "CVS", "Rite Aid"]
technicians = []

# HELPER FUNCTIONS START #

def create_username(f_name, l_name):
  username = f_name[0] + l_name + str(randint(0, 7000))
  return username

def create_password():
  password = randint(10000000, 999999999)
  return str(password)

# HELPER FUNCTIONS END #

for i in range(100):
  f_name = names.get_first_name()
  l_name = names.get_last_name()

  try:
    # creating Users object
    user = Technician (
      f_name = f_name,
      l_name = l_name,
      username = create_username(f_name, l_name),
      pw = create_password(),
      company = companies[randint(0, len(companies)-1)]
    )

    technicians.append(user)

    # adding the fields to users table
    # db.session.add(user)
    # db.session.commit()


  except:
    print("Creation of " + f_name + " " + l_name + " failed.")

count = str(len(technicians))
print(count + " new technicians created!")

# PRINT OUT NEW TECHNICIAN DETAILS IN A FILE
out = open("./script-outputs/technicians.txt", "a")

for tech in technicians:
  out.write(tech.username + " " + tech.pw + "\n")

print("New technician data added to output file!")