import math
import numpy as np
import os
import random 
import sys
import re

def fileImport(fileName): # brings file into program as str numpy array
    
    puzzleStart = np.genfromtxt(fileName, dtype=str, encoding=None, delimiter='\n')
    return puzzleStart

def createMap(fileInfo): # initializes a properly sized array representing known values of system
    puzzleSize = fileInfo[0][6:]
    puzzleDimensions = puzzleSize.split('x')
    puzzleRC = int(puzzleDimensions[0])
    # this boolean states array constains booleans variables on the following data: 
    # 0) safe, 1) unsafe, 2) breeze, 3) stench
    booleanStatesZeros = np.zeros((4, puzzleRC, puzzleRC), dtype=int);
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
        booleanStates[0][row][col] = True # cells 'visited' are always safe 
        # (part of knowledge base)
        
    
    # print(booleanStates)
    
    return booleanStates

def retrieveOtherInfo(fileInfo):
    
    queryCellText = fileInfo[-2]
    arrows = int((fileInfo[1].split(' '))[1]) # 2nd line, all characters after ' ' converted     # to an integer
    
    # split by (, <commas>, ) 
    queryLineInfo = re.split(r"[(,)]\s*", queryCellText) 
    
    
    query = [int(queryLineInfo[-3]), int(queryLineInfo[-2])]
    query_arrows = (query, arrows)
    return query_arrows
    

def saveOutput(deduction, clauses_array, GROUP_ID, PUZZLE_PATH): # saves solved puzzle to output file
    fileName = GROUP_ID + "_" + PUZZLE_PATH[-11:-4] + ".txt"
    writeString = ""
    for clause in clauses_array:
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
    query = query_arrows[0]
    arrows = query_arrows[1]
    clauses_array = [] # placeholder
    
    
    # output stuff
    if (booleanStates[0][query[0]][query[1]] == True): 
        deduction = "SAFE" # if cell is safe, then it's safe
    elif (booleanStates[1][query[0]][query[1]] == True):
        deduction = "UNSAFE" # if cell is unsafe, then it's unsafe
    else: 
        deduction = "RISKY" # if we don't know, then it's risky
    
    
    saveOutput(deduction, clauses_array, GROUP_ID, PUZZLE_PATH)