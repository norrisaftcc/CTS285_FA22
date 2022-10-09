# procman.py
"""
    Procman is a procedurally programmed version of Dataman, in Python.
    
    It is intended to show when using object-oriented programming is useful,
    and why.
"""
    
    
def main():
    print("Welcome to Procman!")
    ui_init()   # Initialize the user interface
    # loop until user is finished
    # menu() returns True if you should go again, False if finished
    keepGoing = True
    while keepGoing == True:
        keepGoing = ui_main_menu()
    print("Exiting program.")


def ui_init():
    print("Initializing user interface...")
    # initialize the user interface
    
def ui_main_menu():
    print("Displaying menu...")
    # display the menu
    # get the user's choice
    # return True if you should go again, False if finished
    ui_show_main_menu()
    choice = int(input("Selection: "))
    if choice == 1:
        ui_do_answer_checker()
    elif choice == 2:
        ui_do_memory_bank()
    elif choice == 0:
        print("Exiting program.")
        return False
    # unless user asked to exit, return True
    return True
    
def ui_show_main_menu():

    print ("Dataman Main Menu")
    print ("1. Answer Checker")
    print ("2. Memory Bank")
    print ("0. Exit")

def ui_do_answer_checker():
    print("Answer Checker")
    # do the answer checker
    
def ui_do_memory_bank():
    print("Memory Bank")
    # do the memory bank


    
# launch the program.
if __name__ == "__main__":
    main()