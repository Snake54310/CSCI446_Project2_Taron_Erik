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
        
        self.runCount = 0
        
        
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
            if (self.hasStench([row+1, column])):
                neighboringStench = True
                
        if (row - 1 >= 0):
            if (self.hasStench([row-1, column])):
                neighboringStench = True
                
        if (column + 1 < self.columns):
            if (self.hasStench([row,column + 1])):
                neighboringStench = True
                
        if (column - 1 >= 0):
            if (self.hasStench([row, column - 1])):
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
        if type(element) != tuple or len(element) != 2:  # if shape not consistent with graph calls
            return False
        code = element[0]
        cell = element[1]
        
        if code == 'HS':  # Constant if True
            return self.hasStench(cell)
        elif code == 'HB':  # Constant if True
            return self.hasBreeze(cell)
        elif code == 'IS':  # Constant if True
            return self.isSafe(cell)
        elif code == 'IU':  # Constant if True
            return self.isUnsafe(cell)
        elif code == 'CW':  # Constant if False (could not)
            return not self.couldWompus(cell)
        elif code == 'CH':  # Constant if False
            return not self.couldHole(cell)
        elif code == 'IW':  # Constant if True
            return self.isWompus(cell)
        elif code == 'IH':  # Constant if True
            return self.isHole(cell)
        elif code == 'IG':  # Always constant
            return True
        
        return False
    
    def evaluateCellCall(self, element):
        code = element[0]
        cell = element[1]
        if code == 'HS':  
            return self.hasStench(cell)
        elif code == 'HB':  
            return self.hasBreeze(cell)
        elif code == 'IS': 
            return self.isSafe(cell)
        elif code == 'IU': 
            return self.isUnsafe(cell)
        elif code == 'CW': 
            return self.couldWompus(cell)
        elif code == 'CH': 
            return self.couldHole(cell)
        elif code == 'IW': 
            return self.isWompus(cell)
        elif code == 'IH': 
            return self.isHole(cell)
        elif code == 'IG': 
            return self.isGiven(cell)
        
        return -1 # if invalid, return failure
        
    
    
    
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
    
    def moveCancelNots(self, statementTuple, previousPredicate):
        newStatementTuple = statementTuple
        predicate = statementTuple[0]
        notWasMoved = False
        
        if (previousPredicate == 'NOT'):
            if (predicate == 'AND'):
                new1 = ('NOT', statementTuple[1])
                new2 = ('NOT', statementTuple[2])
                newStatementTuple = ('OR', new1, new2)
                notWasMoved = True
            elif (predicate == 'OR'):
                new1 = ('NOT', statementTuple[1])
                new2 = ('NOT', statementTuple[2])
                newStatementTuple = ('AND', new1, new2)
                notWasMoved = True
            elif (predicate == 'NOT'):
                new1 = statementTuple[1]
                newStatementTuple = new1
                notWasMoved = True
                
        newPredicate = newStatementTuple[0]
        finalStatementTuple = ()
        
        for element in newStatementTuple:
            nottedElement = ()
            if (type(element) == tuple):
                nottedResults = self.moveCancelNots(element, newPredicate)
                nottedElement = nottedResults[0]
                removeNot = nottedResults[1]
                if (removeNot):
                    nottedElement = nottedElement[1] 
                
            else:
                nottedElement = element
            
            finalStatementTuple += (nottedElement,)
        
        resultsTuple = (finalStatementTuple, notWasMoved)
            
        return resultsTuple
         
        
    
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
        for row in range(self.rows):
            for column in range(self.columns): # for every cell
                if (not self.holesWompuses[3][row][column]): # if there is not a wompus
                    # there could not be a wompus
                    self.holesWompuses[1][row][column] = False 
        return
    
    def setCell(self, element):
        code = element[0]
        cell = element[1]
        row = cell[0]
        column = cell[1]
        if code == 'HS':  
            self.booleanStates[3][row][column] = True
        elif code == 'HB':  
            self.booleanStates[2][row][column] = True
        elif code == 'IS':
            self.booleanStates[0][row][column] = True
        elif code == 'IU': 
            self.booleanStates[1][row][column] = True
        elif code == 'CW': 
            self.holesWompuses[1][row][column] = False
        elif code == 'CH': 
            self.holesWompuses[0][row][column] = False
        elif code == 'IW': 
            self.holesWompuses[3][row][column] = True
        elif code == 'IH': 
            self.holesWompuses[2][row][column] = True
            
        return
        
    
    
    
    
    
        # END MAP COMMAND OPERATIONS -------------------------------------------------
    
    
        # KNOWLEDGE BASE OPERATIONS METHODS -------------------------------------------------
    def initializeKnowledge(self): # create initial tuple containing all of knowledge base
        for row in range(self.rows):
            for column in range(self.columns):
                cell = [row, column]
                self.clausesQueue += self.noStenchNeighbor(cell)
                self.clausesQueue += self.noBreezeNeighbor(cell)
                # self.clausesQueue += ...
                # ...
        if (self.test == 0):
            self.clausesQueue += [self.cellNotUnsafe(self.query)]
        if (self.test == 1):
            self.clausesQueue += [self.cellNotSafe(self.query)]
            
        CNFIndex = 0
        clausesCount = len(self.clausesQueue)
        for i in self.clausesQueue:
            self.clausesArray.append(str(i)) # add every clause to clauses Queue records string
            newResult = self.moveCancelNots(i, 'AND') 
            newClause = newResult[0]
            
            if (CNFIndex != 0 and CNFIndex != clausesCount - 1):
                self.clausesQueue = (self.clausesQueue[:CNFIndex] + [newClause] + self.clausesQueue[CNFIndex + 1:])

            elif (CNFIndex == 0):
                self.clausesQueue = [newClause] + self.clausesQueue[1:]
                
            else:
                self.clausesQueue = self.clausesQueue[:-1] + [newClause]
            
            CNFIndex += 1
        for i in self.clausesQueue:
            self.clausesArray.append(str(i)) # add every clause to clauses Queue records 
        
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
        
        addKnowledge = []
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
    def substituteRecursion(self, element, Theta):
        if not Theta:
            return element # if substitutions empty, return as-is
        elementType = type(element)
        if elementType != tuple:
            # Check theta to see if we have match
            for listing in Theta:
                to_replace = listing[0]
                replace_with = listing[1]
                if element == to_replace:
                    return replace_with
            return element
        # if type is tuple, check sub-elements
        newElements = []
        for subElement in element:
            newElements.append(self.substituteRecursion(subElement, Theta))
        return tuple(new_elements)

    def performSubstitutions(self, Y, Theta):
        if not Theta: # if substitutions empty, return as-is
            return Y
        substitutedClause = self.substituteRecursion(Y, Theta)
        return substitutedClause
    
    def unifyStatements(self):
        performedUnify = False
        clauseQueue = []
        for X in self.clausesQueue: # for every clause
            clauseQueue.append(X)
            
        while clauseQueue:
            X = clauseQueue.pop(0)
            currentClauseIndex = 0
            clausesCount = len(self.clausesQueue) 
            for Y in self.clausesQueue:
                Theta = self.unifyFunction(X, Y)
                
                # perform substitutions
                if (Theta != -1):
                    newY = self.performSubstitutions(Y, Theta)
                    if (currentClauseIndex != 0 and currentClauseIndex != clausesCount - 1):
                        self.clausesQueue = (self.clausesQueue[:currentClauseIndex] + [newY] + self.clausesQueue[currentClauseIndex + 1:])

                    elif (currentClauseIndex == 0):
                        self.clausesQueue = [newY] + self.clausesQueue[1:]
                    else:
                        self.clausesQueue = self.clausesQueue[:-1] + [newY]
                        
                    if (newY != Y):
                        performedUnify = True
                        clauseQueue.append(newY)
                        clausesArray.append(str(newY))

                currentClauseIndex += 1
            
        return performedUnify
    
    def unifyFunction(self, X, Y, Theta=None): # performed whenever a function is 'anded' or 'or-ed' 
        self.runCount += 1 # number of times this is run -- metric for program scaling
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
        
        if Xtype == bool and Ytype == bool:
            if (X == Y):  
                return Theta # they are equal, valid
            else:
                return -1  # they are unequal, return fail
        elif Xtype == bool and constantY:
            valueY = self.evaluateCellCall(Y)
            if (X == valueY):
                return Theta 
            else:
                return -1
        elif Ytype == bool and constantX:
            valueX = self.evaluateCellCall(X)
            if (valueX == Y):
                return Theta 
            else:
                return -1
        elif Xtype == bool and not constantY:
            return self.unifyVariables(Y, X, Theta)
        
        elif Ytype == bool and not constantX:
            return self.unifyVariables(X, Y, Theta)

        # Other constants
        elif constantX and constantY:
            valueY = self.evaluateCellCall(Y)
            valueX = self.evaluateCellCall(X)
            if valueX == valueY:
                return Theta
            else:
                return -1
        elif constantX:
            # Substitute X value into Y if possible
            valueX = self.evaluateCellCall(X)
            return self.unifyVariables(Y, valueX, Theta)
        elif constantY:
            # Substitute Y value into X if possible
            valueY = self.evaluateCellCall(Y)
            return self.unifyVariables(X, valueY, Theta)
        
        # Tuples (non-constant)
        
        elif Xtype == tuple and Ytype == tuple:
            if len(X) != len(Y):
                return -1
            if len(X) == 2:  # 'NOT' and non-constant cell calls
                theta1 = self.unifyFunction(X[0], Y[0], Theta)
                if theta1 == -1:
                    return -1
                return self.unifyFunction(X[1], Y[1], theta1)  # if predicate identical,
            #run on value
            elif len(X) == 3:  # For 'And' and 'Or' statements
                theta1 = self.unifyFunction(X[0], Y[0], Theta)
                if theta1 == -1:
                    return -1
                theta2 = self.unifyFunction(X[1], Y[1], theta1)
                if theta2 == -1:
                    return -1
                return self.unifyFunction(X[2], Y[2], theta2)
            else:
                return -1

        # for lists 
        elif Xtype == list and Ytype == list:
            if len(X) != len(Y):
                return -1
            theta1 = self.unifyFunction(X[0], Y[0], Theta)
            if theta1 == -1:
                return -1
            return self.unifyFunction(X[1:], Y[1:], theta1)

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
        if X == var:
            return True
        if self.isConstant(X):
            return False
        Xtype = type(X)
        if Xtype in (list, tuple):
            for i in X:
                if self.occurCheck(var, i):
                    return True
        return False
    
    # END UNIFICATION METHODS -------------------------------------------------
    
    
    # RESOLUTION METHODS -------------------------------------------------
    def setForcedValues(self, targetValue): # works because all 2-tuples are 
        # moved to the bottom of tree (not-and, not-or), or removed (not-not)
        # or were at bottom of tree to start (map-cells)
        
        # TARGET VALUE ALWAYS SET TRUE FOR INITIAL CALL!
        
        performedResolve = False
        newClausesQueue = []
        
        for clause in self.clausesQueue:
            targetResult = True # from top of tree, always seek True values
            clauseCat = len(clause) # get type (should never be raw boolean)
            currentClause = clause
            if(clauseCat == 2):
                resultingValue = False
                clausePredicate = clause[0]
                clauseValue = clause[1]
                if (clausePredicate == 'NOT'): # will only ever be one 'NOT' at back-end of logic tree
                    targetValue = False # target value becomes False
                    innerClause = clauseValue[1] # grab inner variable/constant
                    currentClause = innerClause
                
                isConstantValue = isConstant(currentClause)
                
                if(isConstantValue): # if constant
                    resultingValue = evaluateCellCall(currentClause) # check consistency
                    # do not re-append to queue, value is set
                    if (targetValue == resultingValue): # if already consistent
                        pass # do nothing, remove from queue
                    
                    else: # if constant causes contradiction, return failure
                        return -1
                    
                else: # if variable
                    resultingValue = evaluateCellCall(currentClause)
                    if (targetValue == resultingValue): # if already consistent
                        newClausesQueue.append(currentClause) # do nothing besides slight simplification (potentially)
                        # (could still cause contradiction later)
                    else: # if not consistent
                        setCell(currentClause) # value becomes constant
                        newClausesQueue.append(currentClause) # do nothing else besides slight simplification (potentially)
                        # (could still cause contradiction later)
                    
            else:
                newClausesQueue.append(clause) # if different kind of tuple, no forced value exists
                
        self.clausesQueue = newClausesQueue
        return performedResolve
    
        
        
    
    def resolveStatements(self):
        performedResolve = False
        newClausesQueue = []
        for clause in self.clausesQueue:
            newClause = self.resolvePredicate(clause)
            
            if (clause == True):
                # pass # if top-level clause resolved to True, remove from array
                performedResolve = True
            elif (clause == False):
                # maybe print error message
                return -1 # return failure if top-level clause becomes false,
            else:
                newClausesQueue += [newClause]
                if (newClause != clause):
                    performedResolve = True
                
        self.clausesQueue = newClausesQueue
        
        # NOW CHECK FOR FORCED VALUE-SETS!!!
        targetValue = True
        forcedValuesSet = setForcedValues(self, targetValue)
        
        if (forcedValuesSet == -1):
            return -1 # return failure if top-level clause is forced false
        
        if (forcedValuesSet): # If forced values were set, re-call resolveStatements to ensure completed resolution
            resolveStatements(self) # no need to check whether inner resolves were performed, if we're here, we know changes occurred
            performedResolve = True # we know this happened if setForcedValues occurred
        return performedResolve # flag for code to determine whether resolution changed anything
    
    def resolvePredicate(self, statementTuple): # start with this for all predicates, then unify. 
        
        newStatementTuple = ()
        
        for element in statementTuple:
            resolvedElement = ()
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
        
        return result
            
        
        
        
    
    def evaluateFunction(self, statementTuple): # NOTE: FAILURE SIMPLY RESULTS IN A FALSE VALUE INSIDE resolveFunction METHOD
        predicate = statementTuple[0]
        self.runCount += 1 # number of times this is run -- metric for program scaling
        tupleLength = len(statementTuple)
        
        if (predicate == 'NOT'):
            toEvaluate = statementTuple[1]
            
            typeVar = type(toEvaluate)
            
            if (typeVar == bool): # if value is constant, return method Value
                result = self.notMethod(toEvaluate)
                if (result):
                    return True # if the result is correct, return 1
                return False # if the result is incorrect, return -1 (False)
            else: # if value is not constant, try both True and False values (basically, always remains as a variable here, but more code
                # is explanatory
                return statementTuple
                
            
            
        elif (tupleLength == 2):
            
            result = self.evaluatecellCall(statementTuple) # variable if current value of couldWompus in cell is True
            constant = self.isConstant(statementTuple)
            
            if (not constant): # if value is variable
                return statementTuple # if the result is a variable and true, return 0 to keep as variable
            elif (result == True): 
                return True # if the result is a constant ant true
            elif (result == False):
                return False # if result is constant (false), return 1
            return 
        
        elif (predicate == 'AND'): # note: we do not have to deal with evaluating cell-calls because 
            #that is handled at a lower-level of recursion
            value1 = statementTuple[1]
            value2 = statementTuple[2]
            
            type1 = type(value1)
            type2 = type(value2)
            
            totalConstants = 0
            if (type1 == bool):
                totalConstants += 1
            if (type2 == bool):
                totalConstants += 1 
                
            if (totalConstants == 0):
                return statementTuple
            elif (totalConstants == 1):
                attemptResult = andMethod(value1, value2)
                if (attemptResult == True):
                    if (type1 == bool):
                        return value2 # result no longer dependent upon value1
                    if (type2 = bool):
                        return value1 # result no longer dependent upon value2
                return False
            elif (totalConstants == 2):
                Result = andMethod(value1, value2)
                if (result == True):
                    return True
                return False
            return statementTuple
            
        elif (predicate == 'OR'): # note: we do not have to deal with evaluating cell-calls because 
            #that is handled at a lower-level of recursion
            value1 = statementTuple[1]
            value2 = statementTuple[2]
            
            type1 = type(value1)
            type2 = type(value2)
            
            totalConstants = 0
            if (type1 == bool):
                totalConstants += 1
            if (type2 == bool):
                totalConstants += 1 
                
            if (totalConstants == 0):
                return statementTuple
            elif (totalConstants == 1):
                attemptResult = self.orMethod(value1, value2)
                if (attemptResult == False):
                    if (type1 == bool):
                        return value2 # result no longer dependent upon value1
                    if (type2 = bool):
                        return value1 # result no longer dependent upon value2
                    return 0
                return True
            elif (totalConstants == 2):
                Result = self.andMethod(value1, value2)
                if (result == True):
                    return True
                return False
            return statementTuple
            
        else:
            # print error message maybe
            return 0
            
            
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
    