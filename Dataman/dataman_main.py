# -*- coding: utf-8 -*-
"""
Dataman project - entry point (main)

"""
import dataman_ui as ui
import dataman_logic as logic
import dataman_data as data 

def main():
    """ initialize program """
    
    gui = ui.Dataman_UI()
    # loop until user is finished
    # menu() returns True if you should go again, False if finished
    keepGoing = True
    while keepGoing == True:
        keepGoing = gui.menu()
    print("Exiting program.")
    
      
# start program
if __name__ == "__main__":
    main()