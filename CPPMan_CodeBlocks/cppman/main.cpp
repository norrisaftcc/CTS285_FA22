/*
CppMan for Code::Blocks
(still working on VSCode with C++, this is a stopgap)

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

// Method declarations
int start_dataman_program();


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
}

int start_dataman_program() {


}


