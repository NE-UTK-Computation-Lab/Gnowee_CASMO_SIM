# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 22:52:41 2021

@author: madison
"""

#import statementes
import fileinput
import numpy as np
import pandas as pd
import time
import os
import os.path
# from os import path



#%% Program generation functions / numerical replacers

#Program Generation - this generates a new file that takes the mock file and
#replaces the variable names (<var#>) with the variable inputs (fuel types)
#Note: variable names and values must be the same length

#inputs for this module are:
#proposed_filename = new file you are generating
#mock_CASMO = the base input file
#var_values = variable values to input (vector or array)
#n = number of variables
def program_gen(proposed_filename,mock_CASMO,var_values,n): 

    #this generates the variable names that the program will search for & change
    #the format is <var0> and can be changed by user if desired
    varnames = []
    
    for i in range(n):
        v= '<var'+str(i)+'>'
        varnames.append(v)
        
        #new file is generated; copy of old/mock file; w/ proposed file name
    with open(mock_CASMO) as f:
        with open(proposed_filename, "w") as f1:
            for line in f:
                f1.write(line)
        f1.close()
    f.close()
    
    
    #new file is opened and variable names are replaced with variable inputs
    var_valuesn = []
    
    for k in range(len(var_values)):
        var_valuesn.append(str(var_values[k]))
    
    for o in range(len(var_values)):
        with fileinput.FileInput(proposed_filename, inplace=True) as file:
            for line in file:
                print(line.replace(varnames[o], var_valuesn[o]), end='')
        file.close()

    #program returns the new edited file  
    return proposed_filename



#Program Generation 2 - this generates a new file that takes the mock file and
#replaces the variable names (<int#> and <ext#>) with the variable inputs
#(i.e. fuel types w/ and w/out gadolinia depending on location)
#Note: variable names and values must be the same length

#inputs for this module are:
#proposed_filename = new file you are generating
#mock_CASMO = the base input file
#var_values1 = variable values to input (vector or array) INTERIOR
#var_values2 = variable values to input (vector or array) EXTERIOR
#n1 = number of fuel type variables w/ and w/out gad (INTERIOR)
#n2 = number of fuel type variables w/out gad (EXTERIOR)
def program_gen2(proposed_filename,mock_CASMO,var_values1,var_values2,n1,n2): 

    #this generates the variable names that the program will search for & change
    #the format is <var0> and can be changed by user if desired
    varnames1 = []
    varnames2 = []
    
    #this section is for the interior fuel; includes all types
    for i in range(n1):
        v1 = '<int'+str(i)+'>'
        varnames1.append(v1)
        
    #this section is for the edge fuel; no gadolinia  
    for j in range(n2):
        v2 = '<ext'+str(j)+'>'
        varnames2.append(v2)
    
    #new file is generated; copy of old/mock file; w/ proposed file name
    with open(mock_CASMO) as f:
        with open(proposed_filename, "w") as f1:
            for line in f:
                f1.write(line)
        f1.close()
    f.close()
    
    #new file is opened and variable names are replaced with variable inputs
    var_valuesn1 = []
    var_valuesn2 = []
    
    for k in range(len(var_values1)):
        var_valuesn1.append(str(var_values1[k]))
    
    for o in range(len(var_values1)):
        with fileinput.FileInput(proposed_filename, inplace=True) as file:
            for line in file:
                print(line.replace(varnames1[o], var_valuesn1[o]), end='')
        file.close()
    
    for l in range(len(var_values2)):
        var_valuesn2.append(str(var_values2[l]))
    
    for d in range(len(var_values2)):
        with fileinput.FileInput(proposed_filename, inplace=True) as file:
            for line in file:
                print(line.replace(varnames2[d], var_valuesn2[d]), end='')
        file.close()

    #program returns the new edited file  
    return proposed_filename



#%% Variable selector/data/replacer; all variable related functions:


#Fuel Data - Gnowee will pick a fuel type number which is then input into the
#function; the function then returns all variable info to be written into the
#CASMO mock file

#input for this function is:
#fuen = fuel type number for lattice optimization / variable number for other
def fuel_data(fuen):
    #read fuel types from csv file
    data = pd.read_csv('fueltypes.csv',delimiter = ',', skiprows = 0)        
    data = data.to_numpy()
    
    #put fuel types in fuel_num list
    i = 0
    fuel_num = []
    while i<len(data):
        if data[i,0] == 'c start':
            i2 = i+1
            fuel_num.append(data[i2,0])
            i=i+1
        else:
            i=i+1
            
    #convert fuel types to strings
    #add index of fuel types to indexes list
    indexes = []
    for i in range(len(fuel_num)):
        fuel_num[i]=str(fuel_num[i])
        indexes.append(fuel_num.index(fuel_num[i],0))
        
    #return information for each fuel type
    fuel_numhold = []
    for i in range(len(indexes)):
        # fuel number
        fh = fuel_num[indexes[i]]
        fuel_numhold.append(fh)
    return fuel_numhold


#Fuel Data 2 - used when the lattice edges are constrained (no gadolinia)

#inputs for this function are:
#fuen_int = fuel type number (INTERIOR)
#fuen_ext = fuel type number (EXTERIOR)
def fuel_data2(fuen_int,fuen_ext):
    #read fuel types from csv file
    #interior
    data1 = pd.read_csv('fueltypes_int.csv',delimiter = ',', skiprows = 0)        
    data1 = data1.to_numpy()
    #exterior
    data2 = pd.read_csv('fueltypes_ext.csv',delimiter = ',', skiprows = 0)        
    data2 = data2.to_numpy()
    
    #put fuel types in fuel number list
    i = 0
    fuel_num1 = []
    fuel_num2 = []
    
    while i<len(data1):
        if data1[i,0] == 'c start':
            i2 = i+1
            fuel_num1.append(data1[i2,0])
            i=i+1
        else:
            i=i+1
    
    j = 0
    while j<len(data2):
        if data2[j,0] == 'c start':
            j2 = j+1
            fuel_num2.append(data2[j2,0])
            j=j+1
        else:
            j=j+1
            
    #convert fuel types to strings
    #add index of fuel types to indexes list
    indexes1 = []
    for i in range(len(fuen_int)):
        fuen_int[i]=str(fuen_int[i])
        indexes1.append(fuel_num1.index(fuen_int[i],0))
    
    indexes2 = []
    for j in range(len(fuen_ext)):
        fuen_ext[j]=str(fuen_ext[j])
        indexes2.append(fuel_num2.index(fuen_ext[j],0))
        
    #return information for each fuel type
    fuel_numhold1 = []
    fuel_numhold2 = []
    
    for i in range(len(indexes1)):
        # fuel number
        fh1 = fuel_num1[indexes1[i]]
        fuel_numhold1.append(fh1)
        
    for j in range(len(indexes2)):
        fh2 = fuel_num2[indexes2[j]]
        fuel_numhold2.append(fh2)
        
    return fuel_numhold1, fuel_numhold2



#Fuel Writer - creates variables that are found & replaced '<var0>'

#inputs for this function are:
#proposed_filename = new file you are generating
#ind = variable/fuel information from the fuel selector module
#n = number of variables/fuel types
def fuelwriter(proposed_filename,ind,n): 

    #creates list of variable names to find&replace   
    varnum = []
    for i in range(n):
        v = '<var'+str(i)+'>'
        varnum.append(v)

    #variable changer; these loops read the file from the program generation
    #function and replace the variable names with fuel number selected
    for o in range(len(ind)):
        with fileinput.FileInput(proposed_filename, inplace=True) as file:
            for line in file:
                print(line.replace(varnum[o], str(ind[o])), end='')
        file.close()

    return proposed_filename


#Fuel Writer 2 - creates variables that are found & replaced for both
#the internal and external (edge) lattice positions '<int0>' and '<ext0>'

#inputs for this function are:
#proposed_filename = new file you are generating
#ind1 = variable/fuel information from the fuel selector module (INTERIOR)
#ind2 = variable/fuel information from the fuel selector module (EXTERIOR)
#n1 = number of fuel type variables w/ and w/out gad (INTERIOR)
#n2 = number of fuel type variables w/out gad (EXTERIOR)
def fuelwriter2(proposed_filename,ind1,ind2,n1,n2): 

    #creates list of variable names to find&replace   
    varnum1 = []
    varnum2 = []
    
    for i in range(n1):
        v1 = '<int'+str(i)+'>'
        varnum1.append(v1)

    for j in range(n2):
        v2 = '<ext'+str(j)+'>'
        varnum2.append(v2)
        
    #variable changer; these loops read the file from the program generation
    #function and replace the variable names with fuel number selected
    for o in range(len(ind1)):
        with fileinput.FileInput(proposed_filename, inplace=True) as file:
            for line in file:
                print(line.replace(varnum1[o], str(ind1[o])), end='')
        file.close()

    for k in range(len(ind2)):
        with fileinput.FileInput(proposed_filename, inplace=True) as file:
            for line in file:
                print(line.replace(varnum2[k], str(ind2[k])), end='')
        file.close()
      
    return proposed_filename



#%%
######### Job submission function -- in progress for CASMO

#developing and running script to submit CASMO4 jobs to necluster
solver = 'casmo4'
#boolean: True to submit jobs, False to check how many jobs will be submitted
submit_jobs = True
cluster_input_string = """#!/bin/bash
#PBS -V
#PBS -q fill
#PBS -l nodes=1:ppn=8

hostname
cd ${PBS_O_WORKDIR}

module load studsvik
casmo4 %%%INPUT%%%.inp
grep -a "Run Completed" %%%INPUT%%%.out > %%%INPUT%%%_done.dat"""


def run_on_cluster(common_string):
    list_of_jobs_submitted = []

    for file in os.listdir('.'):
        # Checking if file ends in ".inp" and if the flag is in the filename
        if file.endswith(".inp") == False:
            continue
        if common_string not in file:
            continue
        print("Creating cluster script for CASMO job: " + file)

        script_string = cluster_input_string
        script_string = script_string.replace("%%%INPUT%%%", file.replace('.inp',''))
        script_file_string = file.replace('.inp','_script.txt') 
        script_file = open(script_file_string, 'w')
        script_file.write(script_string)
        script_file.close()
        time.sleep(5)

        print("Submitting CASMO job: " + file)
        list_of_jobs_submitted.append(file)

        if submit_jobs == True:
            # This line submits the job
            os.system('qsub ' + script_file_string)
            # template=open('cluster_submission.txt','r')
#NOTE: SEEMS THIS FILE DOES NOT EXIST AND WE GET STUCK IN INF LOOP
            # while not os.path.exists(file.replace('.inp','_done.dat')):
            #     template=open('cluster_submission.txt','r')
            #     for line in template:
            #         if 'socket_connect_unix failed' in line:
            #             os.remove('cluster_submission.txt')
            #             time.sleep(5)
            #             os.system('ssh -tt necluster.ne.utk.edu "cd ' + current_Dir + ' && qsub ' + script_file_string+'>> cluster_submissions.txt'+'"')
            #         else:
            #             print('Job not complete waiting 15 seconds')
            #             time.sleep(15)
                        
            # template.close()
        # os.remove('cluster_submission.txt')
    return list_of_jobs_submitted


#%% file check program
#checks that the specific number of files were created
#files should contain a common string given by user

#inputs are:
#com_str = common string that new files contain; should be proposed file name
#file_num = how many files are expected
def file_check(com_str,file_num):

    # files = os.listdir(os.getcwd())
    # count = 0
    # i = 0
    trials = 0
    minute = .25
    time.sleep(60*minute)
    
    while trials<10000:
        files = os.listdir(os.getcwd())
        i = 0
        count = 0
        
        while i<(len(files)):
            # files = os.listdir(os.getcwd())
            if com_str in files[i]:
                count = count + 1
                i = i + 1
            else:
                i = i + 1 
        
        if file_num==count:
            print('yes it is complete ')
            finish = 1
            break
        else:
            print('no '+str(trials))
            time.sleep(60*minute)
            trials = trials + 1
            
    return finish



#File Find function
#this function finds and returns all the filenames with the common string
#Python uses this to identify which files to delete to maintain apt memory
#this is performed after desired results are extracted and stored

#input is:
#com_str = common string that created files contain; proposed file name
def file_find(com_str):

    i = 0  
    names = []
    files = os.listdir(os.getcwd())
    while i<(len(files)):
        if com_str in files[i]:
            names.append(files[i])
            i = i + 1
        else:
            i = i + 1
    return names

#%%
#Get Results function
#this function searches output file for a specific string & returns that line
#if your string does not match it returns a blank list  

#inputs are:
#file_name = name of the output file to search
#string_to_search = string to search to locate desired results line
#results_filename = string to name the csv file that the results will print to
def get_results(file_name, string_to_search, results_filename):

    #open the file in read only mode
    result = []
    with open(file_name, 'r') as read_obj:
        #read all lines in the file one by one
        for line in read_obj:
            #for each line, check if line contains the string
            #if it does, copy that line of text
            if string_to_search in line:
                res = True, line
                result.append(res)
    #save the result array to a results csv
    np.savetxt(results_filename,result,fmt ='%s')
    return result


########
