class NodeVC:
  to = 0
  next = None
  prev = None
  color = 0
  distance = -1

  def __init__(self, key):
    self.key = key

class GraphVC:
  edges = []
  grade = []
  isDirected = False
  nodes = []
  root = None

  def __init__(self, numNodes):
    self.numNodes = numNodes
    i = 0
    while i <= numNodes:
      self.grade.append(0)
      self.edges.append(None)
      i += 1

  def insert_edge(self, intU, intV, nameU, nameV, firstTime):
    item = NodeVC(nameU)
    item.to = intV
    item.next = self.edges[intU]
    if intU == 1:
      self.root = item
    
    self.edges[intU] = item
    self.grade[intU] += 1
    
    if firstTime and intV != intU:
      self.insert_edge(intV, intU, nameV, nameU, False) 
  
  def showBranches(self):
    intSource = 1
    self.edges[intSource].color = 1
    self.edges[intSource].distance = 0
    self.edges[intSource].prev = None
    queue = []
    queue.append(intSource)

    string = ""
    while len(queue) != 0:
      u = queue.pop(0)
      v = self.edges[u]
      if v.distance == 1: print(v.key)
      while v != None:
        if v.to == None:
          break
        if self.edges[v.to] != None:
          if self.edges[v.to].color == 0:
            self.edges[v.to].color = 1
            self.edges[v.to].distance = self.edges[u].distance + 1
            self.edges[v.to].prev = u
            queue.append(v.to)
        v = v.next
      self.edges[u].color = 2  

    self.resetColors()

  def searchBranch(self, branchName):
    i = 1
    while i <= self.numNodes:
      if self.edges[i] != None:
        if self.edges[i].color == 0:
          path = self.dfs_visit(i, branchName)
          if path != None: 
            self.resetColors()
            return path
      i += 1
    self.resetColors()
      
  def dfs_visit(self, u, branchName):
    self.edges[u].color = 1
    v = self.edges[u]
    if v.key == branchName:
      return v.key

    while v != None:
      if v.to == None: 
        break
      if self.edges[v.to] != None:
        if self.edges[v.to].color == 0:
          self.edges[v.to].prev = self.edges[u]
          return self.dfs_visit(v.to, branchName)
      v = v.next
    
    self.edges[u].color = 2

  def resetColors(self):
    for i in range(1, len(self.edges)):
      if self.edges[i] == None: continue
      self.edges[i].color = 0
