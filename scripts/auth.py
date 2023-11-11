import csv, os

class User:
  def __init__(self, username, password):
    self.username = username
    self.password = password

def register():
  username = input("Enter desired username\n")
  password = input("Enter password\n")
  passwordConfirm = input("Confirm password\n")
  
  while password != passwordConfirm:
    print("Password and confirmation values don't match")
    password = input("Enter password\n")
    passwordConfirm = input("Confirm password\n")
  
  with open("./users/database.csv", newline='') as db:
    reader = csv.reader(db)
    for row in reader:
      currUser, _ = row
      if currUser == username:
        print("Username already exists")
        return None
  
  with open("./users/database.csv", "a", newline='') as db:
    writer = csv.writer(db)
    writer.writerow([username, password])
    os.mkdir(f'./users/{username}')
    return User(username, password)
  
def login():
  username = input("Enter username\n")
  password = input("Enter password\n")

  with open("./users/database.csv") as db:
    reader = csv.reader(db)
    for row in reader:
      currUser, currPass = row
      if currUser == username:
        if currPass == password:
          print(f"Login successful, welcome {username}")
          return User(username, password)
        else:
          print(f"Wrong password")
          return None
  
  print("User doesn't exist")
  return None
