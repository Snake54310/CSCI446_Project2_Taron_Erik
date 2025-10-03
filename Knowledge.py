import math
import numpy as np
import os
import random 
import sys
import re
import copy as cp

class Knowledge:
    def __init__(self, booleanStates, holesWompuses):
        self.booleanStates = cp.copy(booleanStates); #  this boolean states array contains 
        # booleans variables on the following data: 
        # 0) safe, 1) unsafe, 2) breeze, 3) stench, 4) given
        
        
        self.holesWompuses = cp.copy(holesWompuses); #     # creates an initial array of:
        # 0) there could be a hole 1) there could be a wompus
        # 2) there is a hole 3) there is a wompus

        arraysShape = booleanStates.shape
        
        self.rows = arraysShape[1] # number of rows in map
        self.columns = arraysShape[2] # number of columns in map
        
        self.clausesArray = [] # record created clauses (strings)
        
        self.clausesQueue = [] # clauses to be unified/resolved/evaluated
        
        # EXPLANATION OF VARIABLES AND CONSTANTS:
        # (A state refers to any boolean value)
        # 0. the 'given' state is always a constant
        # 1. All states associated with given cells are constants
        # 2. Safe, Unsafe, Breeze, Stench, Given are all constant if set True
        # and variables if false AND not given
        # 3. There could be a hole, there could be a wompus are both variables 
        # unless set False, at which point they are constants
        # 4. There is a wompus, there is a hole are both variables 
        # unless set True, at which point they are constants
        # 5. raw True and False values are constants
        # 6. anything containing a to-be-simplied function is a variable
        
        # NOTE: WE SHOULD CONSIDER TRACKING CONSTANTS AND VARIABLES IN THE PROGRAM
        # OR: WE CAN DEFINE METHODS TO DETERMINE "VARIABLE" OR "CONSTANT" FROM THESE
        # RULES FOR ANY VALUE IN ANY CELL (likely easier, actually)
        
        # IF NO MORE VARIABLES CAN BE SIMPLIFIED, RESOLVED, OR UNIFIED THEN WE 
        # ARE DONE. WE EXTRACT WHAT WE CAN FROM COMPLETED LOGIC
        
        
        # OUTPUT METHODS -------------------------------------------------
    def getClausesArray(self):
        return self.self.clausesArray
        # END OUTPUT METHODS -------------------------------------------------
    
        # GET-DATA METHODS -------------------------------------------------
    def hasStench(self, cell):
        row = cell[0]
        column = cell[1]
        hasStench = False
        if (self.booleanStates[3][row][column] == True):
            hasStench = True
        return hasStench
    
    
    def hasBreeze(self, cell):
        row = cell[0]
        column = cell[1]
        hasBreeze = False
        if (self.booleanStates[2][row][column] == True):
            hasBreeze = True
        return hasBreeze
    
    
    def hasNeighboringStench(self, cell):
        row = cell[0]
        column = cell[1]
        neighboringStench = False
        
        if (row + 1 < self.rows):
            if (hasStench([row+1, column])):
                neighboringStench = True
                
        if (row - 1 >= 0):
            if (hasStench([row-1, column])):
                neighboringStench = True
                
        if (column + 1 < self.columns):
            if (hasStench([row,column + 1])):
                neighboringStench = True
                
        if (column - 1 >= 0):
            if (hasStench([row, column - 1])):
                neighboringStench = True       
        
        return neighboringStench
    
    
    def hasNeighboringBreeze(self, cell):
        row = cell[0]
        column = cell[1]
        neighboringBreeze = False
        
        if (row + 1 < self.rows):
            if (self.hasBreeze([row+1, column])):
                neighboringBreeze = True
                
        if (row - 1 >= 0):
            if (self.hasBreeze([row-1, column])):
                neighboringBreeze = True
                
        if (column + 1 < self.columns):
            if (self.hasBreeze([row, column + 1])):
                neighboringBreeze = True
                
        if (column - 1 >= 0):
            if (self.hasBreeze([row, column - 1])):
                neighboringBreeze = True       
        
        return neighboringBreeze
               
    def isGiven(self, cell):
        row = cell[0]
        column = cell[1]
        isGiven = False
        if (self.booleanStates[4][row][column] == True):
            isGiven = True
        return isGiven
    
    def isSafe(self, cell):
        row = cell[0]
        column = cell[1]
        isSafe = False
        if (self.booleanStates[0][row][column] == True):
            isSafe = True
        return isSafe
    
    def isUnsafe(self, cell):
        row = cell[0]
        column = cell[1]
        isUnsafe = False
        if (self.booleanStates[1][row][column] == True):
            isUnsafe = True
        return isUnsafe
    
    def couldWompus(self, cell):
        row = cell[0]
        column = cell[1]
        couldWompus = False
        if (self.holesWompuses[1][row][column] == True):
            couldWompus = True
        return couldWompus
        
    def couldHole(self, cell):
        row = cell[0]
        column = cell[1]
        couldHole = False
        if (self.holesWompuses[0][row][column] == True):
            couldHole = True
        return couldHole
    
    def isWompus(self, cell):
        row = cell[0]
        column = cell[1]
        isWompus = False
        if (self.holesWompuses[3][row][column] == True):
            isWompus = True
        return isWompus
        
    def isHole(self, cell):
        row = cell[0]
        column = cell[1]
        isHole = False
        if (self.holesWompuses[2][row][column] == True):
            isHole = True
        return isHole
    
    
    
        # END GET-DATA METHODS -------------------------------------------------
    
        # BOOLEAN OPERATOR METHODS -------------------------------------------------
        
        # python defines and, or, and not operators.
        # If all variables (one for not and two for and/or) operated on by an operator
        # are constants, simplify to boolean state
        
        # TUPLES LOOK LIKE THIS: (OPERATOR/FUNCTION, VAR_A, VAR_B) (if var B exists)
    
    def impliesMethod(self, X, Y):
        # store the expression: (not x) or y
        implies = ("OR", ("NOT", X), Y)
        return implies
    
    
    
    
        # END BOOLEAN OPERATOR METHODS -------------------------------------------------
    
    
        # MAP COMMAND OPERATIONS -------------------------------------------------
    
    def noMoreWompuses(self): # to be run if marked wompuses is equal to marked holes
        for row in self.rows:
            for column in self.columns: # for every cell
                if (not self.holesWompuses[3][row][column]): # if there is not a wompus
                    # there could not be a wompus
                    self.holesWompuses[1][row][column] = False 
        return
    
    
    
    
    
    
    
    
        # END MAP COMMAND OPERATIONS -------------------------------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
    