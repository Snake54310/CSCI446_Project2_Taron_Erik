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
        
        hazardsShape = holesWompuses.shape
        
        self.rows = arraysShape[1] # number of rows in map
        self.columns = arraysShape[2] # number of columns in map
        
        self.clausesArray = [] # record created clauses (strings)
        
        self.clausesQueue = () # clauses to be unified/resolved/evaluated
        
        '''
        holesWompusesConstantsZeros = np.zeros(hazardsShape, dtype=int)
        self.holesWompusesConstants = holesWompusesConstantsZeros.astype(bool) # track all values that are constants
        
        booleanStatesConstantsZeros = np.zeros(arraysShape, dtype=int)
        self.booleanStatesConstants = booleanStatesConstantsZeros.astype(bool) # track all values that are constants
        
        for row in self.rows:
            for c in self.columns:
                self.booleanStatesConstants[4][row][column] = True # given state always constant
        '''
        
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
        # 7. if there are no more wompuses, then all 'there is a wompus' values are constant
        
        # NOTE: WE SHOULD CONSIDER TRACKING CONSTANTS AND VARIABLES IN THE PROGRAM
        # OR: WE CAN DEFINE METHODS TO DETERMINE "VARIABLE" OR "CONSTANT" FROM THESE
        # RULES FOR ANY VALUE IN ANY CELL (likely easier, actually)
        
        # IF NO MORE VARIABLES CAN BE SIMPLIFIED, RESOLVED, OR UNIFIED THEN WE 
        # ARE DONE. WE EXTRACT WHAT WE CAN FROM COMPLETED LOGIC
        
        # !!! DUE TO THE NATURE OF THE VARIABLES AS THEY RELATE TO THE KNOWLEDGE BASE, TRACKING VARIABLE/CONSTANT
        # IS LIKELY COMPLETELY UNNECESSARY!!!
        
        # OUTPUT METHODS -------------------------------------------------
    def getClausesArray(self):
        return self.self.clausesArray
        # END OUTPUT METHODS -------------------------------------------------
    
        # GET-DATA METHODS -------------------------------------------------
    def hasStench(self, cell, Target): # CODE: 'HS'
        row = cell[0]
        column = cell[1]
        hasStench = False
        if (self.booleanStates[3][row][column] == True):
            hasStench = True
        return (hasStench == Target)
    
    
    def hasBreeze(self, cell, Target): # CODE: 'HB'
        row = cell[0]
        column = cell[1]
        hasBreeze = False
        if (self.booleanStates[2][row][column] == True):
            hasBreeze = True
        return (hasBreeze == Target)
    
    
    def hasNeighboringStench(self, cell, Target): # CODE: 'HNS'
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
        
        return (neighboringStench == Target)
    
    
    def hasNeighboringBreeze(self, cell, Target): # CODE: 'HNB'
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
        
        return (neighboringBreeze == Target)
               
    def isGiven(self, cell, Target): # CODE: 'IG'
        row = cell[0]
        column = cell[1]
        isGiven = False
        if (self.booleanStates[4][row][column] == True):
            isGiven = True
        return (isGiven == Target)
    
    def isSafe(self, cell, Target): # CODE: 'IS'
        row = cell[0]
        column = cell[1]
        isSafe = False
        if (self.booleanStates[0][row][column] == True):
            isSafe = True
        return (isSafe == Target)
    
    def isUnsafe(self, cell, Target): # CODE: 'IU'
        row = cell[0]
        column = cell[1]
        isUnsafe = False
        if (self.booleanStates[1][row][column] == True):
            isUnsafe = True
        return (isUnsafe == Target)
    
    def couldWompus(self, cell, Target): # CODE: 'CW'
        row = cell[0]
        column = cell[1]
        couldWompus = False
        if (self.holesWompuses[1][row][column] == True):
            couldWompus = True
        return (couldWompus == Target)
        
    def couldHole(self, cell, Target): # CODE: 'CH'
        row = cell[0]
        column = cell[1]
        couldHole = False
        if (self.holesWompuses[0][row][column] == True):
            couldHole = True
        return (couldHole == Target)
    
    def isWompus(self, cell, Target): # CODE: 'IW'
        row = cell[0]
        column = cell[1]
        isWompus = False
        if (self.holesWompuses[3][row][column] == True):
            isWompus = True
        return (isWompus == Target)
        
    def isHole(self, cell, Target): # CODE: IH
        row = cell[0]
        column = cell[1]
        isHole = False
        if (self.holesWompuses[2][row][column] == True):
            isHole = True
        return (isHole == Target)
    
    def isConstant(self, operation, element): # no code likely needed -- called during unification and resolution
        
        if (element == True or element == False): # if it is a constant True or False
            return True
        
        return False
    
    
    
    
        # END GET-DATA METHODS -------------------------------------------------
    
        # BOOLEAN OPERATOR METHODS -------------------------------------------------
        
        # python defines and, or, and not operators.
        # If all variables (one for not and two for and/or) operated on by an operator
        # are constants, simplify to boolean state
        
        # TUPLES LOOK LIKE THIS: (OPERATOR/FUNCTION, VAR_A, VAR_B, Target) (if var B exists), Target is our defined True/False boolean 
        # result for the operation to hold
        
        
    def impliesMethod(self, X, Y):
        # store the expression: (not x) or y
        implies = ("OR", ("NOT", X), Y, True)
        return implies
    
    def andMethod(self, X, Y, Target):
        return ((X and Y) == Target)
    
    def orMethod(self, X, Y, Target):
        return ((X or Y) == Target)
    
    def notMethod(self, X, Target):
        return (not X == Target)
    
    
        # END BOOLEAN OPERATOR METHODS -------------------------------------------------
    
    
        # MAP COMMAND OPERATIONS -------------------------------------------------
    
        # MAYBE ALL UNNCESSARY
        
        
    def noMoreWompuses(self): # to be run if marked wompuses is equal to marked holes
        for row in self.rows:
            for column in self.columns: # for every cell
                if (not self.holesWompuses[3][row][column]): # if there is not a wompus
                    # there could not be a wompus
                    self.holesWompuses[1][row][column] = False 
        return
    
    def setHasWompus(self, cell):
        row = cell[0]
        column = cell[1]
    
    
    
    
    
    
        # END MAP COMMAND OPERATIONS -------------------------------------------------
    
    
        # KNOWLEDGE BASE OPERATIONS METHODS -------------------------------------------------
    def cellNotUnsafe(self, cell): # if this causes a contradiction, then cell must be Unsafe -- do not append to the clausesQueue within 
        # the same knowledge base as cellNotUnsafe
        addKnowledge = ('IU', cell, False)
        return addKnowledge
        
    def cellNotSafe(self, cell): # if this causes a contradiction, then cell must be Safe -- do not append to the clausesQueue within 
        # the same knowledge base as cellNotUnsafe
        addKnowledge = ('IS', cell, False)
        return addKnowledge
        
    def noStenchNeighbor(self, cell): # if cell is adjacent to a given cell without a stench, then cell does not have wompus
        row = cell[0]
        column = cell[1]
        
        addKnowledge = ()
        if (row + 1 < self.rows):
            addKnowledge1 = addKnowledge + (self.impliesMethod(('AND', ('HS', [row + 1, column], False), ('IG', [row + 1, column], True), True), ('IW', cell, False)))
            addKnowledge = addKnowledge1
            
        if (row - 1 >= 0):
            addKnowledge1 = addKnowledge + (self.impliesMethod(('AND', ('HS', [row - 1, column], False), ('IG', [row - 1, column], True), True), ('IW', cell, False)))
            addKnowledge = addKnowledge1
                
        if (column + 1 < self.columns):
            addKnowledge1 = addKnowledge + (self.impliesMethod(('AND', ('HS', [row, column + 1], False), ('IG', [row, column + 1], True), True), ('IW', cell, False)))
            addKnowledge = addKnowledge1
                
        if (column - 1 >= 0):
            addKnowledge1 = addKnowledge + (self.impliesMethod(('AND', ('HS', [row, column - 1], False), ('IG', [row, column - 1], True), True), ('IW', cell, False)))
            addKnowledge = addKnowledge1     
        
        return addKnowledge
    
    def noBreezeNeighbor(self, cell): # if cell is adjacent to a given cell without a breeze, then cell does not have hole
        row = cell[0]
        column = cell[1]
        
        addKnowledge = ()
        if (row + 1 < self.rows):
            addKnowledge1 = addKnowledge + (self.impliesMethod(('AND', ('HS', [row + 1, column], False), ('IG', [row + 1, column], True), True), ('IH', cell, False)))
            addKnowledge = addKnowledge1
            
        if (row - 1 >= 0):
            addKnowledge1 = addKnowledge + (self.impliesMethod(('AND', ('HS', [row - 1, column], False), ('IG', [row - 1, column], True), True), ('IH', cell, False)))
            addKnowledge = addKnowledge1
                
        if (column + 1 < self.columns):
            addKnowledge1 = addKnowledge + (self.impliesMethod(('AND', ('HS', [row, column + 1], False), ('IG', [row, column + 1], True), True), ('IH', cell, False)))
            addKnowledge = addKnowledge1
                
        if (column - 1 >= 0):
            addKnowledge1 = addKnowledge + (self.impliesMethod(('AND', ('HS', [row, column - 1], False), ('IG', [row, column - 1], True), True), ('IH', cell, False)))
            addKnowledge = addKnowledge1     
        
        return addKnowledge
        
    
    
    # END KNOWLEDGE BASE OPERATIONS METHODS -------------------------------------------------
    
    
    # FUNCTION EVALUATION METHODS -------------------------------------------------
    
    def evaluateFunction(self, statementTuple):
        # CODE CYCLE:
        
        # 0. If there is variable, do not evaluate the function
        # 1. Evaluate Function
            # a. Select function based upon first element of statement tuple
            # b. Run function with correct number of elements, and the target value
            # c. Expect it to return True (result is step 2), otherwise result is step 3
        # 2. If function holds, update map accordingly
        # 3. if function does not hold, break because we have found a contradiction.
        # 4. return result of function (if we make it here, it's the target value) -- Our tuple will be changed to this value
        # NOTE: DUE TO THE 3 RETURN CASES (containsVar, FAILURE, SUCCESS), we will return an integer 0, -1, or 1 instead of a boolean 
    
    
    
    
    
    # END FUNCTION EVALUATION METHODS -------------------------------------------------
    
    
    # UNIFICATION METHODS -------------------------------------------------
    
    
    
    # END UNIFICATION METHODS -------------------------------------------------
    
    
    # RESOLUTION METHODS -------------------------------------------------
    
    
    
    # END RESOLUTION METHODS -------------------------------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
    