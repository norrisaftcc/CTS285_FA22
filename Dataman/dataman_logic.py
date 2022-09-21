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
        """ print the problem in human readable form """
        problemString = str(self.first) + " " + self.operator + " " + \
            str(self.second) + " = " + self.answer
        return problemString
        
    def solve(self):
        """ find the actual answer """
        # TODO -- it only works if the answer is 4 now
        return 4