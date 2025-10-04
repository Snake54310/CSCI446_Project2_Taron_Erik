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
    holesWompusesZeros = np.zeros(arraysShape, dtype=int)
    holesWompuses = holesWompusesZeros.astype(bool)
    
    ''' ALL OF THESE OPERATIONS MUST TAKE PLACE IN FOL
    for row in range(arraysShape[1]):
        for col in range(arraysShape[2]):
            if (booleanStates[0][row][col] != True):
                # if the cell is not known to be safe, there could be 
                # a hole or a wompus (knowledge base)
                holesWompuses[0][row][col] = True
                holesWompuses[1][row][col] = True
    
    
    for row in range(arraysShape[1]):
        for col in range(arraysShape[2]):
            if (booleanStates[0][row][col] == True): # If cell is safe and visited
                # (all known-safe cells have been visited at this point in the code)
                # check whether there is a stench or a breeze: 
                # if there is no breeze, there is no hole in adjacent cells
                # (knowledge base)
                if (booleanStates[2][row][col] != True):
                    if (row + 1 < arraysShape[1]): # if row 'below' exists in map
                        holesWompuses[0][row + 1][col] = False
                    if (row - 1 > -1): # if row 'above' exists in map
                        holesWompuses[0][row - 1][col] = False
                    if (col + 1 < arraysShape[1]): # if column 'below' exists in map
                        holesWompuses[0][row][col + 1] = False
                    if (col - 1 > -1): # if column 'above' exists in map
                        holesWompuses[0][row][col - 1] = False
                
                # if there is no stench, there is no wompus in adjacent cells
                # (knowledge base)
                if (booleanStates[3][row][col] != True):
                    if (row + 1 < arraysShape[1]): # if row 'below' exists in map
                        holesWompuses[1][row + 1][col] = False
                    if (row - 1 > -1): # if row 'above' exists in map
                        holesWompuses[1][row - 1][col] = False
                    if (col + 1 < arraysShape[1]): # if column 'below' exists in map
                        holesWompuses[1][row][col + 1] = False
                    if (col - 1 > -1): # if column 'above' exists in map
                        holesWompuses[1][row][col - 1] = False
    # the next step (logically) would be to say that "if there is 
    # no chance of wompus and there is no chance of hole, then the cell is safe
    # Likely part of knowledge base, but should be implemented in recursive FOL cycle
    '''
                
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
    #print(booleanStates) # working correctly here
    #print(holesWompuses) # working correctly here
    
    # NOTE: we still need to extract relevant
    # tuple-formed literals from these initial visualization-style data structures
    # BUT THIS SHOULD BE DONE INSIDE THE RECURSION
    
    # General structure: visual map => literals => logic pipeline => visual map => literals => ...
    # NOTE: we will likely want an object to store our information in 
    # so that it can be better tracked inside recursion
    
    # For FOL recursion, base-cases (to return up tree) will be:
    # 1. if the query cell safe index is set TRUE
    # 2. if the query cell unsafe index is set TRUE
    # 3. if there is nowhere else to go logically via FOL
    
    
    # output stuff
    if (booleanStates[0][query[0]][query[1]] == True): 
        deduction = "SAFE" # if cell is safe, then it's safe
    elif (booleanStates[1][query[0]][query[1]] == True):
        deduction = "UNSAFE" # if cell is unsafe, then it's unsafe
    else: 
        deduction = "RISKY" # if we don't know, then it's risky
    
    
    saveOutput(deduction, clausesArray, GROUP_ID, PUZZLE_PATH)