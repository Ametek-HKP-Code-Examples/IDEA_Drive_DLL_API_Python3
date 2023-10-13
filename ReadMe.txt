IDEA Drive Command Dynamic Library and Programmer Example Kit

This archive is intended to help users of the IDEADriveCommand.dll dynamic library to utilize all the functionality of the library and IDEA Drive. 
The source code folders in this archive were written using Visual Studio 2015 IDE and are intended to show the user how to call functions from the DLL.
One of these API projects was written in Visual Basic .NET 4.5.2 and the other was written in Python version 3.11. These programs were intended for 
use in Windows 7,8, and 10. The Python source code may run in some Unix based environments but may need modification to run properly.

VB.net code:
You will need to compile the code for x64 architecture in order for the program to function properly. This program is quite robust and demonstrates most 
of the DLL functionality. The left section of the GUI allows the user to select serial ports and RS485 IDEA Drive address (for daisy chained drives). 
The bottom sections of the GUI allow for easily sending commands to the IDEA Drive. Simply select the command you want to send and the parameter boxes
will automatically appear and have the correct parameter names. The top right section is used to send bare string commands to the drive and see the raw data being 
returned. Use the Send Command button to send the string entered in the command textbox below it. 

Python Code:
This program is a simple GUI interface to send commands to the IDEA Drive. You will need to check to make sure you have installed the correct libraries to
run the code (see the import section of the code for specifics). In the GUI, you can set the serial port and drive address, enter a command, and click the 
Execute Command button and it will send the command and return any responses. Address and return characters are not required and are handled in code. You 
will just need to enter the command letter (see Communication Manual) followed by any parameters that may be required (each parameter spaced with comma, 
no spaces). If your drive address is found when searching for addresses, it will display active in the Python terminal.


Also see the IDEADriveDLLCommandList xlsx file (MS Excel spread sheet). This document contains a list of all DLL API functions, parameter data types, examples, etc.

For more information, please contact the Haydon Kerk Pittman branch of Ametek Inc. 
See the EULA.rtf file for our licensing agreement on all the software contained in this repository.
