import math
import numpy as np
import os
import random 
import sys
import re
import copy as cp

class Knowledge:
    def __init__(self, booleanStates, holesWompuses, arrows, query, test):
        self.booleanStates = cp.copy(booleanStates); #  this boolean states array contains 
        # booleans variables on the following data: 
        # 0) safe, 1) unsafe, 2) breeze, 3) stench, 4) given
        
        self.arrows = arrows # number of potential wompuses
        
        self.query = query # cell we are testing
        
        self.test = test # integer indicating to test not unsafe (0) or not safe (1)
        
        self.holesWompuses = cp.copy(holesWompuses); #     # creates an initial array of:
        # 0) there could be a hole 1) there could be a wompus
        # 2) there is a hole 3) there is a wompus

        arraysShape = booleanStates.shape
        
        hazardsShape = holesWompuses.shape
        
        self.rows = arraysShape[1] # number of rows in map
        self.columns = arraysShape[2] # number of columns in map
        
        self.clausesArray = [] # record created clauses (strings)
        
        self.clausesQueue = [] # clauses to be unified/resolved/evaluated, combined with unification (if possible) or 'and-ing' together
        
        
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
        return self.clausesArray
    
        # END OUTPUT METHODS -------------------------------------------------
    
        # GET-DATA METHODS -------------------------------------------------
    def hasStench(self, cell): # CODE: 'HS' // Constant: if True
        row = cell[0]
        column = cell[1]
        hasStench = False
        if (self.booleanStates[3][row][column] == True):
            hasStench = True
        return hasStench
    
    
    def hasBreeze(self, cell): # CODE: 'HB' // Constant: if True
        row = cell[0]
        column = cell[1]
        hasBreeze = False
        if (self.booleanStates[2][row][column] == True):
            hasBreeze = True
        return hasBreeze
    
    
    def hasNeighboringStench(self, cell): # CODE: 'HNS' // Constant: Always (likely never call this, though)
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
    
    
    def hasNeighboringBreeze(self, cell): # CODE: 'HNB' // Constant: Always (likely never call this, though)
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
               
    def isGiven(self, cell): # CODE: 'IG' // Constant: Always
        row = cell[0]
        column = cell[1]
        isGiven = False
        if (self.booleanStates[4][row][column] == True):
            isGiven = True
        return isGiven
    
    def isSafe(self, cell): # CODE: 'IS' // Constant: if True
        row = cell[0]
        column = cell[1]
        isSafe = False
        if (self.booleanStates[0][row][column] == True):
            isSafe = True
        return isSafe
    
    def isUnsafe(self, cell): # CODE: 'IU' // Constant: if True
        row = cell[0]
        column = cell[1]
        isUnsafe = False
        if (self.booleanStates[1][row][column] == True):
            isUnsafe = True
        return isUnsafe
    
    def couldWompus(self, cell): # CODE: 'CW' // Constant: if False
        row = cell[0]
        column = cell[1]
        couldWompus = False
        if (self.holesWompuses[1][row][column] == True):
            couldWompus = True
        return couldWompus
        
    def couldHole(self, cell): # CODE: 'CH' // Constant: if False
        row = cell[0]
        column = cell[1]
        couldHole = False
        if (self.holesWompuses[0][row][column] == True):
            couldHole = True
        return couldHole
    
    def isWompus(self, cell): # CODE: 'IW' // Constant: if True
        row = cell[0]
        column = cell[1]
        isWompus = False
        if (self.holesWompuses[3][row][column] == True):
            isWompus = True
        return isWompus
        
    def isHole(self, cell): # CODE: 'IH' // Constant: if True
        row = cell[0]
        column = cell[1]
        isHole = False
        if (self.holesWompuses[2][row][column] == True):
            isHole = True
        return isHole
    
    def isConstant(self, element): # no code likely needed -- called during unification and resolution
        
        if (element == True or element == False): # if it is a constant True or False
            return True
        
        return False
    
    
    
    
        # END GET-DATA METHODS -------------------------------------------------
    
        # BOOLEAN OPERATOR METHODS -------------------------------------------------
        
        # python defines and, or, and not operators.
        # If all variables (one for not and two for and/or) operated on by an operator
        # are constants, simplify to boolean state
        
        # TUPLES LOOK LIKE THIS: (OPERATOR/FUNCTION, VAR_A, VAR_B) (if var B exists), Result is result of predicate operating on Variable(s)
        
        
    def impliesMethod(self, X, Y): # NO CODE, APPLIED DIRECTLY UPON KNOWLEDGE INIT
        # store the expression: (not x) or y
        implies = ("OR", ("NOT", X), Y)
        return implies
    
    def andMethod(self, X, Y): # CODE: 'AND' // Constant: if FALSE OR IF X and Y are constants (do not call if both are variables)
        # (if one of X or Y is variable and result is True, treat result as variable)
        if (X == False): # expression must result in False (constant)
            return False
        if (Y == False): # expression must result in False (constant)
            return False
        return True # Expression results in True: (if X and Y are constants, treat as constant). If X or Y is variable, treat as variable
    
    def orMethod(self, X, Y): # CODE: 'OR' // Constant: if TRUE OR IF X and Y are constants (do not call if both are variables)
        # (if one of X or Y is variable and result is false, treat result as variable)
        if (X == True): # expression must result in True (constant)
            return True
        if (Y == True): # expression must result in True (constant)
            return True
        return False # Expression results in False: (if X and Y are constants, treat as constant). If X or Y is variable, treat as variable
    
    def notMethod(self, X): # CODE: 'NOT' // Constant: X is constant (do not call if X is variable)
        return (not X)
    
    
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
        self.holesWompuses[3][row][column] = True
        return
    
    def setHasHole(self, cell):
        row = cell[0]
        column = cell[1]
        self.holesWompuses[2][row][column] = True
        return
        
    def setCellCouldWompus(self, cell):
        row = cell[0]
        column = cell[1]
        self.holesWompuses[1][row][column] = False
        return
    
    def setCellCouldHole(self, cell):
        row = cell[0]
        column = cell[1]
        self.holesWompuses[0][row][column] = False
        return
    
    
    
    
    
        # END MAP COMMAND OPERATIONS -------------------------------------------------
    
    
        # KNOWLEDGE BASE OPERATIONS METHODS -------------------------------------------------
    def initializeKnowledge(self): # create initial tuple containing all of knowledge base
        for row in self.rows:
            for column in self.columns:
                cell = [row, column]
                self.clausesQueue += self.noStenchNeighbor(cell)
                self.clausesQueue += self.noBreezeNeighbor(cell)
                # self.clausesQueue += ...
                # ...
        if (self.test == 0):
            self.clausesQueue += [self.cellNotUnsafe(self.query)]
        if (self.test == 1):
            self.clausesQueue += [self.cellNotSafe(self.query)]
            
        for i in self.clausesQueue:
            self.clausesArray.append(str(i)) # add every clause to clauses Queue records string
        return
        
    def cellNotUnsafe(self, cell): # if this causes a contradiction, then cell must be Unsafe -- do not append to the clausesQueue within 
        # the same knowledge base as cellNotUnsafe
        addKnowledge = ('NOT', ('IU', cell))
        # addKnowledge = ('NOT', ('IU', cell, True), True)
        return addKnowledge
        
    def cellNotSafe(self, cell): # if this causes a contradiction, then cell must be Safe -- do not append to the clausesQueue within 
        # the same knowledge base as cellNotUnsafe
        addKnowledge = ('NOT', ('IS', cell))
        return addKnowledge
        
    def noStenchNeighbor(self, cell): # if cell is adjacent to a given cell without a stench, then cell could not have wompus
        row = cell[0]
        column = cell[1]
        
        addKnowledge = []
        if (row + 1 < self.rows):
            addKnowledge1 = addKnowledge + [self.impliesMethod(('AND', ('NOT', ('HS', [row + 1, column])), ('IG', [row + 1, column])), ('NOT', ('CW', cell)))]
            addKnowledge = addKnowledge1
            
        if (row - 1 >= 0):
            addKnowledge1 = addKnowledge + [self.impliesMethod(('AND', ('NOT', ('HS', [row - 1, column])), ('IG', [row - 1, column])), ('NOT', ('CW', cell)))]
            addKnowledge = addKnowledge1
                
        if (column + 1 < self.columns):
            addKnowledge1 = addKnowledge + [self.impliesMethod(('AND', ('NOT', ('HS', [row, column + 1])), ('IG', [row, column + 1])), ('NOT', ('CW', cell)))]
            addKnowledge = addKnowledge1
                
        if (column - 1 >= 0):
            addKnowledge1 = addKnowledge + [self.impliesMethod(('AND', ('NOT', ('HS', [row, column - 1])), ('IG', [row, column - 1])), ('NOT', ('CW', cell)))]
            addKnowledge = addKnowledge1     
        
        return addKnowledge
    
    def noBreezeNeighbor(self, cell): # if cell is adjacent to a given cell without a breeze, then cell could not have hole
        row = cell[0]
        column = cell[1]
        
        addKnowledge = ()
        if (row + 1 < self.rows):
            addKnowledge1 = addKnowledge + [self.impliesMethod(('AND', ('NOT', ('HB', [row + 1, column])), ('IG', [row + 1, column])), ('NOT', ('CH', cell)))]
            addKnowledge = addKnowledge1
            
        if (row - 1 >= 0):
            addKnowledge1 = addKnowledge + [self.impliesMethod(('AND', ('NOT', ('HB', [row - 1, column])), ('IG', [row - 1, column])), ('NOT', ('CH', cell)))]
            addKnowledge = addKnowledge1
                
        if (column + 1 < self.columns):
            addKnowledge1 = addKnowledge + [self.impliesMethod(('AND', ('NOT', ('HB', [row, column + 1])), ('IG', [row, column + 1])), ('NOT', ('CH', cell)))]
            addKnowledge = addKnowledge1
                
        if (column - 1 >= 0):
            addKnowledge1 = addKnowledge + [self.impliesMethod(('AND', ('NOT', ('HB', [row, column - 1])), ('IG', [row, column - 1])), ('NOT', ('CH', cell)))]
            addKnowledge = addKnowledge1     
        
        return addKnowledge
        
    
    
    # END KNOWLEDGE BASE OPERATIONS METHODS -------------------------------------------------
    
    
    # FUNCTION EVALUATION METHODS ------------------------------------------------- 
    
    
    
    
    
    # END FUNCTION EVALUATION METHODS -------------------------------------------------
    
    
    # UNIFICATION METHODS -------------------------------------------------
    def performSubstitutions(self, Y, Theta):
        
        return 
    
    def unifyStatements(self):
        unified = False
        clauseQueue = []
        for X in self.clausesArray: # for every clause
            clauseQueue += [X]
            
        while clauseQueue:
            X = clauseQueue.pop(0)
            currentClauseIndex = 0
            clausesCount = len(clausesArray) 
            for Y in self.clausesArray:
                replace = self.unifyFunction(X, Y)
                
                # perform substitutions
                newY = self.performSubstitutions(Y, replace)
                if (currentClauseIndex != 0 and currentClauseIndex != clausesCount):
                    self.clausesArray = (self.clausesArray[:Y] + [newY] + self.clausesArray[Y + 1:])
                
                
                if (replace != -1 and replace != []):
                    unified = True
                    clausesQueue += newY
                
                

                currentClauseIndex += 1
            
        return unified
    
    def unifyFunction(self, X, Y, Theta=None): # performed whenever a function is 'anded' or 'or-ed' 
        # with another funciton (our clausesQueue should be considered a massive 'and' string for this purpose)
        if Theta is None:
            Theta = []
        if (Theta == -1):
            return -1
        if (X == Y):
            # Theta.append([X, Y])
            return Theta # items are identical, return substitutions
        
        Xtype = type(X)
        Ytype = type(Y)
        constantX = self.isConstant(X)
        constantY = self.isConstant(Y)
        
        if ((not constantX) and Xtype != tuple and Xtype != str and Xtype != list): # X is variable
            return self.unifyVariables(X, Y, Theta)
        elif ((not constantY) and Ytype != tuple and Ytype != str and Ytype != list):  # Y is variable
            return self.unifyVariables(Y, X, Theta)
        elif (Xtype == tuple and Ytype == tuple):
            if (len(X) == 2 and len(Y) == 2):
                return self.unifyFunction(Y[1], X[1], self.unifyFunction(Y[0], X[0], Theta))
            elif (len(X) == 3 and len(Y) == 3):
                return self.unifyFunction([Y[1], Y[2]], [X[1], X[2]], self.unifyFunction(Y[0], X[0], Theta))
            else:
                return -1
        elif (Xtype == list and Ytype == list):
            return self.unifyFunction(X[1:], Y[1:], self.unifyFunction(X[0], Y[0], Theta))
        
        return -1
        
        
    def unifyVariables(self, var, X, Theta):
        if [var, True] in Theta:
            return self.unifyFunction(True, X, Theta)
        elif [var, False] in Theta:
            return self.unifyFunction(False, X, Theta)
        if [X, True] in Theta:
            return self.unifyFunction(var, True, Theta)
        elif [X, False] in Theta:
            return self.unifyFunction(var, False, Theta)
        elif self.occurCheck(var, X):
            return -1
        
        else:
            Theta.append([var, X])
            return Theta
        
    def occurCheck(self, var, X):
        if (X == var):
            return True
        if (self.isConstant(X)):
            return False
        Xtype = type(X)
        Ytype = type(Y)
        if (Xtype == list or Xtype == tuple):
            for i in X:
                failed = self.occurCheck(var, i)
                if failed:
                    return True
        return False
    
    # END UNIFICATION METHODS -------------------------------------------------
    
    
    # RESOLUTION METHODS -------------------------------------------------
    def resolveStatements(self):
        
    
    def resolvePredicate(self, statementTuple): # start with this for all predicates, then unify. 
        
        newStatementTuple = ()
        
        for element in statementTuple:
            if (type(element) == tuple):
                resolvedElement = self.resolveFunction(element)
            else:
                resolvedElement = element
            
            newStatementTuple += (resolvedElement,)
        
        for element in statementTuple:
            if (type(element) == tuple):
                return newStatementTuple # if, following recursion, tuple still contains unresolved tuples, then return without 
                # attempting further resolution
        
        result = self.evaluateFunction(statementTuple)
        
        if (result == 0):
            return statementTuple # if we cannot resolve a variable, do not resolve 
        
        if (result == 1):
            return True # if result matches target, return True
        
        return False # if result does not match target, return False
            
        
        
        
    
    def evaluateFunction(self, statementTuple): # NOTE: FAILURE SIMPLY RESULTS IN A FALSE VALUE INSIDE resolveFunction METHOD
        predicate = statementTuple[0]
        
        if (predicate == 'NOT'):
            toEvaluate = statementTuple[1]
            if isConstant(toEvaluate): # if value is constant, return method Value
                result = self.notMethod(toEvaluate)
                if (result):
                    return 1 # if the result is correct, return 1
                return -1 # if the result is incorrect, return -1 (False)
            else: # if value is not constant, try both True and False values (basically, always remains as a variable here, but more code
                # is explanatory
                evaluateFalse = False
                evaluateTrue = False
                resultTrue = self.notMethod(True)
                resultFalse = self.notMethod(False)
                if (resultTrue and resultFalse): # technically impossible, but writing for clarity
                    return 0 # result remains a variable, do not simplify
                elif (resultTrue):
                    return 0 # if result is unknown, return 0
                elif (resultFalse):
                    return 0 # if result is unknown, return 0
                return -1 # if the result is incorrect, return -1 (false)
            
        if (predicate == 'CW'):
            toEvaluate = statementTuple[1]
            
            result = self.couldWompus(toEvaluate) # variable if current value of couldWompus in cell is True
            
            if (result == True): # if value is variable
                return 0 # if the result is a variable and true, return 0 to keep as variable
            else (result == False):
                return -1 # if result is constant (false), return 1
            
        if (predicate == 'CH'):
            toEvaluate = statementTuple[1]
            
            result = self.couldHole(toEvaluate) # variable if current value of couldWompus in cell is True
            
            if (result == True): # if value is a variable and is True
                return 0 # if the result is a variable and true, return 0 to keep as variable
            else: # if the value is constant and incorrect, return failure
                return -1
            
        if (predicate == 'IG'):
            toEvaluate = statementTuple[1]
            
            # we know this is a constant because given values are constant:
            result = self.isGiven(toEvaluate)
            if (result):
                return 1 # if the result is correct , return 1
            return -1 # if the result is incorrect, return -1 (failure)
            
            
        # CODE CYCLE:
        
        # 0. If there is variable that cannot be turned into a constant, do not evaluate the function (return 0)
        # 1. Evaluate Function
            # a. Select function based upon first element of statement tuple
            # b. Run function with correct number of elements, and the target value
            # c. Expect it to return True (result is step 2), otherwise result is step 3
        # 2. If function holds, update map accordingly (only needed if variable was forced to become a constant)
        # 3. if function does not hold, return -1. This tuple's value is now resolved to False
        # 4. return 1 -- Our tuple will be resolved to True
        # NOTE: DUE TO THE 3 RETURN CASES (FAILURE, contains_var, SUCCESS), we will return an integer -1, 0, or 1 instead of a boolean
    
    
    
    # END RESOLUTION METHODS -------------------------------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
    