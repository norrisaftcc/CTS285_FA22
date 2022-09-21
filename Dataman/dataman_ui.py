#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:48:43 2022

@author: norrisa
Dataman_ui -- user interface for project
"""
import dataman_logic as logic
import dataman_data as data 

class Dataman_UI:
    def __init__ (self):
        self.logic = logic.Dataman_Logic()
        self.data  = data.Dataman_Data()
        
    def showMenu(self):
        print ("Dataman Main Menu")
        print ("1. Answer Checker")
        print ("< -- Unimplemented options 2,3,etc. -- >")
        print ("0. Exit")
        
    def menu(self):
        self.showMenu()
        choice = int(input("Selection: "))
        if choice == 0: # exit
            return False # UI is finished
        if choice == 1:
            self.doAnswerChecker()
        else: 
            print("Choice not available.")
        return True # UI is still running
    
    def doAnswerChecker(self):
        print("Problem format is: 2 + 2 = 4")
        problemTyped = input("Enter math problem: ")
        problemElements = problemTyped.split(" ")
        #for item in problemElements:
        #    print(item)
        first = problemElements[0]
        operator = problemElements[1]
        second = problemElements[2]
        #equalSign = problemElements[3] # discard this, it's always "="
        answer = problemElements[4]
        problem = logic.Problem(first, operator, second, answer)
        print("Your problem was: ", str(problem))
        
            