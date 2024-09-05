# Ghidra initializer 

This python script automates the process of running ghidra, creating a project and importing the binary file.


# Usage 

``` python ghidra_autorun.py <binary_name> ```
First time running the script it will prompt you for the location of ghidra in your machine , example : /usr/share/ghidra
It will then memorize this location in ~/.ghidra_config.json for further usages 

It will create a folder with the binary name in the current directory to store the ghidra files 



