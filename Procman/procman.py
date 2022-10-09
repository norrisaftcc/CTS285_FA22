# procman.py
"""
    Procman is a procedurally programmed version of Dataman, in Python.
    
    It is intended to show when using object-oriented programming is useful,
    and why. Presumably it will get to the point that breaking it into
    modules, and then objects, will make sense...
    
    v2 - split program into procman, procman_ui, procman_logic
    everything is imported, so this is just to make files smaller
    and organized into what they actually do
"""


# The imports below would import to the ui.* and logic.* "namespaces" (modules)
# I didn't do this yet because you then have to use, for example:
# ui.ui_show_problem_with_user_answer
# rather than ui_show_problem_with_user_answer

#import procman_ui as ui
#import procman_logic as logic

# For now, just import the entire module, which leaves it in the base "namespace"
from procman_ui import *
from procman_logic import *

# Program Start
    
def main():
    print("Welcome to Procman!")
    ui_init()   # Initialize the user interface
    # loop until user is finished
    # menu() returns True if you should go again, False if finished
    keepGoing = True
    while keepGoing == True:
        keepGoing = ui_main_menu()
    print("Exiting program.")

 
# launch the program.
if __name__ == "__main__":
    main()