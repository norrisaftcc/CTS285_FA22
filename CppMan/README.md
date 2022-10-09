README.md for cppman

CppMan is a from-scratch implementation of DataMan to compare C++ and python
Again, the goal is to start procedural then go OO as it's useful.
(Hopefully this will show why/when OO helps.)

setup/installation
in order to use vscode with c++ i went down the following rabbit hole

https://code.visualstudio.com/docs/cpp/config-mingw
Install MSYS2
- install gcc within it (x64_86 version): [pacman -S mingw-w64-x86_64-gcc]
- update and restart so you can see gcc: [pacman -Suy] then [gcc --version]
- install toolchain: [pacman -S --needed base-devel mingw-w64-x86_64-toolchain]
- add mingw bin to PATH in windows (see above url)
	- for me that was c:\dev\msys2\mingw64\bin (ish)
- relaunch vscode (go to source dir, type "code .")

and... (10/9/22) after that, it can't find the headers.
when i manually add the headers in the mingw directory, it fails with:
the definition of std::initializer_list does not contain the expected constructor

so ... uh let's come back later. Going with codeblocks for now.
(we could just use repl.it also)

