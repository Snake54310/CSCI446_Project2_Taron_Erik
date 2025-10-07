import math
import numpy as np
import os
import random 
import sys
import re
import copy as cp
from Knowledge import Knowledge

def fileImport(fileName): # brings file into program as str numpy array
    
    puzzleStart = np.genfromtxt(fileName, dtype=str, encoding=None, delimiter='\n')
    return puzzleStart

def createMap(fileInfo): # initializes a properly sized array representing known values of system
    puzzleSize = fileInfo[0][6:]
    puzzleDimensions = puzzleSize.split('x')
    puzzleRC = int(puzzleDimensions[0])
    # this boolean states array contains booleans variables on the following data: 
    # 0) safe, 1) unsafe, 2) breeze, 3) stench, 4) given
    booleanStatesZeros = np.zeros((5, puzzleRC, puzzleRC), dtype=int);
    booleanStates = booleanStatesZeros.astype(bool)
    
    for location in fileInfo[3: -2]: # for every given location (cell)
        # split by (, <commas>, ), :
        rowCol =  re.split(r"[(,):]\s*", location)  # https://pythonguides.com/split-strings-with-multiple-delimiters-in-python/
        row = int(rowCol[1])
        col = int(rowCol[2])
        breeze = rowCol[4][0]
        stench = rowCol[5][0]
            
        breezeStatus = False
        stenchStatus = False
        if (breeze == "T"):
            breezeStatus = True
            #print("breeze: " + str(row) + str(col)) 
        if (stench == "T"):
            stenchStatus = True
            #print("stench: " + str(row) + str(col)) 
        
        # breeze status of cell is
        booleanStates[2][row][col] = breezeStatus
        # stench status of cell is
        booleanStates[3][row][col] = stenchStatus
        # booleanStates[0][row][col] = True # cells 'visited' are always safe # maybe delete 
        booleanStates[4][row][col] = True # track given 
        # (part of knowledge base)
        
    return booleanStates

def retrieveOtherInfo(fileInfo):
    
    queryCellText = fileInfo[-2]
    arrows = int((fileInfo[1].split(' '))[1]) # 2nd line, all characters after ' ' converted     # to an integer
    
    # split by (, <commas>, ) 
    queryLineInfo = re.split(r"[(,)]\s*", queryCellText) 
    
    
    query = [int(queryLineInfo[-3]), int(queryLineInfo[-2])]
    query_arrows = (query, arrows)
    return query_arrows
    
def createHolesWompuses(booleanStates):
    # creates an initial array of:
    # 0) there could be a hole 1) there could be a wompus
    # 2) there is a hole 3) there is a wompus
    # will likely need changes to conform to the project requirements, but it 
    # might be a useful draft
    # maybe 'part of knowledge base'
    arraysShape = booleanStates.shape
    holesWompusesZeros = np.zeros((4, arraysShape[0], arraysShape[1]), dtype=int)
    holesWompuses = holesWompusesZeros.astype(bool)
    for row in range(arraysShape[1]):
        for col in range(arraysShape[2]):
            holesWompuses[0] = True
            holesWompuses[1] = True
    
    return holesWompuses
    
    
    
    
def saveOutput(deduction, clausesArray, GROUP_ID, PUZZLE_PATH): # saves solved puzzle to output file
    fileName = GROUP_ID + "_" + PUZZLE_PATH[-11:-4] + ".txt"
    writeString = ""
    for clause in clausesArray:
        writeString += clause
        writeString += "\n"
  
    writeString += "\n"
    writeString += "QUERY: " + deduction
    with open(fileName, "w") as f:
        f.write(writeString)
        
    return

def testQuery(booleanStates, holesWompuses, arrows, query):
    test1 = 0 # set 0, -1 for testing
    knowledgeBase1 = Knowledge(booleanStates, holesWompuses, arrows, query, test1)
    knowledgeBase1.initializeKnowledge()
    Changed = True
    
    while Changed:
        Changed = False
        Changed = knowledgeBase1.resolveStatements()
        if (Changed == -1):
            print("0) safe, 1) unsafe, 2) breeze, 3) stench, 4) given")
            print(knowledgeBase1.getBooleanStates())
            print("0) there could be a hole 1) there could be a wompus 2) there is a hole 3) there is a wompus")
            print(knowledgeBase1.getHolesWompuses())
            print("SAFE")
            return "SAFE"
        
    print("0) safe, 1) unsafe, 2) breeze, 3) stench, 4) given")
    print(knowledgeBase1.getBooleanStates())
    print("0) there could be a hole 1) there could be a wompus 2) there is a hole 3) there is a wompus")
    print(knowledgeBase1.getHolesWompuses())
    
    print("remaining clauses:")
    remainingClauses = knowledgeBase1.getClausesQueue()
    for i in remainingClauses:
        print(i)
    
    print("BREAKKKKKKKKKKKK")    
        
    
    test0 = 1 # set 1
    knowledgeBase0 = Knowledge(booleanStates, holesWompuses, arrows, query, test0)
    knowledgeBase0.initializeKnowledge()
    Changed = True
    finalkb = knowledgeBase1.getKnowledgeBase()
    #for i in finalkb:
        #print(i)
    
    while Changed:
        Changed = False
        Changed = knowledgeBase0.resolveStatements()
        if (Changed == -1):
            print("UNSAFE")
            return "UNSAFE"

    print("0) safe, 1) unsafe, 2) breeze, 3) stench, 4) given")
    print(knowledgeBase0.getBooleanStates())
    print("0) there could be a hole 1) there could be a wompus 2) there is a hole 3) there is a wompus")
    print(knowledgeBase0.getHolesWompuses())
    
    print("remaining clauses:")
    remainingClauses2 = knowledgeBase0.getClausesQueue()
    #for i in remainingClauses2:
        #print(i)
    
    print("RISKY")
    return "RISKY"
        
    
    

def main(GROUP_ID, PUZZLE_PATH): 
    
    fileName = PUZZLE_PATH 
    fileInfo = fileImport(fileName)
    booleanStates = createMap(fileInfo)
    
    query_arrows = retrieveOtherInfo(fileInfo)
    #print(query_arrows) # working correctly here
    
    query = query_arrows[0]
    arrows = query_arrows[1]
    clausesArray = [] # placeholder

    holesWompuses = createHolesWompuses(booleanStates)
    
    
    
    deduction = testQuery(booleanStates, holesWompuses, arrows, query)
    # output stuff
    if (booleanStates[0][query[0]][query[1]] == True): 
        deduction = "SAFE" # if cell is safe, then it's safe
    elif (booleanStates[1][query[0]][query[1]] == True):
        deduction = "UNSAFE" # if cell is unsafe, then it's unsafe
    else: 
        deduction = "RISKY" # if we don't know, then it's risky
    
    
    saveOutput(deduction, clausesArray, GROUP_ID, PUZZLE_PATH)