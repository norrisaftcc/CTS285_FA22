# procman_logic
# goal is to handle anything that is not UI related

# Data storage for a math problem
# Memory Bank for this version is a list of problems kept in global memory

memory_bank = []

# A problem is a list of 3 items: [operand1, operator, operand2, equals, userAnswer]]
# Note that storing the "equals" sign is redundant, but it makes the problem easier to read

# problems are implemented as a list, these constants define the indices
OPERAND1 = 0
OPERATOR = 1
OPERAND2 = 2
EQUALS = 3
USER_ANSWER = 4
# if problem is resized, this will need to be updated. (don't use magic numbers)
SIZE_OF_PROBLEM = 5
# End Data Related Structures and constants


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

### Checking problems for correctness should be in the logic module ###
### RELABEL these methods as they no longer deal with UI ###
### TODO: Move these to the appropriate module or class ###
# Methods which handle problems (by individual list)
def logic_parse_problem(problemText):
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


def logic_pack_problem(operand1, operator, operand2, equals, userAnswer):
    problem = [operand1, operator, operand2, equals, userAnswer]
    return problem

def logic_show_problem_with_user_answer(problem):
    #space = " "
    #problemString = problem[OPERAND1] + " " problem[OPERATOR], problem[OPERAND2], "=", problem[USER_ANSWER]
    problemString = str(problem[OPERAND1]) + " " + problem[OPERATOR] + " " + str(problem[OPERAND2]) + " = " + str(problem[USER_ANSWER])
    return problemString
   
def logic_show_problem_with_actual_answer(problem):
    actualAnswer = logic_get_actual_answer(problem)
    print(problem[OPERAND1], problem[OPERATOR], problem[OPERAND2], "=", actualAnswer) 
    

### end logic methods ###   
