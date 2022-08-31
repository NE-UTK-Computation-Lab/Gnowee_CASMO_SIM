# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 22:52:41 2021

Original script authored by Chris Busch

This version was edited and commentated by Madison Tippet for use with CASMO/SIMULATE

"""

#import statementes
import fileinput
import numpy as np
import pandas as pd
import time
import os
import os.path



#%% Program generation functions / numerical replacers

#Program Generation - this generates a new file that takes the mock file and
#                     replaces the variable names (<var#>) with the variable
#                     inputs (fuel types)
#Note: variable names and values must be the same length

#inputs:
#proposed_filename = new file you are generating
#mock_input = the base input file
#var_values = variable values to input (vector or array)
#n = number of variables

#output:
#proposed_filename = the new file generated
def program_gen(proposed_filename,mock_input,var_values,n): 

    #this generates the variable names that the program will search for & change
    #the format is <var0> and can be changed by user if desired
    varnames = []
    
    for i in range(n):
        v= '<var'+str(i)+'>'
        varnames.append(v)
        
        #new file is generated; copy of old/mock file; w/ proposed file name
    with open(mock_input) as f:
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

#------------------------------------------------------------------------------
#Program Generation 2 - this generates a new file that takes the mock file and
#                       replaces the variable names (<int#> and <ext#>) with 
#                       the variable inputs (i.e. fuel types w/ and w/out 
#                       gadolinia depending on location)
#Note: variable names and values must be the same length

#inputs:
#proposed_filename = new file you are generating
#mock_input = the base input file
#var_values1 = variable values to input (vector or array) INTERIOR
#var_values2 = variable values to input (vector or array) EXTERIOR
#n1 = number of fuel type variables w/ and w/out gad (INTERIOR)
#n2 = number of fuel type variables w/out gad (EXTERIOR)

#output:
#proposed_filename = new file generated
def program_gen2(proposed_filename,mock_input,var_values1,var_values2,n1,n2): 

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
    with open(mock_input) as f:
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

#Variable Data - Gnowee will pick a fuel type / blade notch which is then input 
#                into the function; the function then returns all variable info
#                to be written into the mock input file

#input:
#variables = csv file with all possible variables; number of variable values
#            must be >= number of variable positions (n in program_gen)
#Note: in csv file, after each variable value, add a line that says 'c start'
#      for discretion between values

#output:
#var_numhold = variable info for the var_writer
def var_data(variables):
    #read variables from csv file
    data = pd.read_csv(variables,delimiter = ',', skiprows = 0)        
    data = data.to_numpy()
    
    #put variable values in var_num list
    i = 0
    var_num = []
    while i<len(data):
        if data[i,0] == 'c start':
            i2 = i+1
            var_num.append(data[i2,0])
            i=i+1
        else:
            i=i+1
            
    #convert fuel types / blade notches to strings
    #add index of fuel types / blade notches to indexes list
    indexes = []
    for i in range(len(var_num)):
        var_num[i]=str(var_num[i])
        indexes.append(var_num.index(var_num[i],0))
        
    #return information for each fuel type / blade notch
    var_numhold = []
    for i in range(len(indexes)):
        # variable number
        fh = var_num[indexes[i]]
        var_numhold.append(fh)
    return var_numhold

#------------------------------------------------------------------------------
#Variable Data 2 - used when the lattice edges are constrained (no gadolinia) / or 
#             when two different variable vectors are used

#inputs:
#var_int = csv file with all fuel types permitted in the interior of lattice
#var_ext = csv file with all fuel types permitted in the exterior of lattice

#outputs:
#var_numhold1, var_numhold2 = variable info for the var_writer
def var_data2(var_int,var_ext):
    #read fuel types from csv file
    #interior
    data1 = pd.read_csv(var_int,delimiter = ',', skiprows = 0)        
    data1 = data1.to_numpy()
    #exterior
    data2 = pd.read_csv(var_ext,delimiter = ',', skiprows = 0)        
    data2 = data2.to_numpy()
    
    #put fuel types in variable number list
    i = 0
    var_num1 = []
    var_num2 = []
    
    while i<len(data1):
        if data1[i,0] == 'c start':
            i2 = i+1
            var_num1.append(data1[i2,0])
            i=i+1
        else:
            i=i+1
    
    j = 0
    while j<len(data2):
        if data2[j,0] == 'c start':
            j2 = j+1
            var_num2.append(data2[j2,0])
            j=j+1
        else:
            j=j+1
            
    #convert fuel types to strings
    #add index of fuel types to indexes list
    indexes1 = []
    for i in range(len(var_int)):
        var_int[i]=str(var_int[i])
        indexes1.append(var_num1.index(var_int[i],0))
    
    indexes2 = []
    for j in range(len(var_ext)):
        var_ext[j]=str(var_ext[j])
        indexes2.append(var_num2.index(var_ext[j],0))
        
    #return information for each fuel type
    var_numhold1 = []
    var_numhold2 = []
    
    for i in range(len(indexes1)):
        # fuel number
        fn1 = var_num1[indexes1[i]]
        var_numhold1.append(fn1)
        
    for j in range(len(indexes2)):
        fn2 = var_num2[indexes2[j]]
        var_numhold2.append(fn2)
        
    return var_numhold1, var_numhold2

#------------------------------------------------------------------------------
#Variable Writer - creates variables that are found & replaced '<var0>'

#inputs:
#proposed_filename = new file you are generating
#ind = variable (i.e. fuel) information from the variable selector module
#n = number of variables/fuel types

#output:
#proposed_filename = new file generated
def var_writer(proposed_filename,ind,n): 

    #creates list of variable names to find&replace   
    varnum = []
    for i in range(n):
        v = '<var'+str(i)+'>'
        varnum.append(v)

    #variable changer; these loops read the file from the program generation
    #function and replace the variable names with variable selected
    if n<len(ind):
        for j in range(n):
            with fileinput.FileInput(proposed_filename, inplace=True) as file:
                for line in file:
                    print(line.replace(varnum[j], str(ind[j])), end='')
            file.close()
    else:
        for o in range(len(ind)):
            with fileinput.FileInput(proposed_filename, inplace=True) as file:
                for line in file:
                    print(line.replace(varnum[o], str(ind[o])), end='')
            file.close()

    return proposed_filename

#------------------------------------------------------------------------------

#Variable Writer 2 - creates variables that are found & replaced for both
#                the internal and external (edge) lattice positions
#                ('<int0>' and '<ext0>')

#inputs:
#proposed_filename = new file you are generating
#ind1 = variable/fuel information from the fuel selector module (INTERIOR)
#ind2 = variable/fuel information from the fuel selector module (EXTERIOR)
#n1 = number of fuel type variables w/ and w/out gad (INTERIOR)
#n2 = number of fuel type variables w/out gad (EXTERIOR)

#output:
#proposed_filename = new file generated 
def var_writer2(proposed_filename,ind1,ind2,n1,n2): 

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



#%%Job submission function

#Run on Cluster - this creates and submits a script to the UTK NE Cluster to 
#                 perform runs in CASMO-4 or SIMULATE-3


#boolean: True to submit jobs, False to check how many jobs will be submitted
submit_jobs = True
#Note: script information must be adjusted to represent one's cluster
cluster_input_string_casmo = """#!/bin/bash
#PBS -V
#PBS -q fill
#PBS -l nodes=1:ppn=8

hostname
cd ${PBS_O_WORKDIR}

module load studsvik
casmo4 %%%INPUT%%%.inp
grep -a "Run Completed" %%%INPUT%%%.out > %%%INPUT%%%_done.dat"""

cluster_input_string_sim = """#!/bin/bash
#PBS -V
#PBS -q fill
#PBS -l nodes=1:ppn=8

hostname
cd ${PBS_O_WORKDIR}

module load studsvik
simulate3 %%%INPUT%%%.inp
grep -a "SUMMARY" %%%INPUT%%%.out > %%%INPUT%%%_done.dat"""

#inputs:
#common_string = string representing name of input file and all related files
#                to the optimization
#solver = string noting which code to use

#output:
#list_of_jobs_submitted = list of job numbers successfully submitted to the
#                         UTK NE Cluster
def run_on_cluster(common_string,solver):
    list_of_jobs_submitted = []

    for file in os.listdir('.'):
        # Checking if file ends in ".inp" and if the flag is in the filename
        if file.endswith(".inp") == False:
            continue
        if common_string not in file:
            continue
        print("Creating cluster script for job: " + file)

        if solver == 'casmo':
            script_string = cluster_input_string_casmo
        if solver == 'sim':
            script_string = cluster_input_string_sim
        
        script_string = script_string.replace("%%%INPUT%%%", file.replace('.inp',''))
        script_file_string = file.replace('.inp','_script.txt') 
        script_file = open(script_file_string, 'w')
        script_file.write(script_string)
        script_file.close()
        time.sleep(5)

        print("Submitting job: " + file)
        list_of_jobs_submitted.append(file)
        current_Dir = os.getcwd()

        if submit_jobs == True:
            # This line submits the job
            os.system('qsub ' + script_file_string + '>> cluster_submission.txt')
            # template=open('cluster_submission.txt','r')
            while not os.path.exists(file.replace('.inp','_done.dat')):
                template=open('cluster_submission.txt','r')
                for line in template:
                    if 'socket_connect_unix failed' in line:
                        os.remove('cluster_submission.txt')
                        time.sleep(5)
                        os.system('ssh -tt necluster.ne.utk.edu "cd ' + current_Dir + ' && qsub ' + script_file_string+'>> cluster_submission.txt'+'"')
                    else:
                        print('Job not complete waiting 15 seconds')
                        time.sleep(15)
                        
            template.close()
        os.remove('cluster_submission.txt')
    return list_of_jobs_submitted


#%% file check program

#File Check - checks that the specific number of files were created containing
#             the common string designated by user

#inputs:
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

#------------------------------------------------------------------------------
#File Find - this function finds and returns all the filenames with the common 
#            string; Python uses this to identify which files to delete after 
#            desired results are extracted and stored; maintains apt memory 

#input:
#com_str = common string that created files contain; proposed file name

#output:
#names = names of files containing the common string
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

#%% Get Results function

# Get Results - searches output file for a specific string & returns that line
#               or if string is not found, it returns a blank list  

#inputs:
#file_name = name of the output file to search
#string_to_search = string to search to locate desired results line
#results_filename = string to name the csv file that results will print to

#output:
#result = csv file of the results in the desired line
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

#------------------------------------------------------------------------------
#Get Table function
#authored by Madison Tippet

#Get Table - searches for a section or table name and extracts the table below;
#            this is repeated for the table at each statepoint / exposure point
#            (or for other codes, each time it appears)

#inputs:
#file_name = name of output file to search
#section_title = string to search to identify the table
#results_filename = string to name the csv file that results will print to
#header_lines = the number of lines to count as headers to the table
#points = the number of data points in the table

#output:
#result = csv file and list of all tables with desired title
def get_table(file_name, section_title, results_filename, header_lines, points):
    result = []
    # Open the file in read only mode
    with open(file_name,'r') as read_obj:
        #split '.out' file into rows
        # read_obj = read_obj.split("/n")
        
        #read all lines one by one
        for line in read_obj:
            if section_title in line:
                res = line
                result.append(res)
                # with open(results_filename, "a") as file_object:
                #     file_object.write(str(line) +'\n')
                for i in range(points+header_lines):   
                    res = next(read_obj)
                    result.append(res)
                    # with open(results_filename, "a") as file_object:
                    #     file_object.write(str(line) +'\n')
    np.savetxt(results_filename, result, fmt ='%s')
    return result

#------------------------------------------------------------------------------
#Get Column function
#authored by Madison Tippet

#Get Column - takes a table from the get_table function and extracts specific
#             columns from it

#inputs:
#table = results/table from get_table function
#header_lines = the number of lines to count as headers to the table
#points = the number of data points in the table

#outputs:
#parameter = desired column from the last statepoint table (i.e. End of Cycle)
#parameter_list = list of each column from all statepoint tables
#max_parameter_list = list of maximum values from each statepoint column 
#max_parameter =  maximum value from all statepoint columns
def get_column(table, header_lines, points, column_num):
    parameter_list = []
    max_parameter_list = []
    i = header_lines
    while i<len(table):
        j = i+points
        datalist = table[i:j]
        parameter = np.genfromtxt(datalist,usecols=(column_num))
        parameter_list.append(parameter)
        max_parameter_list.append(np.max(parameter))
        i = i + points + header_lines + 1
    max_parameter_list = np.array(max_parameter_list)
    max_parameter = np.max(max_parameter_list)
    return(parameter,parameter_list,max_parameter_list,max_parameter)


