#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries and packages

from gurobipy import *
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


# get current working directory 
path = os.getcwd()


# In[3]:


# import tracts, pods, and distances

with open(path+'/tracts.csv', 'r', encoding='utf-8-sig') as f: 
    tracts = np.genfromtxt(f, dtype=float, delimiter=',') # residential areas
    
with open(path+'/pods.csv', 'r', encoding='utf-8-sig') as f: 
    pods = np.genfromtxt(f, dtype=float, delimiter=',') # sites
    
with open(path+'/dists.csv', 'r', encoding='utf-8-sig') as f: 
    dists = np.genfromtxt(f, dtype=float, delimiter=',')


# In[4]:


# capacity = np.sum(pods[:,2]) #total capacity of all pods
popTotal = np.sum(tracts[:,2]) # total population in Allegheny County

residents = tracts[:,2] # population of tracts
capacity = pods[:,2] # capacity of pods


# In[5]:


# indices for tracts and pods
p = len(tracts) #census tracts
q = len(pods) #pods

n_tracts = range(p) # number of tracts
n_pods = range(q) # number of pods

P = 20 #number of pods that can be built (subject to change)
I = .1 #proportion of population at each tract to be served (subject to change)


# In[6]:


# setting up model object

m = Model("Assignments")


# In[7]:


# setting up the decision variables

# where to build the pods
x = m.addVars(n_pods, vtype=GRB.BINARY) #1 if pod j is built

# where to assign which tracts to which pods
y = m.addVars(n_tracts, n_pods, vtype=GRB.BINARY) #1 if area i assigned to pod j


# In[8]:


# Objective Function

objFn = LinExpr()

objFn += sum(sum(dists[i,j] * y[i,j] * (residents[i]) for i in n_tracts) for j in n_pods)
#
m.setObjective(objFn)

m.modelSense = GRB.MINIMIZE


# In[9]:


# Constraints

# number of total sites that we could build
m.addConstr(sum(x[j] for j in n_pods) <= P) 

# capacity constraints
for j in n_pods:
    m.addConstr(sum(residents[i] * y[i,j] for i in n_tracts) <= 30 * 2 * capacity[j] * x[j]) 

# a residential can have at most one shelter
for i in n_tracts:
    m.addConstr(sum(y[i,j] for j in n_pods) == 1) 

# all residential areas must be met
m.addConstr(sum(sum(y[i,j] for j in n_pods) for i in n_tracts) >= len(residents)) 

# a tract can only be assigned to a pod that as been built
for i in n_tracts:
    for j in n_pods:
        m.addConstr(x[j] - y[i,j] >= 0)


# In[10]:


m.optimize()


# In[11]:


print(m.objVal)


# In[12]:


# New Optimization Model
# Minimax Problem

# new optimization model
m1 = Model("MiniMax")

# pods
x1 = m1.addVars(n_pods, vtype = GRB.BINARY) # same as x_j (whether a pod is built on site j)

# tracts
y1 = m1.addVars(n_tracts, n_pods, vtype=GRB.BINARY) # same as y_ij (whether a residential area
                                                    # i is assigned to site j)


# In[13]:


# max distance
maxDistance = m1.addVars(1,1, lb = 0.0) # a new decision variable to pick the maximum distance
                                        # between the tract (residential area) to pods

m1.setObjective(maxDistance[0,0])
m1.modelSense = GRB.MINIMIZE


# In[14]:


# Constraints

# number of total sites that we could build
m1.addConstr(sum(x1[j] for j in n_pods) <= P) 

# capacity constraints
for j in n_pods:
    m1.addConstr(sum(residents[i] * y1[i,j] for i in n_tracts) <= 30 * 2 * capacity[j] * x1[j]) 

# a residential can have at most one shelter
for i in n_tracts:
    m1.addConstr(sum(y1[i,j] for j in n_pods) == 1) 

# all residential areas must be met
m1.addConstr(sum(sum(y1[i,j] for j in n_pods) for i in n_tracts) >= len(residents)) 

# a tract can only be assigned to a pod that as been built
for i in n_tracts:
    for j in n_pods:
        m1.addConstr(x1[j] - y1[i,j] >= 0)

# the distance to shelter must be less than or equal to the maximum distance
for j in n_pods:
    for i in n_tracts:
        m1.addConstr(dists[i,j] * y1[i,j] <= maxDistance[0,0])


# In[15]:


m1.optimize()


# In[16]:


print(m1.objVal)


# ## Visualization of Tracts  Assignment to Pods

# In[31]:


DistanceToSite = [] # list of all the distances between the tracts and their assigned pods
residenceSitePair = [] # tracts and pods pair

for i in n_tracts:
    for j in n_pods:
        if y[i,j].x == 1:
            residenceSitePair.append((i,j))

for a, b in residenceSitePair:
    # distance = abs(tracts[a][0] - pods[b][0]) + abs(tracts[a][1] - pods[b][1]) # grid distance
    distance = np.sqrt((tracts[a][0] - pods[b][0]) ** 2 + abs(tracts[a][1] - pods[b][1]) ** 2) # eucledian distance
    DistanceToSite.append(distance)


# In[32]:


# plotting histogram

plt.hist(DistanceToSite)

plt.title("Tracts to Pods Distance")
plt.xlabel("Distance to Tracts (in miles)")
plt.ylabel("# of Tracts")

plt.show()


# In[36]:


# same setup as before but for for the minimax model this time

DistanceToSite1 = []
residenceSitePair1 = []

for i in n_tracts:
    for j in n_pods:
        if y1[i,j].x == 1:
            residenceSitePair1.append((i,j))

for a, b in residenceSitePair1:
    # distance1 = abs(tracts[a][0] - pods[b][0]) + abs(tracts[a][1] - pods[b][1]) # grid distance
    distance1 = np.sqrt((tracts[a][0] - pods[b][0]) ** 2 + abs(tracts[a][1] - pods[b][1]) ** 2) # eucledian distance
    DistanceToSite1.append(distance1)


# In[37]:


# plotting histogram

plt.hist(DistanceToSite1)

plt.title("Tracts to Pods Distance (after minimizing maximum distance)")
plt.xlabel("Distance to Tracts (in miles)")
plt.ylabel("# of Tracts")

plt.show()

