import subprocess, os
from scripts.auth import register, login, User
from scripts.browser import Browser

class App:
  def __init__(self):
    # self.user = None
    self.user = User("moncho", "test")
    self.browser = None
    self.printMenu()
  
  def printMenu(self):
    while self.user == None:
      os.system('clear' if os.name == 'posix' else 'cls')
      print("1. Login")
      print("2. Register")
      print("3. Exit program")
      num = int(input())
      if num == 1:
        self.user = login()
      elif num == 2:
        self.user = register()
      elif num == 3:
        return
    
    self.browser = Browser(self.user.username)
    print(f"Logged in as: {self.user.username}")
    while True:
      os.system('clear' if os.name == 'posix' else 'cls')
      print("1. Browse projects")
      print("2. Quit program")
      num = int(input())
      if num == 1:
        # subprocess.run(['python', './scripts/editor.py', 'noname.txt'])
        # subprocess.run('ls', shell=True)
        # projects = os.listdir(f'./users/{self.user.username}')
        self.browser.browseProjects()
      elif num == 2:
        break

App()