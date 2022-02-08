# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 00:56:38 2021

@author: madison
"""

# Gnowee Modules
import Gnowee_multi
from ObjectiveFunction_Multi import ObjectiveFunction_multi
from Constraints import Constraint
from GnoweeHeuristics_multi import GnoweeHeuristics_multi
from CASMOtest import CASMOtest
import numpy as np
import matplotlib.pyplot as plt
from OptiPlot_multi import plot_vars
from GnoweeUtilities_multi import ProblemParameters_multi, Event, Parent_multi

import random

# Select optimization problem type and associated parameters
# This uses the CASMO problem - runs various CASMO inputs to optimize the lattice fuel pin arrangement, maximizing k-inf at EOC
# Inputs (discrete) - fuel type numbers hard coded in mock CASMO input file 

listOfObjectiveFunctions = [ObjectiveFunction_multi(CASMOtest)]

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
gh= GnoweeHeuristics_multi(objective=listOfObjectiveFunctions, constraints=[], lowerBounds=[], upperBounds=[],
                     discreteVals=[[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
                                   [1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
                                   [1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
                                   [1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],
                                   [1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]], 
                     varType=['d','d','d','d','d','d','d','d','d','d',
                              'd','d','d','d','d','d','d','d','d','d',
                              'd','d','d','d','d','d','d','d','d','d',
                              'd','d','d','d','d','d','d','d','d','d',
                              'd','d','d','d','d','d'],
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

plt.plot(generations, fitnesses, '-r', lw=2) # plot the data as a line
plt.xlabel('Population', fontsize=14) # label x axis
plt.ylabel('Fitness', fontsize=14) # label y axis
plt.gca().grid() # add grid lines
plt.show() # display the plot
plt.savefig('Fitness.png')