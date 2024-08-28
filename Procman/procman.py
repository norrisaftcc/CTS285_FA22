# procman.py
"""
    Procman is a procedurally programmed version of Dataman, in Python.
    
    It is intended to show when using object-oriented programming is useful,
    and why. Presumably it will get to the point that breaking it into
    modules, and then objects, will make sense...

    Fall 2024: Made some minor changes to the comments. (two, exactly.)
"""
# Memory Bank for this version is a list of problems kept in global memory
# A problem is a list of 3 items: [operand1, operator, operand2, equals, userAnswer]]
# Note that storing the "equals" sign is redundant, but it makes the problem easier to read


# problems are implemented as a list, these constants define the indices
OPERAND1 = 0
OPERATOR = 1
OPERAND2 = 2
EQUALS = 3
USER_ANSWER = 4
# if problem is resized, this will need to be updated
SIZE_OF_PROBLEM = 5


    
def main():
    print("Welcome to Procman!")
    ui_init()   # Initialize the user interface
    # loop until user is finished
    # menu() returns True if you should go again, False if finished
    keepGoing = True
    while keepGoing == True:
        keepGoing = ui_main_menu()
    print("Exiting program.")

#### UI Methods ####
def ui_init():
    print("Initializing user interface...")
    # initialize the user interface
    
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
    problem = ui_parse_problem(problemText)
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
### TODO: Move these to the appropriate module or class ###
# Methods which handle problems (by individual list)
def ui_parse_problem(problemText):
    """chop the provided string into pieces using spaces.
    order follows the structure of problems
    ex: "2 + 2 = 4" -> [2, "+", 2, 4]
    If successful, returns a list in the above format.
    If it fails, it returns just an error string
    """
    # chop the provided string into pieces using spaces
    # order follows the structure of problems
    # ex: "2 + 2 = 4" -> [2, "+", 2, 4]
    problem = problemText.split(" ")
    # debug
    print(problem)
    # convert the strings to numbers
    try:
        problem[OPERAND1] = int(problem[OPERAND1])
        problem[OPERAND2] = int(problem[OPERAND2])
        problem[USER_ANSWER] = int(problem[USER_ANSWER])
    except ValueError:
        problem = "Invalid problem: non-numeric operand(s)"
    if problem[OPERATOR] not in ["+", "-", "*", "/"]:
        problem = "Invalid problem: invalid operator"
    if problem[EQUALS] != "=":
        problem = "Invalid problem: missing equals sign"
    return problem


def ui_pack_problem(operand1, operator, operand2, equals, userAnswer):
    problem = [operand1, operator, operand2, equals, userAnswer]
    return problem

def ui_show_problem_with_user_answer(problem):
    #space = " "
    #problemString = problem[OPERAND1] + " " problem[OPERATOR], problem[OPERAND2], "=", problem[USER_ANSWER]
    problemString = str(problem[OPERAND1]) + " " + problem[OPERATOR] + " " + str(problem[OPERAND2]) + " = " + str(problem[USER_ANSWER])
    return problemString
   
def ui_show_problem_with_actual_answer(problem):
    actualAnswer = logic_get_actual_answer(problem)
    print(problem[OPERAND1], problem[OPERATOR], problem[OPERAND2], "=", actualAnswer) 
    
"""
# copilot gave me this, ponder it
 def ui_show_memory_bank(memoryBank):
    print("Memory Bank")
    # display the memory bank
    for problem in memoryBank:
        ui_show_problem(problem)
"""

### end ui methods ###

#### Logic Methods ####  
def logic_get_actual_answer(problem):
    """Provides the actual answer to the problem, if available.

    Args:
        problem (list): [op1, operator, op2, equals, userAnswer]

    Returns:
        int: the answer
        str: if error message
    """
    # return the actual answer to a problem
    # Copilot wrote this 100%. Good Copilot!
    # Consider using a dictionary to map operators to functions (copilot's idea)
    # Consider using exceptions here so we don't
    # have to check every answer for a string error message (my idea)
    if len(problem) != SIZE_OF_PROBLEM: # oops, I was using a number and it was wrong
        return "Invalid problem: wrong number of items"
    if problem[OPERATOR] == "+":
        return problem[OPERAND1] + problem[OPERAND2]
    elif problem[OPERATOR] == "-":
        return problem[OPERAND1] - problem[OPERAND2]
    elif problem[OPERATOR] == "*":
        return problem[OPERAND1] * problem[OPERAND2]
    elif problem[OPERAND2] == 0:
        return "undefined" # can't divide by zero
    elif problem[OPERATOR] == "/": # integer division, we need to include remainders i guess
        return problem[OPERAND1] // problem[OPERAND2]
    else:
        return "invalid operator"

def logic_check_problem(problem, userAnswer):
    # return True if userAnswer is correct, False otherwise
    # check if the answer is correct
    # This is redundant, probably, and there could be some
    # confusion between actual answer and user answer.
    # we do not store the actual answer in the problem.
    actualAnswer = logic_get_actual_answer(problem)
    print("DEBUG")
    print("userAnswer:", userAnswer)
    print("actualAnswer:", actualAnswer)
    if userAnswer == actualAnswer:
        return True
    else:
        return False

### end logic methods ###    
# launch the program.
if __name__ == "__main__":
    main()

