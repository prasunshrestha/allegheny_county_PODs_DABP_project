# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 08:44:50 2020

Decision Analytics for Business and Policy
Team Project

@author: Jose Salomon
"""

## NOTES: MODEL INFEASIBLE WITH CAPACITY AT IS. NEED TO INCREASE CAPACITY 100 FOLD OR SERVE A SMALL PROPRTION OF POPULATION WITHIN EACH AREA TO REACH FEASIBILITY
import os
import numpy as np
#genfromtxt runs two main loops. The first loop converts each line of the file in a sequence of strings. The second loop converts each string to the appropriate data type
import gurobipy as gp
from gurobipy import GRB


# Get current working directory 
PATH = os.getcwd()

# Import parameters NOTE: NEED TO USE GENFROMTEXT FUNC AS USING PANDAS CSV GENERATES WRONG SHAPE FOR N*1 ARRAYS
with open(PATH+'/tracts.csv', 'r', encoding='utf-8-sig') as f: 
    tracts = np.genfromtxt(f, dtype=float, delimiter=',')

with open(PATH+'/pods.csv', 'r', encoding='utf-8-sig') as f: 
    pods = np.genfromtxt(f, dtype=float, delimiter=',')

with open(PATH+'/dists.csv', 'r', encoding='utf-8-sig') as f: 
    dists = np.genfromtxt(f, dtype=float, delimiter=',')


#tracts = areas[:,0:2] #selects x,y coordinates leaving out population
#pods = pods[:,0:2] #selects x,y coordinates leaving out capacity


n = 402 #census tracts
m = 47 #pods

P = 20 #number of pods that can be built
tot_pop = 1231145 #total population in Allegheny County (sum of all census tracts)
I = .1 #proportion of population at each tract to be served


n_tracts = range(n)
n_pods = range(m)

# create a matrix with all distances from areas i to pod j (areas rows, pods columns)
#[x.coord,y.coord, dist from i to j given dij=sqrt((xi-xj)**2 - (yi - yj**2))
#distances = np.zeros(shape=(n,m))
#
#for i in n_areas:
#    apos = np.array((areas[i,0],areas[i,1]))
#    for j in n_pods:
#        newd = np.sqrt((apos[0]-pods[j,0])**2 + (apos[1]-pods[j,1])**2)
#        distances[i,j] = newd

    
# CAPACITY at each shelter
capacity = pods[:,2]

# RESIDENTS in each area
residents = tracts[:,2]

## Setting up model object
m = gp.Model("assignments")

## DVs
x = m.addVars(n_pods, vtype=GRB.BINARY) #1 if pod j is built
y = m.addVars(n_tracts, n_pods, vtype=GRB.BINARY) #1 if area i assigned to pod j

## OBJECTIVE FUNCTION

objFn = gp.LinExpr()
objFn += sum(sum(dists[i,j]*y[i,j]*(residents[i]/tot_pop) for i in n_tracts) for j in n_pods)
#
m.setObjective(objFn)

m.modelSense = GRB.MINIMIZE
## CONSTRAINTS ##
# capacity 
for j in n_pods:
    m.addConstr(sum(residents[i]*y[i,j] for i in n_tracts) <= 30*2*capacity[j]*x[j]) #30 represents number of days POD expected to operate, 2 represents capacity multiplier

# Can only build 10 shelters
m.addConstr(sum(x[j] for j in n_pods) <= P)

# assignment can only be done on a built PODS

for i in n_tracts:
    for j in n_pods:
        m.addConstr(x[j]-y[i,j] >=0)

for i in n_tracts:
    m.addConstr(sum(y[i,j] for j in n_pods) == 1)

#Solve
m.optimize()

## Print optimal value ##
print(m.objVal)

## Print optimal solution ##
# shelters built

for i in n_pods:
    print (i, x[i].x)
#
##areas assignments and distance
#
#optsol_list = []
#for i in n_areas:
#    for j in n_pods:
#        optsol_list.append(i)
#        optsol_list.append(j)
#        optsol_list.append(y[i,j].x)
#        #print((i, j, y[i,j].x))  #used if need to print optimal solution
#
###save optimal solution values into an 8000x3 array
#opt_sol = np.array(optsol_list)
#opt_sol = np.reshape(opt_sol, (8000,3))
#
##np.savetxt("opt_sol.csv", opt_sol, delimiter=",")
##np.savetxt("distances.csv", distances, delimiter=",")











#create a distance column to attach to optimal solution array
#dist_list = []
#for i in n_areas:
#    for j in n_shelters:
#        dist_list.append(distances[i,j])
#
##dist_col = np.array(dist_list)
##dist_col = np.reshape(dist_col, (8000,1))
##np.savetxt("dist_col.csv", dist_col, delimiter=",")
##
##np.savetxt("res_col.csv", residents, delimiter=",")
 
        




  
#    
#    

