IDEA Drive Command Dynamic Library and Programmer Example Kit

This archive is intended to help users of the IDEADriveCommand.dll dynamic library utilize all the functionality of the library and IDEA Drive. 
The source code folders in this archive were written using Visual Studio 2015 IDE and are intended to show the user how to call functions from the DLL.
One of these API projects was written in Visual Basic .NET 4.5.2 and the other was written in Python version 3.11. 

Considerations:
These programs were intended for use in Windows 7, 8, and 10. The Visual Basic .NET example will require you to install the 4.5.2 .NET framework for the 
executable to run. Most of the functions in the DLL will send direct commands to the IDEA Drive. For these functions, make sure that you have installed
the proper drivers for Windows (if you have installed the AIO IDEA Drive GUI software then these drivers will be installed automatically. Also, make sure that
your hardware connections are correct (minimum of a USB and power connections). Be cautious when testing movement commands and make sure that the command parameters
are set within the specifications for your motor. For data set commands to the library (such as GetCommandName()), you will need to first initialize the database 
by calling the InitializeCommandSet() dll function. 

DLL Calling Conventions:
The DLL functions are exported with __declspec(dllexport) for convenient usage in Windows applications. Some functions will return an integer but most
are void functions. The void return functions will take a string pointer to pre-allocated memory as a parameter and fill the memory space with any return data. 
Most functions will only take up to a limit of 1024B allocation of memory at a time. Functions that can return large strings (such as GetCommandList) can take up to 85MB.

VB.net Code:
This program is quite robust and demonstrates most of the DLL functionality. The left section of the GUI allows the user to select serial ports and 
RS485 IDEA Drive address (for daisy chained drives). The bottom sections of the GUI allows for easily sending commands to the IDEA Drive. Simply select 
the command you want to send and the parameter boxes will automatically appear and have the correct parameter names. The top right section is used to 
send bare string commands to the drive and see the raw data being returned. Use the Send Command button to send the string entered in the command textbox 
below it. Note that the carriage return character and address are automatically added to the command so they do not need to be entered into the GUI. 
When compiling, note that the DLL comes in a x86 and x64 package so you will need to link to the appropriate DLL depending on how you compile the code. 

Python Code:
This program is a simple GUI interface to send commands to the IDEA Drive. You will need to check to make sure you have installed the correct libraries to
run the code (see the import section of the code for specifics). In the GUI, you can set the serial port and drive address, enter a command, and click the 
Execute Command button and it will send the command and return any responses. Address and return characters are not required and are handled in code. You 
will just need to enter the command letter (see Communication Manual) followed by any parameters that may be required (each parameter spaced with comma, 
no spaces). If your drive address is found when searching for addresses, it will display active in the Python terminal.

Labview:
This DLL has been tested to work with Labview 2015 and may work in newer versions. Check whether you are using the 32-bit version or the 64-bit version of 
Labview to import the appropriate DLL. To import the DLL library from the main Labview window, navigate to Tool >> Import >> Shared Library (.DLL)... 
Select "Create VIs for a shared library" and click next. On the next page, select the folder icon and navigate to the appropriate DLL file for the IDEA Drive. 
If the header file is in the same directory, it will be selected automatically. If not, click on the folder icon in the next section to select the 
corresponding header file. Click Next and include any additional paths your project may need then click Next again. If the import was successful, 
you should see a list of functions from the IDEA Drive dynamic library. Uncheck any you will not be using then click Next. On the next window you 
can change the name and path of the new Labview import library. Click Next. If you need error handling, apply that in the next window then click Next. 
Use the next window to configure your functions. Calling Convention should be C. Click Next twice and the library will be generated in Labview. 
Each function will be generated as a VI and can be imported to your project. An example project (for 32-bit version) is included in this archive.

See the IDEADriveDLLCommandList xlsx file (MS Excel spreadsheet). This document contains a list of all DLL API functions, parameter data types, examples, etc.
For IDEA Drive specific command structure and information, see the IDEA Drive Communications Manual for more details.
 
See the EULA.rtf file for our licensing agreement on all the software contained in this repository.
