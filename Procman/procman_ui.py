# procman_ui
# handles all user interface related tasks
# (and to be honest, a few things that aren't UI related)

# procman_ui requires procman_logic constants in order to work
# but it doesn't need to know about the rest of procman_logic
from procman_logic import *

#### UI Methods ####
def ui_init():
    print("Initializing user interface...")
    # initialize the user interface
    # Later we would do things like clear the problem set, etc. 
    # (or import a problem set from a file)
    
def ui_main_menu():
    print("Displaying menu...")
    # display the menu
    # get the user's choice
    # return True if you should go again, False if finished
    ui_show_main_menu()
    try:
        choice = int(input("Selection: "))
        if choice == 1:
            ui_do_answer_checker()
        elif choice == 2:
            ui_do_memory_bank()
        elif choice == 0:
            print("Exiting program.")
            return False
        else:
            print("Choice not available.")
    except ValueError: # if the user enters a non-numeric value
        print("Invalid choice.")
    # unless user asked to exit, return True
    print() # blank line for readability
    return True
    
def ui_show_main_menu():

    print ("Dataman Main Menu")
    print ("1. Answer Checker")
    print ("2. Memory Bank")
    print ("0. Exit")

def ui_do_answer_checker():
    print("Answer Checker")
    # do the answer checker
    print("Problem format is: 2 + 2 = 4")
    problemText = input("Enter math problem: ")
    problem = logic_parse_problem(problemText)
    # did some debugging here, I wasn't actually returning the problem from ui_show_problem_with_user_answer
    #print(problem, "<-- from ui_parse_problem")
    #print("Your problem was: ", ui_show_problem_with_user_answer(problem))
    #print("Your problem was:", str(ui_show_problem_with_user_answer(problem)))
    if len(problem) != SIZE_OF_PROBLEM:
        print("ERROR: ", problem[0])
        return # Ms. Seidi disapproves of early return statements, it's debatable...
    # check if the answer is correct
    #isCorrect = logic_check_problem(problem, problem[USER_ANSWER])
    # tell the user if they were correct
    userAnswer = problem[USER_ANSWER]
    actualAnswer = logic_get_actual_answer(problem)
    # DEBUG type checking wtf man
    print("Your answer was", userAnswer, type(userAnswer))
    print("The correct answer was", actualAnswer, type(actualAnswer))
    
    if userAnswer == actualAnswer:
        isCorrect = True
    else:
        isCorrect = False
    
    if isCorrect:
        print("Correct!")
    else:
        print("Incorrect.")
    return
    
def ui_do_memory_bank():
    print("Memory Bank")
    # do the memory bank
    print("Not implemented yet.")

### UNORGANIZED METHODS ###

"""
# copilot gave me this, ponder it
 def ui_show_memory_bank(memoryBank):
    print("Memory Bank")
    # display the memory bank
    for problem in memoryBank:
        ui_show_problem(problem)
"""

### end ui methods ###