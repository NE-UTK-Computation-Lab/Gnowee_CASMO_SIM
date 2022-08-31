# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 23:38:17 2021

@author: Madison Tippet
"""

import numpy as np
import os
from functions import program_gen as pg
from functions import program_gen2 as pg2
from functions import var_data as vd
from functions import var_data2 as vd2
from functions import varwriter as vw
from functions import varwriter2 as vw2
from functions import run_on_cluster as roc
from functions import file_check as fc
from functions import get_results as gr
from functions import file_find as ff
from functions import get_table as gt
from functions import get_column as gc



# This is objective function pairs Studsvik's SIMULATE-3 (full-core depletion
# code with the optimizer Gnowee in order to optimize the axial enrichment 
# loading, core loading pattern, and/or blade sequences to arrive at a design
# which maximizes cycle length, achieves criticality at each exposure step, and
# minimizes the linear power density and other thermal limits.

# input: vec = selected vector design from Gnowee
# output: fitness = how well the design meets the objective function designated
#                   by the user

def SIM3(vec):
    print(vec)
    
    #initialization of function inputs
    #---------------------------------
    init_file = 'blade_pattern' #name of optimization files (cyc01_opt,cyc02_opt)
    num_of_var_opt = 4 #number of variables to optimize
    num_of_files = 9 #.inp,.cms,.sum,.res,.out,_done.dat,_script.txt,_script.txto, _script.txte
    input_file = 'rodded_opt.txt' #mock input file (cyc01.txt,cyc02.txt)
    variables = 'bladepattern.csv' #csv file with all variable options (fueltypes_sim.csv,axialsegments.csv)
    
    #calling the functions
    #---------------------
    #make input file and replace <> with variable inputs
    pg(init_file+'.inp',input_file,vec,num_of_var_opt)

    #variable data selector
    ind = vd(variables,vec)
    # print(ind)
    #variable writer
    vw(init_file+'.inp',ind,num_of_var_opt)
    print('file made')
    
    #create/submit cluster script for SIM-3
    roc(init_file+'.inp','sim')
    
    #check that all files were created
    fc(init_file,num_of_files)
    print('files found')
    
    #extracting data
    #---------------
    #extract k-values at each exposure step - BLADE PATTERNS
    k1 = gr(init_file+'.out','1  0   1.500','values.csv')
    k1 = np.genfromtxt('values.csv') #read in from csv
    k1 = k1[4] #takes just the k-values from the results
    # k2 = gr(init_file+'.out','2  0  730.00','values.csv')
    # k2 = np.genfromtxt('values.csv') 
    # k2 = k2[4]
    # k3 = gr(init_file+'.out','4  0 1080.00','values.csv')
    # k3 = np.genfromtxt('values.csv') 
    # k3 = k3[4] 
    print('k-eff:',k1)
    # print('k-eff:',k2)
    # print('k-eff:',k3)
    
    #CYCLE OPTIMIZATION PARAMETERS
    #extract axial data
    # data = gt(init_file+'.out','Axial Distribution Summary','axial.csv',7, 25)
    # linear_heat, linear_heat_list, max_linear_heat_list, max_linear_heat = gc(data,7,25,1)
    # fdz, fdz_list, max_fdz_list, max_fdz = gc(data,7,25,6)
    # print('Max LPD (kW/ft):',max_linear_heat)
    
    # #get enrichment
    # enrichment = gt(init_file+'.out','Fueled Segments:','enrich.csv',6,10)
    # enrich, enrich_list, max_enrich_list, max_enrich = gc(enrichment,6,10,3)
    # enrichavg = np.mean(enrich_list)
    # print('Enrichment:',enrichavg)
    # #Separative Work Unit (SWU) Calculations
    # xp = enrichavg/100 #concentration of the product uranium
    # xf = 0.00711 #concentration of the feed uranium
    # xt = 0.002 #concentration of the tails
    # Mp = (np.pi*(0.44**2)*0.88)*92*10.97 #mass of the product uranium (grams)
    # Mf = ((xp-xt)/(xf-xt))*Mp #mass of the feed uranium (g)
    # Mt = Mf-Mp #mass of the tails (g)
    # #Value functions
    # Vxp = (1-2*xp)*np.log((1-xp)/xp)
    # Vxt = (1-2*xt)*np.log((1-xt)/xt)
    # Vxf = (1-2*xf)*np.log((1-xf)/xf)
    # Swu = Mp*Vxp + Mt*Vxt - Mf*Vxf #g SWU
    # conv = 98 #$/1 kg SWU
    # cost = conv*(Swu/1000) #$
    # print('Cost: $',cost)
    
    # Fitness calculation
    #--------------------
    #option 1 - fitness = difference between k-val & arbitrary "max" number
    # fitness = 1.0 - kvals
    #option 2 - fitness based off k-eff and kW/ft values
    # fitness = 2*(1 - kvals) +  0.02*(max_linear_heat - 16)
    #option 3 - constraint on linear power density
    # if max_linear_heat>=16:
    #     #removes axial loading that results in a linear heat over threshold
    #     fitness = 1E9
    # else:
    #     #fitness = difference between k-val & arbitrary "max" number
    #     fitness = 1 - kvals
    #option 4 - constraint on EOC k-eff
    # if kvals<1:
    #     fitness = 1E9
    # else:
    #     fitness = max_linear_heat - 16
    #option 5 - constraint on EOC k-eff w/cost consideration
    # if kvals<1:
    #     fitness = 1E9
    # else:
    #     fitness = 0.5*(max_linear_heat - 16) + 0.01*(cost)
    #option 6 - constraint on both k-eff and LPD
    # if max_linear_heat>=16:
    #     fitness = 1E9
    # elif kvals<1:
    #     fitness = 1E9
    # else:
    #     fitness = 0.01*cost
    #option 7 - constraint on k and focus on LPD
    # if kvals <1:
    #     fitness = 1E9
    # elif max_linear_heat < 16:
    #     fitness = 2 + (max_linear_heat - 16)
    # else:
    #     fitness = (max_linear_heat - 16)
    #option 8 - achieve criticality with blade sequences
    if round(k1,5) == 1.00000:
        fitness = 0.0
    elif k1 < 1.00:
        fitness = (1.0 - k1)
    else:
        fitness = (k1 - 1.0)
        
    print('Fitness:',fitness)

    #perserve data
    #-------------
    #delete all optimization files
    l = ff(init_file)
    p=0
    for p in range(len(l)):
        os.remove(l[p])
        
    #save results
    #------------
    #open file with access mode 'a'
    #write results (vector/fitness) to file
    with open("results.csv", "a") as file_object:
        file_object.write(str(vec)+'; '+str(fitness)+'; '+str(k1)+'\n')
        #file_object.write(str(vec)+'; '+str(fitness)+'; '+str(kvals)+'; '+str(max_linear_heat)+'; '+str(cost)+'\n')
        
    return fitness


#------------------------------------------------------------------------------


# This objective function pairs Studsvik's CASMO-4 lattice physics code with 
# the optimizer Gnowee in order to optimize the lattice arrangement of fuel
# types to arrive at a design that maximizes k-eff at end of cycle and 
# minimizes the power peaking factor (<1.6)

# option 1 has no constraints on the placement of gadolinia, but option 2
# prevents fuel w/ gadolinia concentrations to be placed on the outer edges
# of the lattice (this is one of 4 heuristics rules that have been applied)

# 4 Heursistics rules: fuel lattice has diagonal symmetry, fixed water rod
# positions in center, pins at edge cannot contain gadolinia, and pins at
# corners must have minimum uranium arrangments in literature

# input: vec = selected vector design from Gnowee
# output: fitness = how close the design is to max k-eff and min ppf and min
#                  enrichment costs

def CASMO4(vec):
    print(vec)
        
    #option 1 - One fuel type list
    
    # #initialization of function inputs
    # #---------------------------------
    # init_file = 'casmo_opt'
    # num_of_var_opt = 46
    # num_of_files = 8 #.inp,.cax,.log,.out,_done.dat,_script.txt,_script.txto, _script.txte
    # input_file = 'BWRGNOW.txt'
    
    # #calling the functions
    # #---------------------
    # #make input file and replace <> with variable inputs
    # pg(init_file+'.inp',input_file,vec,num_of_var_opt)

    # #fuel type data selector
    # ind = vd(vec)
    # #fuel type writer
    # vw(init_file+'.inp',ind,num_of_var_opt)
    # print('file made')
    
    # -------------------------------------------------------------------------
     
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
    
    #initialization of function inputs
    #---------------------------------
    init_file = 'casmo_opt'
    num_of_var_opt1 = 30 #int
    num_of_var_opt2 = 16 #ext
    num_of_files = 8 #.inp,.cax,.log,.out,_done.dat,_script.txt,_script.txto, _script.txte
    input_file = 'BWR_lattice.txt'
    
    #calling the functions
    #---------------------
    #make input file and replace <> with variable inputs
    # pg(init_file+'.inp',input_file,interior,num_of_var_opt1)
    # pg(init_file+'.inp',init_file+'.inp',exterior,num_of_var_opt2)
    pg2(init_file+'.inp',input_file,interior,exterior,num_of_var_opt1,num_of_var_opt2)
    
    #fuel type data selector
    ind1,ind2 = vd2('fueltypes_int.csv','fueltypes_ext.csv')
    
    #fuel type writer
    # vw(init_file+'.inp',ind1,num_of_var_opt1)
    # vw(init_file+'.inp',ind2,num_of_var_opt2)
    vw2(init_file+'.inp',ind1,ind2,num_of_var_opt1,num_of_var_opt2)
    print('file made')
    
    
    
    #For both options
    #----------------
    #cluster script for CASMO created/submitted
    roc(init_file+'.inp','casmo')
    
    #check all files were created
    fc(init_file,num_of_files)
    print('files found')
    
    #extract results
    #---------------
    #k-inf at EOC
    values = gr(init_file+'.out','BURNUP =   63.000 MWD/KG   K-INF =   ','values.csv')
    values = np.genfromtxt('values.csv') #read in from csv
    kvals = values[7] #takes just the k-values from the results
    print(kvals)
    
    #constraints (Max power peaking factor)
    constraints = gr(init_file+'.out','PEAK: LL =','constraints.csv')
    constraints = np.genfromtxt('constraints.csv')
    ppf = max(constraints[:,7])
    print(ppf)
    
    #enrichment
    enrich = gr(init_file+'.out','1 40.0  768.0  551.7  551.7    0.0        0.000','enrich.csv')
    enrich = np.genfromtxt('enrich.csv')
    enrichment = (enrich[12])
    print(enrichment)

    #Separative Work Unit (SWU) Calculations
    xp = enrichment/100 #concentration of the product uranium
    xf = 0.00711 #concentration of the feed uranium (0.71% natural)
    xt = 0.002 #concentration of the tails (.2% by weight)
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
    # -------------------
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
    fitness = 100 + 100*(ppf-1.6) + 1000*(0.85-kvals) + cost/10
    print(fitness)
    
    #perserve data
    #-------------
    #delete all the files
    l = ff(init_file)
    p=0
    for p in range(len(l)):
        os.remove(l[p])
    
    #save results
    #------------
    #open file with access mode 'a'
    #write results (vector/fitness) to file
    with open("results.csv", "a") as file_object:
        file_object.write(str(vec)+'; '+str(fitness)+'; '+str(kvals)+'; '+str(ppf)+'\n')
    return fitness