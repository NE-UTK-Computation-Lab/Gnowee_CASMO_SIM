# this is a file for containing the methods and classes used to 
#store past results to prevent redundent evaluations

#NOTE: CURRENTLY ONLY APPROPRIATE FOR SINGLE OBJECTIVE FUNCTION SITUATIONS

import pickle
import os
import numpy as np

Default_FileName = "DefaultResultLibName"
DefaultColumnNames = ["feature_vectors", "fittness", "EvaluationNumber"]
DefaultkeyColumnIndex = 0
DefaultValueColumnIndex = 1

class resultsLibrary:
    def __init__(self, FileName, ColumnNames, keyColumnIndex, ValueColumnIndex, fileFolder =os.getcwd(), numObjectiveFunctions = 1):
        #INPUTS:
        #FileName: the name under which the data is saved as a file
        #ColumnNames: an ORDERED list of strings specifying the names of the data columns
        #keyColumnIndex: an index number which specifies which column contains the dictionary key
        # typically the keys will be the feature vectors and will be stored as strings
        #ValueColumnIndex: similar to key columnIndex in that it specifies which data column contain the values
        #that corespond to the keys 
        #fileFolder: a path object or string specifying the name of the subfolder in which the data will be stored
        self.ColumnNames = ColumnNames
        self.keyColumnIndex = keyColumnIndex
        self.ValueColumnIndex = ValueColumnIndex
        self.FileFolder = fileFolder
        self.FileName = FileName
        self.NumObjectiveFunctions = numObjectiveFunctions
        if self.NumObjectiveFunctions != 1:
            self.advanced_data = [{}]
            for x in range(numObjectiveFunctions-1):
                self.advanced_data.append({})
            print ("Advanced data is stored as a :")
            print(type(self.advanced_data))
        else:
            self.basic_data = {} #the basic dictionary for storing past results
        self.LatestPopulation = []

def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)
def save_object(obj, name):
    savefilename = name +".pickle"
    try:
        with open(savefilename, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

class resultsLibray_Interface:
    def __init__(self, FileName = Default_FileName, ColumnNames = DefaultColumnNames, keyColumnIndex = DefaultkeyColumnIndex, ValueColumnIndex = DefaultValueColumnIndex, Filelocation = os.getcwd(), numObjectiveFunctions = 1):
        # check if file already exists
        self.FileName = FileName
        self.currentLocation= os.getcwd()
        self.Filelocation = Filelocation
        self.FileName_and_Path = os.path.join(Filelocation, FileName+'.pickle')
        os.chdir(self.Filelocation)
        if FileName+'.pickle' in os.listdir():
            AlreadyExists = True
            print("File Already Exists")
            #set the file parameters based on the pre-existing file
            self.result_Lib = load_object(self.FileName_and_Path)
            self.ColumnNames = ColumnNames
            self.keyColumnIndex = keyColumnIndex
            self.ValueColumnIndex = ValueColumnIndex
            self.NumObjectiveFunctions = numObjectiveFunctions
            if self.NumObjectiveFunctions == 1:
                self.basic_data_internal = self.result_Lib.basic_data
            else:
                self.advanced_data_internal = self.result_Lib.advanced_data
            self.LatestPopulation = self.result_Lib.LatestPopulation
        else:
            AlreadyExists = False
            print("Creating Results Library")
            #set the file parameters based on the pre-existing file
            self.ColumnNames = ColumnNames
            self.keyColumnIndex = keyColumnIndex
            self.ValueColumnIndex = ValueColumnIndex
            self.NumObjectiveFunctions = numObjectiveFunctions

            self.result_Lib = resultsLibrary(self.FileName, self.ColumnNames, self.keyColumnIndex, self.ValueColumnIndex, self.Filelocation, self.NumObjectiveFunctions)
            if self.NumObjectiveFunctions == 1:
                print("BASIC")
                self.basic_data_internal = self.result_Lib.basic_data #used in part to avoid constantly reading from the hard disc
            else:
                print("ADVANCED")
                self.advanced_data_internal = self.result_Lib.advanced_data
            print("num Objective Functions")
            self.LatestPopulation = self.result_Lib.LatestPopulation
            save_object(self.result_Lib, FileName)


        os.chdir(self.currentLocation)

    def feature_vector_to_key(self, feature_vector):
        #this function converts a feature vector to a searchable key in the dictionary
        key_string = ' '.join(map(str, feature_vector))
        return key_string

    def isInLibrary(self, feature_vector):
        #this function searches the data libary to see if a feature vector has previously been evaluated
        #print(np.shape(feature_vector))
        searchkey = self.feature_vector_to_key(feature_vector)
        if self.NumObjectiveFunctions == 1:
            if searchkey in self.basic_data_internal:
                return True
            else:
                return False
        else:
            if searchkey in self.advanced_data_internal[0]: #only have to check the first dictionary
                return True
            else:
                return False
    def weed_list(self, list_of_feature_vectors):
        #this function takes in a list of feature vectors and returns the same list but without previously evaluated feature vectors
        num_vec = len(list_of_feature_vectors)
        new_list = []
        for i in range(0,num_vec):
            if not self.isInLibrary(list_of_feature_vectors[i]):
                new_list.append(list_of_feature_vectors[i])
        return new_list

    def add_to_lib(self, feature_vector, fitness):
        key = self.feature_vector_to_key(feature_vector)
        if self.NumObjectiveFunctions == 1:
            self.result_Lib.basic_data[key] = fitness
            self.basic_data_internal[key] = fitness
        else:
            #in this case, fitness should be a vector of fitnesses for each objective function
            #it will be important that the ordering of the objective functions and fittness remains consistant
            numFitnesses = len(fitness)
            if numFitnesses != self.NumObjectiveFunctions:
                print("Critical Error, the number of fitnesses does not match the number of objective functions when adding to library")
                return False
            else:
                for i in range(numFitnesses):
                    self.result_Lib.advanced_data[i][key] = fitness[i]
                    self.advanced_data_internal[i][key] = fitness[i]
        return True

    def SavePopulation(self, listOfFeatureVectors):
        numVec = len(listOfFeatureVectors)
        self.LatestPopulation = []
        for i in range(0, numVec):
            self.LatestPopulation.append(self.feature_vector_to_key(listOfFeatureVectors[i]))
        self.result_Lib.LatestPopulation = self.LatestPopulation

    def SaveLib(self):
        #saves the library to the dics
        if self.NumObjectiveFunctions == 1:
            self.result_Lib.basic_data = self.basic_data_internal
        else:
            self.result_Lib.advanced_data = self.advanced_data_internal
        self.result_Lib.LatestPopulation = self.LatestPopulation
        save_object(self.result_Lib, self.FileName)

    def LoadLib(self):
        #used in part to avoid constantly reading from the hard disc
        #will load the saved file into memory
        self.result_Lib = load_object(self.FileName)

    def getFitness(self, feature_vector, fitnessIndex = 0):
        #fitness index specifies the index of the dictionary within which that data is stored, it should only be relevant if there is ore than one objective function
        key = self.feature_vector_to_key(feature_vector)
        if self.NumObjectiveFunctions == 1:
            Fitness = self.basic_data_internal[key]
            print("Basic")
        else:
            Fitness = self.advanced_data_internal[fitnessIndex][key]
            print(Fitness)
            print("Advanced")
        print("Type of fitness:")
        print(type(Fitness))
        return Fitness
