# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:39:32 2020

@author: Derek Joslin
"""

import serial
import math


class BoardCom:
    
     #the Board Com object contains a serial port connection object and commands to communicate with hardware


    def __init__(self, port):
        #115200 for the embedded board
        self.port = serial.Serial(port, 57600, timeout=1)
        self.__echo = 1 #by default echo is on

    #sets the echo of the com port onOff (0=Off, 1=On)
    def echo(self, onOff):
        if onOff:
            self.__echo = 1
        else:
            self.__echo = 0
        
        
    #Display the supported commands.
    def help(self):
        self.port.write('HELP\n'.encode('utf-8'))
        self.__print_rx()

    #Reset the controller board.
    def reset(self):
        self.port.write('RESET\n'.encode('utf-8'))
        self.__print_rx()

    #Display the Firmware Version.
    def version(self):
        self.port.write('VERSION\n'.encode('utf-8'))
        self.__print_rx()

    #Set the size of the fluidic chip array as m (rows) n (cols). Example: SETSIZE 3 4
    def set_size(self,rows,columns):
        self.port.write('SETSIZE {0} {1}\n'.format(rows,columns).encode('utf-8'))
        self.__print_rx()

    #Display the current size of the fluidic chip array.
    def get_size(self):
        self.port.write('GETSIZE\n'.encode('utf-8'))
        self.__print_rx()

    #Set the timing parameters for the solenoids as t_s t_pw t_ph (ms). Example: SETTIMES 25 35 45
    def set_times(self,ts,tpw,tph):
        self.port.write('SETTIMES {0} {1} {2}\n'.format(ts,tpw,tph).encode('utf-8'))
        self.__print_rx()

    #Display the current timing parameters for the solenoids.
    def get_times(self):
        self.port.write('GETTIMES\n'.encode('utf-8'))
        self.__print_rx()

    #Set the row starting index and step size as r (row index) s (step size). Example SETROW 0 1
    def set_row(self,rowIndex,step):
        self.port.write('SETROW {0} {1}\n'.format(rowIndex,step).encode('utf-8'))
        self.__print_rx()

    #Display the current row starting index and step size
    def get_row(self):
        self.port.write('GETROW\n'.encode('utf-8'))
        self.__print_rx()

    #Set the column starting index and step size as c (column index) s (step size). Example: SETCOL 3 1
    def set_col(self,columnIndex,step):
        self.port.write('SETCOL {0} {1}\n'.format(columnIndex,step).encode('utf-8'))
        self.__print_rx()

    #Display the current column starting index and step size.
    def get_col(self):
        self.port.write('GETCOL\n'.encode('utf-8'))
        self.__print_rx()

    #Set the trigger index as t (trigger index). Example: SETTRIG 60
    def set_trig(self,tIndex):
        self.port.write('SETTRIG {0}\n'.format(tIndex).encode('utf-8'))
        self.__print_rx()

    #Display the current trigger index.
    def get_trig(self):
        self.port.write('GETTRIG\n'.encode('utf-8'))
        self.__print_rx()

    #Set the source index as s (source index). Example: SETSOURCE 61
    def set_source(self,sIndex):
        self.port.write('SETSOURCE {0}\n'.format(sIndex).encode('utf-8'))
        self.__print_rx()

    #Display the current source index.
    def get_source(self):
        self.port.write('GETSOURCE\n'.encode('utf-8'))
        self.__print_rx()

    #Set the states for the solenoids in the matrix. Example: SETMATRIX A1B4 C39F 56A
    def set_matrix(self,mat):
        self.port.write('SETMATRIX'.encode('utf-8'))
        #write each matrix row
        s = ''
        for row in mat:
            row = list(map(int, row)) #converts true/false to one zero
            a = ''.join(map(str, row))
            w = math.ceil(len(row)/4)
            pad = w*4 - len(row)
            a = '{0}{1}'.format(a, '0'*pad)
            a = '{:0{width}X}'.format(int(a,2), width=w)
            s = '{0} {1}'.format(s, a)
        self.port.write('{0}'.format(s).encode('utf-8'))
        self.port.write('\n'.encode('utf-8'))
        self.__print_rx()

    #Get the states for the solenoids in the matrix.
    def get_matrix(self):
        self.port.write('GETMATRIX\n'.encode('utf-8'))
        self.__print_rx()

    #Start solenoids operating by turning on Source and the gates.
    def start(self):
        self.port.write('START\n'.encode('utf-8'))
        self.__print_rx()

    #Refresh all solenoids from pixel data.
    def refresh(self):
        self.port.write('REFRESH\n'.encode('utf-8'))
        self.__print_rx()

    #Stop all solenoids by turning them off.
    def stop(self):
        self.port.write('STOP\n'.encode('utf-8'))
        self.__print_rx()

    #Set the state (0/1) for the specified solenoid index (0-79). Example: SETBIT 62 1
    def set_bit(self,EVI,state):
        self.port.write('SETBIT {0} {1}\n'.format(EVI,state).encode('utf-8'))
        self.__print_rx()

    #Set the states (0-FF) for the specified byte index (0-9). Example: SETBYTE 3 F3
    def set_byte(self,byte,state):
        self.port.write('SETBYTE {0} {1}\n'.format(byte,state).encode('utf-8'))
        self.__print_rx()

    #Set the state (0=Off, 1=On) for the specified status LED (1-3). Example: SETLED 2 1
    def set_led(self,Led,state):
        self.port.write('SETLED {0} {1}\n'.format(Led,state).encode('utf-8'))
        self.__print_rx()

    #Display the states for the option switches
    def get_switches(self):
        self.port.write('GETSWITCHES\n'.encode('utf-8'))
        self.__print_rx()

    #closes the serial port
    def close(self):
        self.port.close()

    #if echo is on prints the recieve data
    def __print_rx(self):
        if self.__echo:
            print(self.__read_rx())
        else:
            pass
        
    #reads in data on the serial line
    def __read_rx(self):
        self.port.flush()
        return self.port.read_until('') #.decode('utf-8')
    
    
    
    """ New functionality for the arduino """
    
    
    #sets a row on the chip
    def ARDset_row(self, rowIndex, rowData):
        #create list with required parameters
        output = []
        
        #select the select Row Function (1)
        output.append(1)
         
        #add the row index to the list
        output.append(rowIndex)
        
        #take list of rowData and add it to the list, but concatenated with 8 elements as a byte
        row = list(map(int, rowData))
        fill = 0
        N = 8
        tempList = row + [fill] * N
        subList = [tempList[n:n+N] for n in range(0, len(row), N)]
        
        for lst in subList:
            s = '0b' + ''.join(map(str, lst))
            output.append(int(s, base=2))
        
        #send as bytearray with each parameter as a byte
        self.port.write(bytearray(output))
        
        #print the recieved bit if echo is on
        self.__print_rx()
        
        
    def ARDclear_all(self):
        #create list of bytes to send
        output = []
        
        #select the first function
        output.append(2)
        
        #send the byte array
        self.port.write(bytearray(output))
        
        #print the recieved bit
        self.__print_rx()
        
        
        
            
    def ARDget_matrix(self):
        #create list of bytes to be sent
        output = []
        
        #select the third function
        output.append(3)
        
        #send the command
        self.port.write(bytearray(output))
        
        #read the current matrix state
        self.__print_rx()
        
        
        
        
            
    def ARDis_idle(self):
        #create list to be the output
        output = []
        
        #select the fourth function
        output.append(4)
        
        #send the byte
        self.port.write(bytearray(output))
        
        #read whether the device is idle
        self.__print_rx()
        
        
    def ARDturn_off(self):
        #create the list for output
        output = []
        
        #select the fifth function
        output.append(5)
        
        #send the byte
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__print_rx()
        
        
    def ARDturn_on(self):
        #create a list for the output
        output = []
        
        #select the sixth function
        output.append(6)
        
        #send the command
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__print_rx()
        
    
        
        
        
    def ARDset_matrix(self, mat):
        #create a list for the output
        output = []
        
        #select the seventh function
        output.append(7)
        
        #take list of rows and create byte arrays out of each row
        fill = 0
        N = 8
        for rowData in mat:
            row = list(map(int, rowData))[::-1]
            tempList = row + [fill] * N
            subList = [tempList[n:n+N] for n in range(0, len(row), N)]
            for lst in subList:
                s = '0b' + ''.join(map(str, lst))
                output.append(int(s, base=2))
    
        #send the command
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__print_rx()
        
        
        
    def ARDset_dot(self, rowIndex, colIndex, data):
        #create output list
        output = []
        
        #select the eighth function
        output.append(8)
        
        #add the row index column index and state
        output.append(rowIndex)
        output.append(colIndex)
        output.append(data)
        
        #send the command
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__print_rx()
        
        
    def ARDset_all(self, data):
        #create output list
        output = []
        
        #select the eighth function
        output.append(9)
        
        #add the desired data for the state to be set to
        output.append(data)
        
        #send the command
        self.port.write(bytearray(output))
        
        #read the output on the serial port
        self.__print_rx()
        
        


# =============================================================================
# startMatrix = [[1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
#                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]]
# 
# com = BoardCom("COM5")
# com.set_matrix(startMatrix)
# 
# =============================================================================
