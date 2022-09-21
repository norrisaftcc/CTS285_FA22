#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:48:43 2022

@author: norrisa
Dataman_ui -- user interface for project
"""
import dataman_logic as logic
#import dataman_data as data 

class Dataman_UI:
    def __init__ (self):
        self.logic = logic.Dataman_Logic()
        self.data  = logic.Dataman_Data()
        
    def showMenu(self):
        print ("Dataman Main Menu")
        print ("1. Answer Checker")
        print ("2. Memory Bank")
        print ("0. Exit")
        
    def menu(self):
        self.showMenu()
        choice = int(input("Selection: "))
        if choice == 0: # exit
            return False # UI is finished
        if choice == 1:
            self.doAnswerChecker()
        elif choice == 2:
            self.doMemoryBank()
        else: 
            print("Choice not available.")
        return True # UI is still running
    
    def parseProblem(self, problem):
        """ parse a problem string into a Problem object
        input: string
        output: Problem
        """
        problemElements = problem.split(" ")
        first = int(problemElements[0])
        operator = problemElements[1]
        second = int(problemElements[2])
        #equalSign = problemElements[3] # discard this, it's always "="
        answer = int(problemElements[4])
        problem = logic.Problem(first, operator, second, answer)
        return problem
    
    def doAnswerChecker(self):
        print("Problem format is: 2 + 2 = 4")
        problemTyped = input("Enter math problem: ")
        problem = self.parseProblem(problemTyped)
        print("Your problem was: ", str(problem))
        # check if the answer is correct
        isCorrect = self.logic.checkProblem(problem, problem.answer)
        # tell the user if they were correct
        if isCorrect:
            print("Correct!")
        else:
            print("Incorrect.")
        
   
        
    def doMemoryBank(self):
        """ do the memory bank menu """
        choice = -1
        while choice != 0:  
                
            print("Memory Bank Menu")
            print("1. Solve Next Problem")
            print("2. Add Problems")
            print("0. Exit")
            choice = int(input("Selection: "))
            if choice == 0: # exit
                return False
            elif choice == 1:
                problem = self.data.getNextProblem()
                if problem == None:
                    print("No problems in memory bank.")
                    return False
                print("Next problem: (#", self.data.problemIndex, ")")
                print(problem.showProblemToSolve())
                answer = int(input()) 
                # check if the answer is correct
                isCorrect = self.logic.checkProblem(problem, problem.answer)
                # tell the user if they were correct
                if isCorrect:
                    print("Correct!")
                else:
                    print("Incorrect.")
            elif choice == 2:
                self.doAddProblems()
                
    def doAddProblems(self):
        """ let user create a problem
            add it to the memory bank
        """
        print("Problem format is: 2 + 2 = 4")
        problemTyped = input("Enter math problem: ")
        problem = self.parseProblem(problemTyped)
        self.data.addProblem(problem)
        print("Problem added to memory bank.")
            
        
            