import os, subprocess, shutil

class Browser:
  def __init__(self, username):
    self.username = username
    self.currDir = f'./users/{username}'
  
  def browseProjects(self):
    while True:
      os.system('clear' if os.name == 'posix' else 'cls')
      print("----- USAGE -----")
      print("To create a directory, type mk + PROJECT_NAME")
      print("To create a file within a project, type cr + FILE_NAME")
      print("To open a file or directory, type op + FILE_NAME")
      print("To remove a path, type rm + FILE_NAME")
      print("Type ex to go back")
      print("-----------------")
      print(f"Current directory: {self.currDir}")
      files = os.listdir(self.currDir)
      if len(files) == 0:
        print("No files created yet")
      else:
        for path in files:
          print(path)

      command = input().split(" ")
      if command[0] == "ex":
        if self.currDir == f"./users/{self.username}":
          break
        else:
          for i in range(len(self.currDir) - 1, 0, -1):
            lastChar = self.currDir[i]
            if lastChar == "/":
              self.currDir = self.currDir[0:i]
              break
      elif command[0] not in ["mk", "cr", "op", "rm"] or len(command) != 2:
        print("Command not valid")
      elif command[0] == "mk":
        self.createProject(command[1])
      elif command[0] == "cr":
        self.createFile(command[1])
      elif command[0] == "op":
        self.moveToProject(command[1])
      elif command[0] == "rm":
        self.removePath(command[1])     

  def createProject(self, name):
    # pathname = f"{self.currDir}/{name}"
    # if not os.path.isdir(pathname):
    #   return print("Invalid directory name")
    try:
      os.mkdir(f"{self.currDir}/{name}")
    except:
      print("Project name already exists or invalid name format")

  def createFile(self, name):
    pathname = f"{self.currDir}/{name}"
    if self.currDir == f"./users/{self.username}":
      print("You must be inside a directory to create a file")
    elif os.path.exists(pathname):
      print("File already exists")
    else:
      open(pathname, "x")

  
  def moveToProject(self, name):
    pathname = f"{self.currDir}/{name}"
    if os.path.exists(pathname):
      if os.path.isfile(pathname):
        subprocess.run(['python', './scripts/editor.py', pathname])
      else:
        self.currDir = pathname
    else:
      print("Path doesn't exist")
  
  def removePath(self, name):
    pathname = f"{self.currDir}/{name}"
    try:
      os.remove(pathname)
    except FileNotFoundError:
      print("File doesn't exist")
    except OSError:
      ans = input("Do you want to remove the whole directory? (y/n)\n")
      if ans.lower() == 'y':
        try:
          shutil.rmtree(pathname)
        except FileNotFoundError:
          print("Directory doesn't exist")
        except OSError:
          print("Couldn't delete directory")

