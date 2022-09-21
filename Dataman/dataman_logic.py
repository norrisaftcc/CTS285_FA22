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
    
    def checkProblem(problem, userAnswer):
        realAnswer = problem.solve()
        isCorrect = (realAnswer == userAnswer)
        return isCorrect
    
    
class Dataman_Data:
    def __init__(self):
        self.problems = None # list of problems
        
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
        
    def solve(self):
        """ find the actual answer 
        >>> myProblem = Problem(2, "+", 2, 4)
        >>> myProblem.solve()
        4
        >>> anotherProb = Problem(5, "*", 10, 50)
        >>> anotherProb.solve()
        50
        
        """
        # TODO -- it only works if the answer is 4 now
        return 4
    
    
    
    
if __name__ == "__main__":
    """ Test scaffold """
    import doctest
    doctest.testmod()
    