import csv
import random

class Node: 
    def __init__(self, key, name = " "): 
        self.left = None
        self.right = None
        self.key = key
        #self.value = value
        self.name = name
    
    def __str__(self): 
        return str(self.key) #+ "->" + str(self.name)

class BinaryTree: 
    root = None
    
    def insert(self, root, n): 
        if root is None:
            self.root = n
            return 
    
        if n.key < root.key: 
            if root.left is None: 
                root.left = n
            else:
                self.insert(root.left, n)
        elif n.key > root.key: 
            if root.right is None: 
                root.right = n
            else: 
                self.insert(root.right, n)
    
    def search(self, root, key): 
        if root is None: 
            return None
        
        if root.key == key: 
            return root.key
        else: 
            if key < root.key: 
                return self.search(root.left, key)
            else: 
                return self.search(root.right, key)
        
    def minn(self, root):
        if root is None: 
            return None
        
        if root.left is None: 
            return root
    
        return self.minn(root.left)

    def maxx(self, root): 
        if root is None: 
            return None
        
        if root.right is None: 
            return root
        
        return self.maxx(root.right)
    
    def delete(self, root, key): 
        if root is None: 
            return None
        
        if key < root.key:
            root.left, times = self.delete(root.left, key)
        elif key > root.key:
            root.right, times = self.delete(root.right, key)
        else: 
            if root.left is None: 
                temp = root.right
                root = None
                return temp
            elif root.right is None: 
                temp = root.left
                root = None
                return temp
            
            temp = self.minn(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)
        return root

    def print_in(self, root, level, first = ""):
        if root is not None: 
            self.print_in(root.left, level + 1, first)
            if root.key != first:
                print("\t"*level, root)
            self.print_in(root.right, level + 1, first)
            
    
    def print_pre(self, root): 
        if root is not None: 
            print(root)
            self.print_pre(root.left)
            self.print_pre(root.right)
    
    def print_post(self, root): 
        if root is not None:
            self.print_post(root.left)
            self.print_post(root.right)
            print(root)

    def fill_tree(self): 
        randomList=[]
        with open("./users/database.csv") as data: 
            reader = csv.reader(data)
            j = 1
            for row in reader:
                name, pswd = row
                #r = random.randint(1, 10000)
                # if r in randomList:
                #     r = random.randint(r, 10000)
                self.insert(self.root, Node(name, j))
                j += 1

def men(root, ini): 
    ex = input(str("Type ex to get back"))
    if ex == "ex": 
        return