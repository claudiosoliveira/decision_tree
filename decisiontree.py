import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import copy

dataset = pd.read_csv('filmes.csv',encoding="latin1")
X = dataset.iloc[:, 1:].values
#print(X.shape)
print(dataset)
attribute = ['País', 'Grande Estrela', 'Genero', 'Sucesso']


class Node(object):
    def __init__(self):
        self.value = None
        self.decision = None
        self.childs = None


def findEntropy(data, rows):
    yes = 0
    no = 0
    ans = -1
    idx = len(data[0]) - 1
    entropy = 0
    for i in rows:
        if data[i][idx] == 'Sim':
            yes = yes + 1
        else:
            no = no + 1

    x = yes/(yes+no)
    y = no/(yes+no)
    if x != 0 and y != 0:
        entropy = -1 * (x*math.log2(x) + y*math.log2(y))
    if x == 1:
        ans = 1
    if y == 1:
        ans = 0
    return entropy, ans


def findMaxGain(data, rows, columns):
    maxGain = 0
    retidx = -1
    entropy, ans = findEntropy(data, rows)
    #if entropy == 0:
        #if ans == 1:
           # print("Yes")
        #else:
           # print("No")
    #return maxGain, retidx, ans

    for j in columns:
        mydict = {}
        idx = j
        # print(idx)
        for i in rows:
            key = data[i][idx]
            if key not in mydict:
                mydict[key] = 1
            else:
                mydict[key] = mydict[key] + 1
        gain = entropy

        # print(mydict)
        for key in mydict:
            yes = 0
            no = 0
            for k in rows:
                if data[k][j] == key:
                    if data[k][-1] == 'Sim':
                        yes = yes + 1
                    else:
                        no = no + 1
            # print(yes, no)
            x = yes/(yes+no)
            y = no/(yes+no)
            # print(x, y)
            if x != 0 and y != 0:
                gain += (mydict[key] * (x*math.log2(x) + y*math.log2(y)))/10
        #gain /= 10
        #print(gain)
        if gain > maxGain:
            # print("hello")
            maxGain = gain
            retidx = j
    #print(maxGain)
    return maxGain, retidx, ans


def buildTree(data, rows, columns):

    maxGain, idx, ans = findMaxGain(X, rows, columns)
    root = Node()
    root.childs = []
    # print(maxGain)
    if maxGain == 0:
        if ans == 1:
            root.value = 'Sim'
        else:
            root.value = 'Nao'
        return root

    root.value = attribute[idx]
    mydict = {}
    for i in rows:
        # print(idx)
        key = data[i][idx]
        if key not in mydict:
            mydict[key] = 1
        else:
            mydict[key] += 1

    newcolumns = copy.deepcopy(columns)
    newcolumns.remove(idx)
    for key in mydict:
        newrows = []
        for i in rows:
            if data[i][idx] == key:
                newrows.append(i)
        # print(newrows)
        temp = buildTree(data, newrows, newcolumns)
        temp.decision = key
        root.childs.append(temp)
    print("Filme escolhido: "+ str(idx + 1) )
    return root


def traverse(root):
   #print(root.decision)
   # print(root.value)
    

    n = len(root.childs)
    if n > 0:
        for i in range(0, n):
            traverse(root.childs[i])


def calculate():
    rows = [i for i in range(0, 10)]
    columns = [i for i in range(0, 4)]
    root = buildTree(X, rows, columns)
    root.decision = ''
    # print(root.decision)
    traverse(root)

#print(dataset.head())
#print(dataset.to_numpy())
calculate()