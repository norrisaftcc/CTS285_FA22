#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:48:43 2022

@author: norrisa
Dataman_logic -- business logic for project
"""
#import dataman_data as myData 

class Dataman_Logic:
    def __init__(self):
        #self.data = myData.Datman_Data()
        pass
    
    def checkProblem(self, problem, userAnswer):
        realAnswer = problem.solve()
        isCorrect = (realAnswer == userAnswer)
        return isCorrect
    
    
class Dataman_Data:
    def __init__(self):
        self.problems = [] # list of problems
        self.problemIndex = 0 # index of current problem
        
    def addProblem(self, problem):
        """ add a problem to the list of problems
        input: problem
        output: none
        """
        self.problems.append(problem)
        
    def getNextProblem(self):
        """ get the next problem in the list of problems
        input: none
        output: problem
        """
        
        if len(self.problems) == 0:
            return None
        problem = self.problems[self.problemIndex]
        self.problemIndex += 1
        if self.problemIndex >= len(self.problems):
            self.problemIndex = 0
        return problem
    
    def getAllProblems(self): 
        """ get all problems from the Memory Bank
        input: none
        output: list of Problem objects
        """
        return self.problems
        
class Problem:
    def __init__(self, first, operator, second, answer):
        self.first = first
        self.operator = operator
        self.second = second
        self.answer = answer
        
    def __str__(self):
        """ print the problem in human readable form 
        >>> myProblem = Problem(2, "+", 2, 4)
        >>> str(myProblem)
        '2 + 2 = 4'
        >>> anotherProb = Problem(5, "*", 10, 50)
        >>> str(anotherProb)
        '5 * 10 = 50'
        """
        problemString = str(self.first) + " " + self.operator + " " + \
            str(self.second) + " = " + str(self.answer)
        return problemString
    
    def showProblemToSolve(self):
        """ returns a string with the problem in human readable form, 
        but with the answer replaced with a ?   
        input: none
        output: string
        """ 
        problemString = str(self.first) + " " + self.operator + " " + \
            str(self.second) + " = " "?"
        return problemString
        
    def solve(self):
        """ find the actual answer
        input: none
        output: the answer as int (division not yet implemented)
        >>> myProblem = Problem(2, "+", 2, 4)
        >>> myProblem.solve()
        4
        >>> anotherProb = Problem(5, "*", 10, 50)
        >>> anotherProb.solve()
        50
        
        """
        # parse the problem and do the math manually
        first = self.first
        operator = self.operator
        second = self.second
        if (operator == "+"):
            answer = first + second
        if (operator == "*"):
            answer = first * second
        if (operator == "-"):
            answer = first - second
        if (operator == "/"):
            # TODO: handle remainders
            answer = first // second
            
        return answer
    
    
    
    
if __name__ == "__main__":
    """ Test scaffold """
    import doctest
    doctest.testmod()
    