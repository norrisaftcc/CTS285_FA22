#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:48:43 2022

@author: norrisa
Dataman_data -- data for the project
"""


class Dataman_Data:
    
    def __init__(self):
       self.problems = None # list of Problem objects
       
    def getAllProblems(self): 
        """ get all problems from the Memory Bank
        input: none
        output: list of Problem objects
        """
        return self.problems

    
    

    