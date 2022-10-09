/*
Procman in C++ 
Compare with the python version

Again, we're starting with as purely procedural a program as we can.
We'll be adding classes and objects as we go along, as needed.

Portability notes:
I'm trying this in VSCode using mingw64:
https://code.visualstudio.com/docs/cpp/config-mingw for setup.
Should work fine in codeblocks, etc. (test this)

*/

/*
CppMan for VSCode mingw64
(this is using CodeBlocks' mingw installation
Creator: norrisa

CppMan is a C++ version of ProcMan, intended to show the workflow
when moving from a procedural-based program design to one with
objects and classes.

The idea is that as complexity is added, there will be a benefit
to moving to classes.
*/

#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Data types
struct problem {
    int operator1;
    string operand;
    int operator2;
    int answer;
};

// Method declarations
int start_dataman_program();

// UI methods
int ui_main_menu();
int ui_answer_checker();
int ui_memory_bank();

// Data methods
problem read_problem();
string textify_problem(problem p);
bool check_problem(problem p);
// Logic methods




int main()
{
    // testing vector
    vector<string> msg {"Hello", "C++", "World"};

    for (const string& word : msg)
    {
        cout << word << " ";
    }
    cout << endl;
    start_dataman_program();

    return 0;
}
// Start the program, loop until exit
int start_dataman_program() {
    /*
    bool keepGoing = true;
    while (keepGoing) {
        cout << "Starting DataMan program" << endl;
        cout << "Enter a command (menu/quit): " << endl;
        string command;
        cin >> command;
        if (command == "quit") {
            keepGoing = false;
        }
        if (command == "menu") {
            ui_main_menu();
        }
    }*/
    ui_main_menu();
    return 0;
}

// Main menu
int ui_main_menu(){
    /* List main menu in format:
    1. Answer Checker
    2. Memory Bank
    0. Exit
    */
   string command;
    do {
        cout << "Main Menu" << endl;
        cout << "1. Answer Checker" << endl;
        cout << "2. Memory Bank" << endl;
        cout << "0. Exit" << endl;
        cout << "Enter a command: " << endl;
        
        cin >> command;
        if (command == "1") {
            ui_answer_checker();
        }
        else if (command == "2") {
            ui_memory_bank();
        }
        else if (command == "0") {
            cout << "Exiting main menu" << endl << endl;
        }
        else {
            cout << "Invalid command" << endl;
        }
    } while (command != "0");
    return 0;
}

int ui_answer_checker() {
    cout << "Answer Checker" << endl;

    cout << "Problem format: 2 + 2 = 4" << endl;
    problem p = read_problem();
    cout << "You entered: " << textify_problem(p) << endl;

    bool isCorrect = 0;
    isCorrect = check_problem(p);
    //cout << "DEBUG: isCorrect = " << isCorrect << endl;
    if (true == isCorrect) {
        cout << "Correct!" << endl;
    }
    else {
        cout << "Incorrect!" << endl;
    }
    return 0;
}

int ui_memory_bank() {
    cout << "Memory Bank -- Unimplemented" << endl << endl;
    return 0;
}


// Logic methods

// Problem handling methods
problem read_problem() {
    // Note that this craps out with the incorrect amount of input
    // (usual cin problems)
    problem p;
    string equals;
    cout << "Enter a problem (with spaces): " << endl;
     
    cin >> p.operator1 >> p.operand >> p.operator2 >> equals >> p.answer;
    cout << "You entered: " << textify_problem(p) << endl;
    if (equals != "=") {
        cout << "Invalid problem format" << endl;
    }
    return p;
}

string textify_problem(problem p) {
    string text;
    text = to_string(p.operator1) + " " + p.operand + " " + to_string(p.operator2) + " = " + to_string(p.answer);
    return text;
}

bool check_problem(problem p) {
    // returns true if the problem is correct
    int result = 0;
    bool isCorrect = 0;
    if (p.operand == "+") {
        result = p.operator1 + p.operator2;
    }
    else if (p.operand == "-") {
        result = p.operator1 - p.operator2;
    }
    else if (p.operand == "*") {
        result = p.operator1 * p.operator2;
    }
    else if (p.operand == "/") {
        result = p.operator1 / p.operator2;
    }
    else {
        cout << "Invalid operand" << endl;
        return false;
    }
    cout << "DEBUG: result = " << result << " p.answer = " << p.answer << endl;
    if (result == p.answer) {
        isCorrect = 1; // true
    }
    //isCorrect = (result == p.answer);
    //cout << "DEBUG: check_problem: isCorrect = " << isCorrect << endl;

    // i spent 15 minutes figuring out why my answers were wrong
    // i was returning result, not isCorrect (and it was getting munged into a bool)
    return isCorrect;
}
