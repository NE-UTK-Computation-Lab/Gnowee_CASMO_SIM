# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 00:56:38 2021

@author: Madison Tippet
Adapted from Gnowee Example run
"""

# Gnowee Modules
import Gnowee_multi
from ObjectiveFunction_Multi import ObjectiveFunction_multi
from Constraints import Constraint
from GnoweeHeuristics_multi import GnoweeHeuristics_multi
from Obj_Func import CASMO4
from Obj_Func import SIM3
import numpy as np
import matplotlib.pyplot as plt
from OptiPlot_multi import plot_vars,plot_hist
from GnoweeUtilities_multi import ProblemParameters_multi, Event, Parent_multi
import random

# Select optimization problem type and associated parameters

# CASMO Option
# This uses the CASMO code set and corresponding oobjective function -
# tests various CASMO inputs to optimize the lattice fuel pin arrangement

# Inputs (discrete) - fuel type numbers hard coded in mock CASMO input file 

# listOfObjectiveFunctions = [ObjectiveFunction_multi(CASMO4)]

#option 1 - One fuel type list
# gh= GnoweeHeuristics_multi(objective=listOfObjectiveFunctions, constraints=[], lowerBounds=[], upperBounds=[],
#                      discreteVals=[[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
#                                    [1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
#                                    [1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
#                                    [1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
#                                    [1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12]], 
#                      varType=['d','d','d','d','d','d','d','d','d','d',
#                               'd','d','d','d','d','d','d','d','d','d',
#                               'd','d','d','d','d','d','d','d','d','d',
#                               'd','d','d','d','d','d','d','d','d','d',
#                               'd','d','d','d','d','d'],
#                       optimum=0.0, pltTitle='', histTitle='', varNames=['d'])


#option 2 - Fuel types list for both the interior and exterior positions
# gh= GnoweeHeuristics_multi(objective=listOfObjectiveFunctions, constraints=[], lowerBounds=[], upperBounds=[],
#                      discreteVals=[[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
#                                    [1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
#                                    [1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
#                                    [1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],
#                                    [1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]], 
#                      varType=['d','d','d','d','d','d','d','d','d','d',
#                               'd','d','d','d','d','d','d','d','d','d',
#                               'd','d','d','d','d','d','d','d','d','d',
#                               'd','d','d','d','d','d','d','d','d','d',
#                               'd','d','d','d','d','d'],
#                       optimum=0.0, pltTitle='', histTitle='', varNames=['d'])



# SIM3 Option
# This uses the SIM3 code set and corresponding objective function -
# tests various SIM3 inputs to optimize the axial enrichment loading, loading
# pattern, or blade pattterns

#Inputs (discrete) - fuel segment names from CASMO lattices

listOfObjectiveFunctions = [ObjectiveFunction_multi(SIM3)]

# #option 1 - Axial Segments
# gh= GnoweeHeuristics_multi(objective=listOfObjectiveFunctions, constraints=[], lowerBounds=[], upperBounds=[],
#                       discreteVals=[['BWRU248G44','BWRU253G44','BWRU255G44','BWRU260G44','BWRU261G33','BWRU274G44','BWRU278G44','BWRU278G64','BWRU278G84','BWRU296G43','BWRU4274G5','BWRU427G77','BWRU500G56','BWRU553G67','BWRU600G57','BWRU625G57','BWRU644G58','BWRU668G67','BWRU688G57','BWRU693G58','BWRU705G57','BWRU717G68','BWRU722G58','BWRU800G58'],
#                                     ['BWRU248G44','BWRU253G44','BWRU255G44','BWRU260G44','BWRU261G33','BWRU274G44','BWRU278G44','BWRU278G64','BWRU278G84','BWRU296G43','BWRU4274G5','BWRU427G77','BWRU500G56','BWRU553G67','BWRU600G57','BWRU625G57','BWRU644G58','BWRU668G67','BWRU688G57','BWRU693G58','BWRU705G57','BWRU717G68','BWRU722G58','BWRU800G58'],
#                                     ['BWRU248G44','BWRU253G44','BWRU255G44','BWRU260G44','BWRU261G33','BWRU274G44','BWRU278G44','BWRU278G64','BWRU278G84','BWRU296G43','BWRU4274G5','BWRU427G77','BWRU500G56','BWRU553G67','BWRU600G57','BWRU625G57','BWRU644G58','BWRU668G67','BWRU688G57','BWRU693G58','BWRU705G57','BWRU717G68','BWRU722G58','BWRU800G58'],
#                                     ['BWRU248G44','BWRU253G44','BWRU255G44','BWRU260G44','BWRU261G33','BWRU274G44','BWRU278G44','BWRU278G64','BWRU278G84','BWRU296G43','BWRU4274G5','BWRU427G77','BWRU500G56','BWRU553G67','BWRU600G57','BWRU625G57','BWRU644G58','BWRU668G67','BWRU688G57','BWRU693G58','BWRU705G57','BWRU717G68','BWRU722G58','BWRU800G58'],
#                                     ['BWRU248G44','BWRU253G44','BWRU255G44','BWRU260G44','BWRU261G33','BWRU274G44','BWRU278G44','BWRU278G64','BWRU278G84','BWRU296G43','BWRU4274G5','BWRU427G77','BWRU500G56','BWRU553G67','BWRU600G57','BWRU625G57','BWRU644G58','BWRU668G67','BWRU688G57','BWRU693G58','BWRU705G57','BWRU717G68','BWRU722G58','BWRU800G58']],
#                       varType=['d','d','d','d','d'],optimum=0.0, pltTitle='', histTitle='', varNames=['d'])

# # option 2 - 1st Cycle Optimization
# # This tests various SIM3 inputs to optimize the initial core loading pattern to
# # simulate a "cartridge style" core
# # Note: Number of variables can be adjusted based on symmetry requirements

# #Inputs (discrete) - fuel type numbers hard coded in mock SIM3 input file

# gh= GnoweeHeuristics_multi(objective=listOfObjectiveFunctions, constraints=[], lowerBounds=[], upperBounds=[],
#                       discreteVals=[[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
#                                     [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]],
#                       varType=['d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d',
#                                'd','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d',
#                                'd','d','d','d','d','d','d','d','d'],
#                       optimum=0.0, pltTitle='', histTitle='', varNames=['d'])

# option 3 - Blade Pattern

# This tests various SIM3 inputs to optimize the blade pattern on the optimimum
# design from options 1 or 2

# Inputs (discrete) - control blade notches

gh= GnoweeHeuristics_multi(objective=listOfObjectiveFunctions, constraints=[], lowerBounds=[], upperBounds=[],
                      discreteVals=[[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48],[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48],[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48],[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48]],
                      varType=['d','d','d','d'],
                      optimum=0.0, pltTitle='', histTitle='', varNames=['d'])

print(gh)

# Run optimization
(timeline,lastpopulation) = Gnowee_multi.main_multi(gh)
print( '\nThe result:\n', timeline[-1])

#length = len(timeline) added in below
length = len(timeline)
fitnesses = np.zeros(length)
generations = np.zeros(length)
for i in range(0,length):
    ti = timeline[i]
    #changed t to ti
    fitnesses[i] = ti.fitness
    generations[i] = ti.generation
    
    with open("fitgen.txt", "a") as file_object:
        file_object.write(str(fitnesses[i])+'; '+str(generations[i])+'\n')



plt.plot(generations, fitnesses, '-r', lw=2) # plot the data as a line
plt.xlabel('Population', fontsize=14) # label x axis
plt.ylabel('Fitness', fontsize=14) # label y axis
plt.gca().grid() # add grid lines
plt.show() # display the plot
plt.savefig('Fitness.png')

plot_hist()