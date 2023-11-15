import subprocess, os, random
from scripts.auth import register, login, User
from scripts.browser import Browser
from scripts.error import error
from scripts.binary import Node, BinaryTree

class App:
  def __init__(self):
    # self.tree = BinaryTree()
    # self.tree.fill_tree()
    self.initTree()
    self.user = None
    #self.user = User("moncho", "test")
    self.browser = None
    self.printMenu()

  def initTree(self):
    self.tree = BinaryTree()
    self.tree.fill_tree()
  
  def printMenu(self):
    while self.user == None:
      os.system('clear' if os.name == 'posix' else 'cls')
      print("1. Login")
      print("2. Register")
      print("3. View current users")
      print("4. Exit program")
      num = int(input())
      if num == 1:
        self.user = login()
      elif num == 2:
        self.user = register()
        self.initTree()
      elif num == 3: 
        self.tree.print_in(self.tree.root, 0)
        ex = input(str("Press enter to go back\n"))
      elif num == 4:
        return
    
    self.browser = Browser(self.user.username, self.tree)
    while True:
      os.system('clear' if os.name == 'posix' else 'cls')
      print("1. Browse projects")
      print("2. Log out")
      print("3. Quit program")
      num = int(input())
      if num == 1:
        self.browser.browseProjects()
      elif num == 2:
        self.user = None
        return self.printMenu()
      elif num == 3:
        break

App()