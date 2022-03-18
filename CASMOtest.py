# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 23:38:17 2021

@author: Madison Tippet
"""

import numpy as np
import os
from functions import program_gen as pg
from functions import program_gen2 as pg2
from functions import fuelwriter as fw
from functions import fuelwriter2 as fw2
from functions import fuel_data as fd
from functions import fuel_data2 as fd2
from functions import run_on_cluster as roc
from functions import file_check as fc
from functions import get_results as gr
from functions import file_find as ff

# This is an objective function that pairs with Studsvik's Casmo-4 lattice
# physics code in order to optimize the lattice arrangement of fuel types to
# arrive at a design that maximizes k-eff at end of cycle and minimizes the
# power peaking factor (<1.6)

# option 1 has no constraints on the placement of gadolinia, but option 2
# prevents fuel w/ gadolinia concentrations to be placed on the outer edges
# of the lattice (this is one of 4 heuristics rules that have been applied)

# 4 Heursistics rules: fuel lattice has diagonal symmetry, fixed water rod
# positions in center, pins at edge cannot contain gadolinia, and pins at
# corners must have minimum uranium arrangments in literature

#input: vec = selected vector design from Gnowee
#output: fitness = how close the design is to max k-eff and min ppf

def CASMOtest(vec):
    print(vec)
        
    #option 1 - One fuel type list
    
    # #initialization of all the function inputs
    # init_file = 'test0'
    # num_of_var_opt = 46
    # num_of_files = 8 #.inp,.cax,.log,.out,_done.dat,_script.txt,_script.txto, _script.txte
    # input_file = 'BWRGNOW.txt'
    
    # #calling the functions
    
    # #make input file and replace <> with variable inputs
    # pg(init_file+'.inp',input_file,vec,num_of_var_opt)

    # #fuel type data selector
    # ind = fd(vec)
    # #fuel type writer
    # fw(init_file+'.inp',ind,num_of_var_opt)
    # print('file made')
    
    
    
 
    #option 2 - Fuel type list for internal and external   
    
    #separation of fuel type variable lists (Interior and Exterior)
    #Internal lattice positions - fuel types w/ and w/out gadolinia
    interior = []
    i=0
    while i<30:
        interior.append(vec[i])
        i = i + 1
    
    #External lattice positions - fuel types w/out gadolinia
    exterior = []
    while i<46:
        exterior.append(vec[i])
        i = i + 1
    
    #initialization of all the function inputs
    init_file = 'test0'
    num_of_var_opt1 = 30 #int
    num_of_var_opt2 = 16 #ext
    num_of_files = 8 #.inp,.cax,.log,.out,_done.dat,_script.txt,_script.txto, _script.txte
    input_file = 'BWR_inp.txt'
    
    #calling the functions
    
    #make input file and replace <> with variable inputs
    pg2(init_file+'.inp',input_file,interior,exterior,num_of_var_opt1,num_of_var_opt2)

    #fuel type data selector
    ind1,ind2 = fd2(interior,exterior)
    #fuel type writer
    fw2(init_file+'.inp',ind1,ind2,num_of_var_opt1,num_of_var_opt2)
    print('file made')
    
    
    #For both options
    
    #cluster script for CASMO created/submitted
    roc(init_file+'.inp')
    
    #check all files were created
    fc(init_file,num_of_files)
    print('files found')
    
    #extract results (k-inf at EOC) from the output file
    values = gr(init_file+'.out','BURNUP =   63.000 MWD/KG   K-INF =   ','values.csv')
    values = np.genfromtxt('values.csv') #read in from csv
    kvals = values[7] #takes just the k-values from the results
    print(kvals)
    
    #extract constraints (Max power peaking factor) from output file
    constraints = gr(init_file+'.out','PEAK: LL =','constraints.csv')
    constraints = np.genfromtxt('constraints.csv')
    ppf = max(constraints[:,7])
    print(ppf)
    
    #get enrichment
    enrich = gr(init_file+'.out','1 40.0  768.0  551.7  551.7    0.0        0.000','enrich.csv')
    enrich = np.genfromtxt('enrich.csv')
    enrichment = (enrich[12])
    print(enrichment)

    #Separative Work Unit (SWU) Calculations
    xp = enrichment/100 #concentration of the product uranium
    xf = 0.00711 #concentration of the feed uranium
    xt = 0.002 #concentration of the tails
    Mp = np.pi*(.44**2)*15.24*10.97 #mass of the product uranium
    Mf = ((xp-xt)/(xf-xt))*Mp #mass of the feed uranium
    Mt = Mf-Mp #mass of the tails
    #Value functions
    Vxp = (1-2*xp)*np.log((1-xp)/xp)
    Vxt = (1-2*xt)*np.log((1-xt)/xt)
    Vxf = (1-2*xf)*np.log((1-xf)/xf)
    Swu = Mp*Vxp + Mt*Vxt - Mf*Vxf #grams
    cost = 98*Swu/1000 #$

    # Fitness calculation
    #option 1 - constraint on ppf
    # if ppf>=1.6:
    #     #removes lattice arrangements that result in a ppf over the constraint
    #     fitness = 1E9
    # else:
    #     #fitness = difference between k-val & arbitrary "max" number; optimize to zero
    #     fitness = 0.85 - kvals
    #option 2 - multi-objective function
    # fitness = 2 + (ppf-1.6) + (0.85-kvals)
    #option 3 - multi-objective function w/ weighting factors
    # fitness = 100 + 100*(ppf-1.6) + 1000*(0.85-kvals)
    #option 4 - multi-objective w/weighting w/cost factors
    fitness = 100 + 100*(ppf-1.6) + 1000*(0.85-kvals) + (cost-88.2)/5
    print(fitness)
    
    
    #delete all the files
    l = ff(init_file)
    p=0
    for p in range(len(l)):
        os.remove(l[p])
        
    #open file with access mode 'a'
    #write results (vector/fitness) to file
    with open("results.csv", "a") as file_object:
        file_object.write(str(vec)+'; '+str(fitness)+'; '+str(kvals)+'; '+str(ppf)+'\n')
    return fitness