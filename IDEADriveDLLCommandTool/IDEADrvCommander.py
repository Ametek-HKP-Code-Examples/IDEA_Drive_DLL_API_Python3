# Name:           IDEADrvCommander.py
# Author:         Chad F.
# Date:           7-13-23
# Environment:    Python 3.11
# File Type:      Object class
# Description:    This file is to interface with the IDEA Drive (Firmware V5+) in Python. To use, 
#                 create an IDEADrv object, open the appropriate serial port and set the appropriate 
#                 drive address (if drives are networked in RS485). Use the SendCommand function
#                 to send commands or use the individual command functions. Refer to the IDEA Drive
#                 Communications manual for more information on the commands and the parameters they
#                 accept.

from ctypes import *
import time

class IDEADrv:
#region Constructor
    def __init__(self, Port, path, address=""):
        self.MAX_BUFSIZE = 1024
        self.MAX_STREAM_BUFF_SIZE = 85000
        self.cppdll = CDLL(path)
        self.serialPort = Port
        self.DLL_Path = path
        self.IDriveAddress = address
        self.SetCurrentAddress(address)

    def __str__(self):
        return self.serialPort

#endregion
#region Utilities
    def enc(self, x):
        y = x.encode('UTF-8')
        return y

    def Buffer2String(self, buf):
        rtnStr = str(buf, 'UTF-8')
        index = rtnStr.find('\r')
        if index > -1:
            rtnStr = rtnStr.replace("\r","",1)
        return rtnStr
#endregion
#region G&S Methods
    def GetBufferSize():
        print("Buffer Size = " + str(self.MAX_BUFSIZE))
        return self.MAX_BUFSIZE  
  
    def SetBufferSize(self,Size):
        self.MAX_BUFSIZE = Size

    def GetDLLPath():
        print("Full DLL Path = " + str(self.DLL_Path))
        return self.DLL_Path

    def SetDLLPath(path):
        self.DLL_Path = path

    def SetActivePort(self,inPort):
        self.serialPort = inPort
#endregion
#region Communications
    def OpenComms(self):
        self.cppdll.OpenSerial.argtypes = [c_char_p]
        self.cppdll.OpenSerial.restype = c_int
        tmp = c_char_p(self.enc(self.serialPort))
        _portHandle = self.cppdll.OpenSerial(tmp)
        time.sleep(0.06)

    def CloseComms(self):
        self.cppdll.IsSerialOpen.restype = c_bool
        self.cppdll.CloseSerial.restype = c_bool
        while(self.cppdll.IsSerialOpen()):
            if (self.cppdll.CloseSerial()): break
            time.sleep(0.01)

    def SetCurrentAddress(self, localAddress):
        self.cppdll.SetCurrentAddress.argtypes = [c_char_p, c_int]
        self.cppdll.SetCurrentAddress(self.enc(localAddress),len(localAddress))
        self.IDriveAddress = localAddress

    def IsSerialOpen(self):
        self.cppdll.IsSerialOpen.restype = c_bool
        return self.cppdll.IsSerialOpen()

    def GetAllAvailableAddresses(self):
        if not self.IsSerialOpen():
            return ""
        numberOfPossibleIDEADriveAddresses = 256
        _addressList = (c_int*numberOfPossibleIDEADriveAddresses)(*[x for x in range(numberOfPossibleIDEADriveAddresses)])
        self.cppdll.GetAddresses(_addressList)
        return _addressList

#endregion
#region NO R/W Commands
    def Noop(self):
        self.cppdll.Noop()

    def ReturnFromSub(self):
        self.cppdll.ReturnFromSub()

    def SingleStep(self):
        self.cppdll.SingleStep()

    def WaitForMove(self):
        self.cppdll.WaitForMove()

    def Reset(self):
        self.cppdll.Reset()

    def Abort(self):
        self.cppdll.Abort()

    def EnableDataLogging(self):
        self.cppdll.EnableDataLogging()

    def DisableDataLogging(self):
        self.cppdll.DisableDataLogging()

#endregion
#region Readonly Commands
    def GetFirmwareVersion(self):
        self.cppdll.GetFWVersion.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetFWVersion(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetEncoderConfiguration(self):
        self.cppdll.GetEncoderConfiguration.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetEncoderConfiguration(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetHallSensorConfiguration(self):
        self.cppdll.GetHallSensorConfiguration.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetHallSensorConfiguration(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetMotorType(self):
        self.cppdll.GetMotorType.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetMotorType(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetMotorParameters(self):
        self.cppdll.GetMotorParameters.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetMotorParameters(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetControlReference(self):
        self.cppdll.GetControlReference.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetControlReference(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetDriveAddress(self):
        self.cppdll.GetDriveAddress.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetDriveAddress(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetMaxDriveCurrent(self):
        self.cppdll.GetMaxDriveCurrent.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetMaxDriveCurrent(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetFactoryConfiguration(self):
        self.cppdll.GetFactoryConfiguration.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetFactoryConfiguration(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetVelocityProfile(self):
        self.cppdll.GetVelocityProfile.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetVelocityProfile(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetControlGain(self):
        self.cppdll.GetControlGain.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetControlGain(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def IsMoveExecuting(self):
        self.cppdll.IsMoveExecuting.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.IsMoveExecuting(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetPositionVelocity(self):
        self.cppdll.GetPositionVelocity.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetPositionVelocity(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def IsInputOverride(self):
        self.cppdll.IsInputOverride.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.IsInputOverride(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetIOReading(self):
        self.cppdll.GetIOReading.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetIOReading(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetFaultParameters(self):
        self.cppdll.GetFaultParameters.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetFaultParameters(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetFaultReading(self):
        self.cppdll.GetFaultReading.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetFaultReading(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetStartupProgramName(self):
        self.cppdll.GetStartupProgramName.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetStartupProgramName(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def IsProgramExecuting(self):
        self.cppdll.IsProgramExecuting.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.IsProgramExecuting(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

    def GetListProgramNames(self):
        self.cppdll.GetListProgramNames.argtypes = [c_char_p, c_int]
        mystrbuf = create_string_buffer(self.MAX_BUFSIZE)
        mystrbuf[0] = 0
        self.cppdll.GetListProgramNames(mystrbuf, len(mystrbuf))
        return self.Buffer2String(mystrbuf.value)

#endregion
#region Writeonly Commands
    def SetEncoderConfiguration(self, commandParameters):
        self.cppdll.SetEncoderConfiguration.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetEncoderConfiguration(self.enc(commandParameters), len(commandParameters))
        return success

    def SetHallSensorConfiguration(self, commandParameters):
        self.cppdll.SetHallSensorConfiguration.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetHallSensorConfiguration(self.enc(commandParameters), len(commandParameters))
        return success

    def SetMotorParameters(self, commandParameters):
        self.cppdll.SetMotorParameters.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetMotorParameters(self.enc(commandParameters), len(commandParameters))
        return success
    def SetMotorType(self, commandParameters):
        self.cppdll.SetMotorType.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetMotorType(self.enc(commandParameters), len(commandParameters))
        return success

    def SetControlReferenceConfiguration(self, commandParameters):
        self.cppdll.SetControlReferenceConfiguration.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetControlReferenceConfiguration(self.enc(commandParameters), len(commandParameters))
        return success

    def SetDriveAddress(self, commandParameters):
        self.cppdll.SetDriveAddress.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetDriveAddress(self.enc(commandParameters), len(commandParameters))
        return success

    def SetPassword(self, commandParameters):
        self.cppdll.SetPassword.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetPassword(self.enc(commandParameters), len(commandParameters))
        return success

    def RemovePassword(self, commandParameters):
        self.cppdll.RemovePassword.argtypes = [c_char_p, c_int]
        success = self.cppdll.RemovePassword(self.enc(commandParameters), len(commandParameters))
        return success

    def MoveToPosition(self, commandParameters):
        self.cppdll.MoveToPosition.argtypes = [c_char_p, c_int]
        success = self.cppdll.MoveToPosition(self.enc(commandParameters), len(commandParameters))
        return success

    def IndexDistance(self, commandParameters):
        self.cppdll.IndexDistance.argtypes = [c_char_p, c_int]
        success = self.cppdll.IndexDistance(self.enc(commandParameters), len(commandParameters))
        return success

    def GoAtSpeed(self, commandParameters):
        self.cppdll.GoAtSpeed.argtypes = [c_char_p, c_int]
        success = self.cppdll.GoAtSpeed(self.enc(commandParameters), len(commandParameters))
        return success

    def GoAtVoltage(self, commandParameters):
        self.cppdll.GoAtVoltage.argtypes = [c_char_p, c_int]
        success = self.cppdll.GoAtVoltage(self.enc(commandParameters), len(commandParameters))
        return success

    def GoAtTorque(self, commandParameters):
        self.cppdll.GoAtTorque.argtypes = [c_char_p, c_int]
        success = self.cppdll.GoAtTorque(self.enc(commandParameters), len(commandParameters))
        return success

    def ImmediateStop(self, commandParameters):
        self.cppdll.ImmediateStop.argtypes = [c_char_p, c_int]
        success = self.cppdll.ImmediateStop(self.enc(commandParameters), len(commandParameters))
        return success

    def StopMovement(self, commandParameters):
        self.cppdll.StopMovement.argtypes = [c_char_p, c_int]
        success = self.cppdll.StopMovement(self.enc(commandParameters), len(commandParameters))
        return success

    def SetVelocityProfileWaveshape(self, commandParameters):
        self.cppdll.SetVelocityProfileWaveshape.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetVelocityProfileWaveshape(self.enc(commandParameters), len(commandParameters))
        return success

    def SetControlGains(self, commandParameters):
        self.cppdll.SetControlGains.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetControlGains(self.enc(commandParameters), len(commandParameters))
        return success

    def SetPositionOrigin(self, commandParameters):
        self.cppdll.SetPositionOrigin.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetPositionOrigin(self.enc(commandParameters), len(commandParameters))
        return success

    def SetOutputState(self, commandParameters):
        self.cppdll.SetOutputState.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetOutputState(self.enc(commandParameters), len(commandParameters))
        return success

    def SetInputInterrupts(self, commandParameters):
        self.cppdll.SetInputInterrupts.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetInputInterrupts(self.enc(commandParameters), len(commandParameters))
        return success

    def SetPositionLimitFault(self, commandParameters):
        self.cppdll.SetPositionLimitFault.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetPositionLimitFault(self.enc(commandParameters), len(commandParameters))
        return success

    def SetCurrentLimitDurationFault(self, commandParameters):
        self.cppdll.SetCurrentLimitDurationFault.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetCurrentLimitDurationFault(self.enc(commandParameters), len(commandParameters))
        return success

    def SetPositionErrorFault(self, commandParameters):
        self.cppdll.SetPositionErrorFault.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetPositionErrorFault(self.enc(commandParameters), len(commandParameters))
        return success

    def RunProgram(self, commandParameters):
        self.cppdll.RunProgram.argtypes = [c_char_p, c_int]
        success = self.cppdll.RunProgram(self.enc(commandParameters), len(commandParameters))
        return success

    def ExecuteProgram(self, commandParameters):
        self.cppdll.ExecuteProgram.argtypes = [c_char_p, c_int]
        success = self.cppdll.ExecuteProgram(self.enc(commandParameters), len(commandParameters))
        return success

    def SetStartupProgram(self, commandParameters):
        self.cppdll.SetStartupProgram.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetStartupProgram(self.enc(commandParameters), len(commandParameters))
        return success

    def DeleteProgram(self, commandParameters):
        self.cppdll.DeleteProgram.argtypes = [c_char_p, c_int]
        success = self.cppdll.DeleteProgram(self.enc(commandParameters), len(commandParameters))
        return success

    def SetDebugMode(self, commandParameters):
        self.cppdll.SetDebugMode.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetDebugMode(self.enc(commandParameters), len(commandParameters))
        return success

    def RunToLabel(self, commandParameters):
        self.cppdll.RunToLabel.argtypes = [c_char_p, c_int]
        success = self.cppdll.RunToLabel(self.enc(commandParameters), len(commandParameters))
        return success

    def GotoAddress(self, commandParameters):
        self.cppdll.GotoAddress.argtypes = [c_char_p, c_int]
        success = self.cppdll.GotoAddress(self.enc(commandParameters), len(commandParameters))
        return success

    def JumpNTimes(self, commandParameters):
        self.cppdll.JumpNTimes.argtypes = [c_char_p, c_int]
        success = self.cppdll.JumpNTimes(self.enc(commandParameters), len(commandParameters))
        return success

    def GotoIf(self, commandParameters):
        self.cppdll.GotoIf.argtypes = [c_char_p, c_int]
        success = self.cppdll.GotoIf(self.enc(commandParameters), len(commandParameters))
        return success

    def GotoSub(self, commandParameters):
        self.cppdll.GotoSub.argtypes = [c_char_p, c_int]
        success = self.cppdll.GotoSub(self.enc(commandParameters), len(commandParameters))
        return success

    def ReturnTo(self, commandParameters):
        self.cppdll.ReturnTo.argtypes = [c_char_p, c_int]
        success = self.cppdll.ReturnTo(self.enc(commandParameters), len(commandParameters))
        return success

    def WaitTime(self, commandParameters):
        self.cppdll.WaitTime.argtypes = [c_char_p, c_int]
        success = self.cppdll.WaitTime(self.enc(commandParameters), len(commandParameters))
        return success

    def Label(self, commandParameters):
        self.cppdll.Label.argtypes = [c_char_p, c_int]
        success = self.cppdll.Label(self.enc(commandParameters), len(commandParameters))
        return success

    def Comment(self, commandParameters):
        self.cppdll.Comment.argtypes = [c_char_p, c_int]
        success = self.cppdll.Comment(self.enc(commandParameters), len(commandParameters))
        return success

    def SetInputs(self, commandParameters):
        self.cppdll.SetInputs.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetInputs(self.enc(commandParameters), len(commandParameters))
        return success

    def SetInputOverride(self, commandParameters):
        self.cppdll.SetInputOverride.argtypes = [c_char_p, c_int]
        success = self.cppdll.SetInputOverride(self.enc(commandParameters), len(commandParameters))
        return success

#endregion
#region Misc Commands
    def SendCommand(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.SendCommand.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.SendCommand(self.enc(commandParameters), outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

    def SendTimedCommand(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.SendTimedCommand.argtypes = [c_char_p, c_char_p, c_int, c_int, c_int]
        self.cppdll.SendTimedCommand(self.enc(commandParameters), outputBuffer, len(outputBuffer), 60, 30)
        return self.Buffer2String(outputBuffer.value)

    def GetNVParameter(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.GetNVParameter.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.GetNVParameter(self.enc(commandParameters), outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

    def DownloadProgram(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.DownloadProgram.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.DownloadProgram(self.enc(commandParameters), outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

    def IsValidPassword(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.IsValidPassword.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.IsValidPassword(self.enc(commandParameters), outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

    def RecallProgram(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.RecallProgram.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.RecallProgram(self.enc(commandParameters), outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

    def GetListProgramNames(self):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.GetListProgramNames.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.GetListProgramNames(outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

    def UpdateFirmware(self, passwordIn):
        self.cppdll.UpdateFirmware.argtypes = [c_bool]
        if passwordIn == "@metek23":
            return self.cppdll.UpdateFirmware(c_bool(True))
        else:
            return self.cppdll.UpdateFirmware(c_bool(False))

    def RestoreFactoryDefaults(self, check):
        self.cppdll.RestoreFactoryDefaults.argtypes = [c_bool]
        if check:
            return self.cppdll.RestoreFactoryDefaults(c_bool(True))
        else:
            return self.cppdll.RestoreFactoryDefaults(c_bool(False))
#endregion

#region Command Info Commands
    def InitializeCommandSet(self):
        self.cppdll.InitializeCommandSet()

    def GetCommandName(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.GetCommandName.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.GetCommandName(self.enc(commandParameters), outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

    def GetCommandList(self):
        outputBuffer = create_string_buffer(self.MAX_STREAM_BUFF_SIZE)
        self.cppdll.GetCommandList.argtypes = [c_char_p]
        self.cppdll.GetCommandList(outputBuffer)
        return self.Buffer2String(outputBuffer.value)

    def GetNumberOfOutputsDesc(self, commandParameters):
        self.cppdll.GetNumberOfOutputsDesc.argtypes = [c_char_p]
        self.cppdll.GetNumberOfOutputsDesc.restype = c_int
        return self.cppdll.GetNumberOfOutputsDesc(self.enc(commandParameters))

    def GetNumberOfParametersDesc(self, commandParameters):
        self.cppdll.GetNumberOfParametersDesc.argtypes = [c_char_p]
        self.cppdll.GetNumberOfParametersDesc.restype = c_int
        return self.cppdll.GetNumberOfParametersDesc(self.enc(commandParameters))

    def GetCommandLetterFromDescriptive(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.GetCommandLetterFromDescriptive.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.GetCommandLetterFromDescriptive(self.enc(commandParameters), outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

    def GetParameterList(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.GetParameterList.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.GetParameterList(self.enc(commandParameters), outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

    def GetOutputFieldList(self, commandParameters):
        outputBuffer = create_string_buffer(self.MAX_BUFSIZE)
        self.cppdll.GetOutputFieldList.argtypes = [c_char_p, c_char_p, c_int]
        self.cppdll.GetOutputFieldList(self.enc(commandParameters), outputBuffer, len(outputBuffer))
        return self.Buffer2String(outputBuffer.value)

#endregion