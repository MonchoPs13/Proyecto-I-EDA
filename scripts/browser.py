import os, subprocess, shutil, time, csv, datetime, pathlib
from scripts.versionControl import VersionControl
from scripts.linear_sort import heapSort, get_time
class Browser:
  def __init__(self, username, tree):
    self.username = username
    self.tree = tree
    self.currDir = f'./users/{username}'
    self.versionC = None
  
  def browseProjects(self):
    while True:
      os.system('clear' if os.name == 'posix' else 'cls')
      print("----- USAGE -----")
      print("To create a directory, type mk + PROJECT_NAME")
      print("To create a file within a project, type cr + FILE_NAME")
      print("To open a file or directory, type op + FILE_NAME")
      print("To rename a file or directory, type rename + CURR_NAME + NEW_NAME")
      print("To remove a path, type rm + FILE_NAME")
      print("To commit changes, type commit + COMMIT_NAME")
      print("To create a new branch, type br + BRANCH_NAME")
      print("To switch to another branch, type bl")
      print("To merge branches, type merge + SRC_BRANCH + DEST_BRANCH")
      print("To revert changes to the previous commit, type revert")
      print("To add a friend to your list, type af")
      print("To check your collaborations, type collab")
      print("Type ex to go back")
      print("-----------------")
      print(f"Current directory: {self.currDir}")
      if self.versionC != None:
        print(f"Branch: {self.versionC.currBranch}")
      files = os.listdir(self.currDir)
      if len(files) == 0:
        print("No files created yet")
      else:
        l = [] 
        for path in files:
          if "commit" in path or "friends" in path or "shared_files" in path: continue
          l.append(get_time(f"{self.currDir}/{path}", path))
        heapSort(l)
        print("\t-- DATE --\t\t   --FILE NAME--")
        for e in l:
          print(f"{e[0]}\t\t{e[1]}")  

      command = input().split(" ")
      if command[0] == "ex":
        if self.currDir == f"./users/{self.username}":
          break
        elif len(self.currDir.split("/")) == 4 and self.username not in self.currDir:
          self.currDir = f"./users/{self.username}"
          self.versionC = None
        elif len(self.currDir.split("/")) == 5:
          self.currDir = f"./users/{self.username}"
          self.versionC = None
        else:
          for i in range(len(self.currDir) - 1, 0, -1):
            lastChar = self.currDir[i]
            if lastChar == "/":
              self.currDir = self.currDir[0:i]
              if self.currDir == f"./users{self.username}": self.versionC = None
              break
      elif command[0] == "run":
        subprocess.run(['python', f"{self.currDir}/{command[1]}"])
      elif command[0] == "bl":
        self.changeBranch()
      elif command[0] == "revert":
        self.revertChanges()
      elif command[0] == "commit":
        self.commitProject()  
      elif command[0] == "rename" and len(command) == 3:
        self.renameFile(command[1], command[2])
      elif command[0] == "merge" and len(command) == 3:
        self.mergeBranches(command[1], command[2])
      elif command[0] == "af":
        self.addFriend() 
      elif command[0] == "collab":
        self.collabs()
      elif command[0] not in ["mk", "cr", "op", "rm", "br"] or len(command) != 2:
        self.error("Command not valid")
      elif command[0] == "mk":
        self.createProject(command[1])
      elif command[0] == "cr":
        self.createFile(command[1])
      elif command[0] == "op":
        self.moveToProject(command[1])
      elif command[0] == "rm":
        self.removePath(command[1])
      elif command[0] == "br":
        self.createBranch(command[1])
      

  def createProject(self, name):
    if "commit" in name:
      self.error("Invalid name")
      return
    try:
      os.mkdir(f"{self.currDir}/{name}")
      if self.currDir == f"./users/{self.username}": 
        os.mkdir(f"{self.currDir}/{name}/main")
    except:
      self.error("Project name already exists or invalid name format")

  def createFile(self, name):
    pathname = f"{self.currDir}/{name}"
    # if self.currDir == f"./users/{self.username}":
    if len(self.currDir.split("/")) == 3:
      self.error("You must be inside a directory to create a file")
    elif os.path.exists(pathname):
      self.error("File already exists")
    else:
      open(pathname, "x")

  def moveToProject(self, name, dir = ""):
    # pathname = f"{self.currDir if dir == '' else dir}/{name}"
    pathname = f"{self.currDir}/{name}" if dir == "" else dir
    if os.path.exists(pathname):
      if os.path.isfile(pathname):
        subprocess.run(['python', './scripts/editor.py', pathname])
      else:
        # if self.currDir == f"./users/{self.username}":
        if len(self.currDir.split("/")) == 3:
          self.versionC = VersionControl(f"{self.currDir}/{name}", name)
          self.currDir = f"{pathname}/main"
        else: self.currDir = pathname
    else:
      self.error("Path doesn't exist")
  
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
          self.error("Directory doesn't exist")
        except OSError:
          self.error("Couldn't delete directory")
  
  def commitProject(self):
    # if self.currDir == f"./users/{self.username}":
    if len(self.currDir.split("/")) == 3:
      self.error("You need to be inside a project to commit changes")
    elif self.username not in self.currDir:
      self.error("Only the owner of the project can commit changes")
    else:
      self.versionC.commitChanges()

  def createBranch(self, name):
    # if self.currDir == f"./users/{self.username}":
    if len(self.currDir.split("/")) == 3:
      self.error("You need to be inside a project to create a new branch")
      return
    
    if self.username not in self.currDir:
      self.error("Only the project owner can create branches")
      return
    
    self.versionC.createBranch(name)
    self.currDir = f"{self.versionC.projectPath}/{name}"

  def changeBranch(self):
    # if self.currDir == f"./users/{self.username}":
    if len(self.currDir.split("/")) == 3:
      self.error("You need to be inside a project to switch branches")
      return
    
    if self.username not in self.currDir:
      self.error("Only the project owner can change branches")
      return
    
    self.versionC.switchBranches()
    self.currDir = f"{self.versionC.projectPath}/{self.versionC.currBranch}"

  def revertChanges(self):
    # if self.currDir == f"./users/{self.username}":
    if len(self.currDir.split("/")) == 3:
      self.error("You need to be inside a project to revert changes")
      return
    
    if self.username not in self.currDir:
      self.error("Only the project owner can revert changes")
      return
    
    self.versionC.revertChanges()

  def renameFile(self, src, dest):
    try:
      newSrc = f"{self.currDir}/{src}"
      newDest = f"{self.currDir}/{dest}"
      os.rename(newSrc, newDest)
    except FileExistsError:
      self.error("A file already exists with that name")
    except FileNotFoundError:
      self.error("Source file doesn't exist")

  def mergeBranches(self, src, dest):
    # if self.currDir == f"./users/{self.username}":
    if len(self.currDir.split("/")) == 3:
      self.error("You need to be inside a project to merge branches")
      return
    
    if self.username not in self.currDir:
      self.error("Only the project owner can merge branches")
      return
    
    self.versionC.mergeBranches(src, dest)
    self.currDir = f"{self.versionC.projectPath}/{dest}"

  
  def addFriend(self):
    if self.versionC == None:
      self.error("You need to be inside a project to invite friends")
      return
    #newpath =  fr'C:\Users\Lenovo\Desktop\Proyecto-I-EDA-master\users1\{self.username}\friends\f'
    newpath = f"./users/{self.username}/friends/f" 
    self.tree.print_in(self.tree.root, 0, self.username)
    #s = input(str())
    ex = input(str("Type the name of the friend that you would like to add to your list of colaborators!\n"))
    # b = self.tree.search(self.tree.root, int(ex))
    b = self.tree.search(self.tree.root, ex)
    if b is not None:
      #print(f"this is b {b}")
      # friendpath = f'./users/{b}/shared_files/shared'
      # file_path = os.getcwd()
      # file_name = input(str("Type the project name: "))
      # with open(friendpath, "a", newline='') as db:
      #   writer = csv.writer(db)
      #   writer.writerow([f"{self.versionC.projectPath}", file_name])
      with open(newpath, newline = '') as db:
        reader = csv.reader(db)
        for row in reader:
          currUser = row[0]
          if currUser == str(b):
            print("User already in your friend list")
            q = input(str("Press enter to continue"))
            return
       #print(f"this is b {b}")
      friendpath = f'./users/{b}/shared_files/shared'
      file_path = os.getcwd()
      file_name = input(str("Type the project name: "))
      with open(friendpath, "a", newline='') as db:
        writer = csv.writer(db)
        writer.writerow([f"{self.versionC.projectPath}", file_name])
      with open(newpath, "a", newline = '') as db:
        writer = csv.writer(db)
        writer.writerow([b])
      print("Friend added!")
    else: 
      print("Your friend is not registered in the app")
    s = input(str("Press enter to continue"))

  def collabs(self):
    files = os.listdir(f'./users/{self.username}/shared_files')

    if os.path.getsize(f'./users/{self.username}/shared_files/shared') == 0:
      print("Your friends haven't shared any files with you")
      ex = input(str("Press enter to continue"))
    else:
      print("--FILE NAME--")
      with open(f'./users/{self.username}/shared_files/shared', newline = '') as db:
        reader = csv.reader(db)
        for row in reader:
          print(str(row[1]))
      selection = input(str("Select the file you want to open"))
      with open(f'./users/{self.username}/shared_files/shared', newline = '') as db:
        reader = csv.reader(db)
        for row in reader:
          if selection == row[1]:
            self.moveToProject("", row[0])
            print("You have entered to your friend's project!")
            #self.moveToProject()
            # s = input(str("Print enter to continue"))
            break

  def error(self, msg):
    print(msg)
    time.sleep(1.5)
