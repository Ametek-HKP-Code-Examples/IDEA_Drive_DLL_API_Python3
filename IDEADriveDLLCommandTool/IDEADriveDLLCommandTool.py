"""
Name:           IDEADriveDLLCommandTool.py
Author:         Chad F.
Date:           9-22-23
Environment:    Python 3.11
File Type:      Executable (set this file as the startup file)
Version:        2.0
Description:    This program will demostrate the use of the IDEA Drive Dynamic Library in Python 3.11. 
Some libraries may need to be installed (such as tkinter) to run this example code (see imports).
""" 

#Library Imports
import time
import tkinter as tk
from tkinter import ttk
import sys
import glob
from tkinter.ttk import Style
import serial
from tkinter import *
from PIL import ImageTk, Image

#For IDEA Drive object class
import IDEADrvCommander

#Constants
DLL_PATH = ".\\IDEADriveCommandx64.dll"
MAX_NUM_OF_PARAMETERS = 12
MAX_NUM_OF_OUTPUTS = 12
#Globals
ideaDriveAddresses = list()
ideaDriveCommandSet = list()
#GUI setup
root = Tk()
root.geometry('775x500')
root.resizable(False,True)
root.title("IDEA Drive: Python 3 Example")
root.iconbitmap("AmetekALogo.ico")
root.grid()
root.configure()
arrowPNG = ImageTk.PhotoImage(Image.open("Arrow2.png"))

# Sets the IDEA Drive address depending on the input command
def SetIDAddress(command):
    if command[0] == '#':
        addr = command[0:4]
        drive.SetCurrentAddress(addr)
    elif ideaDriveAddresses:
        tmp = addressOptionMenuClicked.get()
        if len(tmp) == 1:
            tmp = "#00" + tmp
        elif len(tmp) == 2:
            tmp = "#0" + tmp
        elif len(tmp) == 3:
            tmp = "#" + tmp
        drive.SetCurrentAddress(tmp)
    else:
        drive.SetCurrentAddress("")

def SendCommand():
    # Set the proper IDEA Drive address
    command = executeEntry.get()
    if not command:
        return
    SetIDAddress(command)
    #Get response and output to GUI.
    response = drive.SendCommand(command)
    time.sleep(0.06)
    responseTextbox.config(state='normal')
    responseTextbox.delete("1.0","end")
    responseTextbox.insert(END, response)
    responseTextbox.config(state='disabled')

#Converts list of parameters to a parameter string to send to the IDEA Drive
def BuildParameterString(cmd):
    out = cmd
    for i in range(0, len(paramList), 1):
        if IDparams[i].get() == "":
            return ""
        out= out + IDparams[i].get() + ","
    if out[len(out)-1] == ",":
        out = out[slice(0,-1)]
    return out
        
def SendDropDownCommand():
    command = commandFinderOptionMenu.get()    
    if not command:
        return
    SetIDAddress(command)
    SendString = ""
    commandLetter = drive.GetCommandLetterFromDescriptive(command)
    if paramList[0] != '':
        SendString = BuildParameterString(commandLetter);
        if SendString == "":
            return
    else:
        SendString = commandLetter
    #Get response and output to GUI.
    response = drive.SendCommand(SendString)
    time.sleep(0.06)
    responseTextbox.config(state='normal')
    responseTextbox.delete("1.0","end")
    responseTextbox.insert(END, response)
    responseTextbox.config(state='disabled')
    response = response[2:-5]
    if command != "Recall Program":
        responseList = response.split(",")
    else: responseList = response

    if outList[0] != '':
        for i in range(0,len(outList),1):
            IDoutputs[i].configure(state = 'normal')
            IDoutputs[i].delete(0,END)
            IDoutputs[i].insert(0,responseList[i])
            IDoutputs[i].configure(state = 'disabled')

#This function will check to see if IDEA Drives are present on the selected serial port and list them in a dropdown menu.
def FindDrives():
    global drive
    if (not drive.IsSerialOpen):
        return
    #Clear options
    addressOptionMenu['menu'].delete(0, 'end')
    #Get all addresses
    addrList = drive.GetAllAvailableAddresses()
    #Clear existing lists
    ideaDriveAddresses.clear()
    #Iterate through addresses and build list
    for i in range(len(addrList)):
        if addrList[i]:
            print("Address " + str(i) + " Active.")
            ideaDriveAddresses.append(i)
    #Update options
    if ideaDriveAddresses:
        addressOptionMenuClicked.set("Broadcast")
        for i in ideaDriveAddresses:
            addressOptionMenu['menu'].add_command(label=i, command=tk._setit(addressOptionMenuClicked, i))
        executeButton["state"]= "normal"
        commandFinderButton["state"]= "normal"
        addressOptionMenuClicked.set(ideaDriveAddresses[0])
    else:
        addressOptionMenuClicked.set("No Drives Available")
        executeButton["state"]= "disabled"
        commandFinderButton["state"]= "disabled"

def FindPorts():
    #Close open port, clear list and reinitialize
    global Ports
    for p in Ports:
        drive.CloseComms()
    Ports.clear()
    portOptionMenu['menu'].delete(0, "end")
    portOptionMenuClicked.set("No Port Devices Found")
    findAddressesButton.configure(state='disabled')
    #Find devices
    Ports = serial_ports()
    #Update GUI for found devices
    if Ports:
        UpdatePortOptionMenu()

def UpdatePortOptionMenu():
    #Clear list, disable address button and reset text
    portOptionMenu['menu'].delete(0, "end")
    portOptionMenuClicked.set("No Port Devices Found")
    findAddressesButton.configure(state='disabled')
    if Ports:
        for i in Ports:
            portOptionMenu['menu'].add_command(label=i, command=lambda value=i: portOptionMenuClicked.set(value))

        findAddressesButton.configure(state='normal')
        portOptionMenuClicked.set(Ports[0])
        drive.SetActivePort(Ports[0])
        drive.OpenComms()
    
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def FillCommandMenu():
    #Clear commands
    commandFinderOptionMenu.set('')
    #Initialize DLL command set
    drive.InitializeCommandSet()
    #Retrieve the command list from the DLL
    response = drive.GetCommandList()
    #Parse string into list
    ideaDriveCommandSet = response.split(",")
    ideaDriveCommandSet.sort()
    if ideaDriveCommandSet:
        commandFinderOptionMenu['values'] = ideaDriveCommandSet

def SetParamsOutputsEntryboxes(arg1):
    cmd = commandFinderOptionMenu.get()
    cmdLetter = drive.GetCommandLetterFromDescriptive(cmd)
    numberOfParams = drive.GetNumberOfParametersDesc(cmd)
    global paramList
    paramList = drive.GetParameterList(cmdLetter).split(",")
    numberOfOutputs = drive.GetNumberOfOutputsDesc(cmd)
    global outList
    outList = drive.GetOutputFieldList(cmdLetter).split(",")
    
    #Create x param entry boxes and y output entryboxes and render them to the display
    for widget in frmCommandParameter.winfo_children():
        widget.destroy()
    for widget in frmCommandOutput.winfo_children():
        widget.destroy()
    for i in range(0, numberOfParams, 1):
        IDparams[i] = Entry(frmCommandParameter, relief=tk.SUNKEN, width=25)
        IDparams[i].grid(column=1, row=i, sticky=NW)
        IDParamsLabels[i] = Label(frmCommandParameter, width=25, font="bold", text=paramList[i])
        IDParamsLabels[i].grid(column=0, row=i, sticky=NW)
    for i in range(0, numberOfOutputs, 1):
        IDoutputs[i] = Entry(frmCommandOutput, relief=tk.SUNKEN, width=25, state='disabled')
        IDoutputs[i].grid(column=3, row=i, sticky=NE)
        IDoutputsLabels[i] = Label(frmCommandOutput, width=25, font="bold", text=outList[i])
        IDoutputsLabels[i].grid(column=2, row=i, sticky=NE)
#endregion

#IDEA Drive Object
drive = IDEADrvCommander.IDEADrv("COM1", DLL_PATH)

#region GUI

#Frame: Drive Selection
frmSelector = Frame(root)
frmSelector.grid(row=0, column=0, columnspan = 4, sticky=W)

#Frame: Command Selection
frmCommandFinder = Frame(root)
frmCommandFinder.grid(row=5, column=0, columnspan=2)

#Frame: Command Parameter
frmCommandParameter = Frame(root)
frmCommandParameter.grid(row=7, column=0, sticky=W)

#Frame: Command Output
frmCommandOutput = Frame(root)
frmCommandOutput.grid(row=7, column=1, sticky=W)

#Label: Parameter Header
paramHeaderLabel = Label(root, width=25, text='Parameters', font=("Arial", 18, "bold"))
paramHeaderLabel.grid(row=6, column=0, sticky=W)

#Label: Output Header
outputHeaderLabel = Label(root, width=25, text='Outputs', font=("Arial", 18, "bold"))
outputHeaderLabel.grid(row=6, column=1, sticky=W)

#Labels: List of parameter labels
IDParamsLabels = [Label(frmCommandParameter, width=40, text='')]*MAX_NUM_OF_PARAMETERS

#Entry: List of parameter entry boxes
IDparams = [Entry(frmCommandParameter, relief=tk.SUNKEN, width=40)]*MAX_NUM_OF_PARAMETERS

#Labels: List of output labels
IDoutputsLabels = [Label(frmCommandParameter, width=40, text='')]*MAX_NUM_OF_OUTPUTS

#Entry: List of output entry boxes
IDoutputs = [Entry(frmCommandParameter, relief=tk.SUNKEN, width=40)]*MAX_NUM_OF_OUTPUTS

#Button: Find Addresses
findAddressesButton = Button(frmSelector, text="Find Drives", command=FindDrives, state='disabled', width=20)
findAddressesButton.grid(row=1, column=0, sticky=W, pady = 3)

#Button: Find Ports
findPortsButton = Button(frmSelector, text="Find Ports", command=FindPorts, width=20)
findPortsButton.grid(row=0, column=0, sticky=W, pady = 3)

#Command Select OptionMenu
commandFinderOptionMenu = ttk.Combobox(frmCommandFinder, values=ideaDriveCommandSet, state='readonly')
commandFinderOptionMenu.grid(row=0, column=0, sticky=W)
FillCommandMenu()
commandFinderOptionMenu.bind("<<ComboboxSelected>>", SetParamsOutputsEntryboxes)

#OptionMenu: Addresses
defaultText = "Click Find Drives"
addressOptionMenuClicked = StringVar(root)
addressOptionMenuClicked.set(defaultText)
addressOptionMenu = OptionMenu(frmSelector, addressOptionMenuClicked, value=ideaDriveAddresses)
addressOptionMenu.configure(indicatoron=0, compound=tk.RIGHT, image=arrowPNG, width=140)
addressOptionMenu.grid(row=1, column=1, sticky=W)

#OptionMenu: Ports
portOptionMenuClicked = StringVar(root)
portOptionMenuClicked.set("No Ports Available")
Ports = serial_ports()
portOptionMenu = OptionMenu(frmSelector, portOptionMenuClicked, value=Ports)
portOptionMenu.configure(indicatoron=0, compound=tk.RIGHT, image=arrowPNG, width=140)
portOptionMenu.grid(row=0, column=1, sticky=W)
if Ports:
    UpdatePortOptionMenu()

#Button: Send Command
executeButton = Button(root, text="Execute Command", command=SendCommand, state="disabled")
executeButton.grid(row=1, column=0, columnspan=2)

#Button: Send Dropdown Menu Command
commandFinderButton = Button(root, text="Execute Dropdown Command", command=SendDropDownCommand, state="disabled")
commandFinderButton.grid(row=4, column=0, columnspan=2)

#Entrybox: Commands Entry
executeEntry = Entry(root, relief=tk.SUNKEN, width=40)
executeEntry.grid(row=2, column=0, columnspan=2, pady=2)

#Textbox: IDEA drive command responses
responseTextbox = Text(root, height=2, width = 96, state='disabled')
responseTextbox.config(fg='black', bg='light grey')
responseTextbox.grid(row=3, column=0, columnspan=4, sticky=W, padx=2, pady=2)

#endregion
root.mainloop()

#Close Serial & delete drive
drive.CloseComms()
del drive
"""
Example Commands:

See IDEA Drive: Communications Manual for full command details.

Get Firmware Version Number -
"v\n"

Stop -
H0,8000,500,500,500,50,64\n

Index 7.81 Revolutions Clockwise -
I100000,256000,256000,256000,512000,512000,1000,1000,1500,1500,10,64\n

"""