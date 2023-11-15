import os, shutil
from scripts.graph import GraphVC
from scripts.error import error

class VersionControl:
  def __init__(self, projectPath, projectName):
    self.projectPath = projectPath
    self.projectName = projectName
    self.currBranch = "main"
    self.branches = []
    self.commits = {}
    self.projectGraph = None
    # print(f"New version control: {projectPath}, {projectName}")
    self.initTree()

  def initTree(self):
    branches = os.listdir(self.projectPath)
    nodeCount = self.countNodes(branches)
    # print(f"node count: {nodeCount}")
    self.projectGraph = GraphVC(nodeCount)

    i = 2
    for branch in branches:
      # print(f"initializing tree, branch: {branch}")
      self.commits[f"{branch}"] = []
      self.branches.append(branch)
      self.projectGraph.insert_edge(1, i, self.projectName, branch, True)
      files = os.listdir(f"{self.projectPath}/{branch}")
      currFile = branch
      for file in files:
        if "commit" not in file: continue
        self.commits[f"{branch}"].append(file)
        self.projectGraph.insert_edge(i, i + 1, currFile, file, True)
        i += 1
        currFile = file
      i += 1

  def commitChanges(self):
    commitCounter = 0
    currDir = f"{self.projectPath}/{self.currBranch}"
    files = os.listdir(currDir)
    for file in files:
      if "commit" not in file: continue
      commitCounter += 1

    newCommit = f"{self.projectPath}/{self.currBranch}/commit{commitCounter + 1}"
    shutil.copytree(currDir, newCommit, ignore = self.ignorePaths('commit'))
    self.commits[f"{self.currBranch}"].append(f"commit{commitCounter + 1}")
    error("Project commit succesfull")
    self.initTree()

  def createBranch(self, branchName):
    if branchName in self.branches:
      error("Branch with that name already exists")
      return
    
    currDir = f"{self.projectPath}/{self.currBranch}"
    newBranch = f"{self.projectPath}/{branchName}"
    shutil.copytree(currDir, newBranch, ignore = self.ignorePaths('commit'))
    self.currBranch = branchName
    self.initTree()

  def switchBranches(self):
    self.projectGraph.showBranches()
    branchName = input("Enter branch name you wish to change to:\n")
    path = self.projectGraph.searchBranch(branchName)
    if path == None:
      error("Branch doesn't exist")
      return
    
    self.currBranch = path

  def revertChanges(self):
    i = 1
    for commit in self.commits[self.currBranch]:
      print(f"{i}: {commit}")
      i += 1

    num = int(input("Choose the commit number you wish to go back to:\n"))
    if num < 1 or num > len(self.commits[self.currBranch]):
      error("Invalid option")
      return
    
    ans = input("Are you sure you want to revert changes? (y/n): ")
    if ans.lower() != "y": return

    src = f"{self.projectPath}/{self.currBranch}/{self.commits[self.currBranch][num - 1]}"
    dest = f"{self.projectPath}/{self.currBranch}/"

    # distutils.dir_util.copy_tree(src, dest) 
    shutil.copytree(src, dest, dirs_exist_ok=True)

  def mergeBranches(self, src, dest):
    srcPath = self.projectGraph.searchBranch(src)
    destPath = self.projectGraph.searchBranch(dest)

    if srcPath == None or destPath == None:
      error("One or both branches don't exist")
      return
    
    ans = input("Are you sure you want to merge branches? Source branch will be deleted (y/n)\n")
    if ans.lower() != 'y': return

    newSrc = f"{self.projectPath}/{srcPath}"
    newDest = f"{self.projectPath}/{destPath}"
    # distutils.dir_util.copy_tree(newSrc, newDest) 
    shutil.copytree(newSrc, newDest, dirs_exist_ok=True)
    shutil.rmtree(newSrc)

  def ignorePaths(self, file):
    def _ignore_(path, names):
        ignored = []
        for dir in names:
          if file in dir:
            ignored.append(dir)
        return set(ignored)
         
    return _ignore_

  def countNodes(self, branches):
    nodeCounter = len(branches) + 1
    for branch in branches:
      files = os.listdir(f"{self.projectPath}/{branch}")
      for file in files:
        if "commit" in file:
          nodeCounter += 1

    return nodeCounter

