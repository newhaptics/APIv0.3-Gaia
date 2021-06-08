# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 12:25:03 2020

@author: Derek Joslin
"""

import copy
import TactileTweener as tac
import GraphicsEngine as gr
import BoardCom as bc
import numpy as np


class HapticsEngine:

    #haptics engine takes in physics of a board and properly executes graphical commands based on the physics
    #take in the physics of the fluidic chip from matlab and use that to determine timing for actions
    #maybe have it take in an FC library class

    def __init__(self, tpw, th, ts, rows, columns, refreshProtocol):
        self.__tpw = tpw
        self.__th = th
        self.__ts = ts
        self.__rows = rows
        self.__columns = columns
        self.__currentState = [[False for i in range(0,columns)] for j in range(0,rows)]
        self.__desiredState = [[False for i in range(0,columns)] for j in range(0,rows)]
        self.ge = gr.GraphicsEngine(self.__desiredState)
        self.__connected = False
        self.__refreshInfo = {'refresh protocol': refreshProtocol}
        #calculate how fast each element in the chip updates based on the setup, hold, and pulse width of the element
        elementTiming = (np.array(ts) + np.array(th)).tolist()
        for rowIndex, row in enumerate(elementTiming):
            for columnIndex, element in enumerate(row):
                if element < tpw[rowIndex][columnIndex]:
                    element = tpw[rowIndex][columnIndex]

        self.__refreshInfo.update({'element refresh timing' : elementTiming})

    def get_size(self):
        """ returns a tuple of rows and columns """
        return (self.__columns, self.__rows)

    def get_currentState(self):
        """ returns the current state of the chip """
        return self.__currentState

    def get_desiredState(self):
        """ returns the state that the chip wants to be in """
        return self.__desiredState

    def set_desiredState(self, newState):
        """ sets a desired state of the chip """
        for rowIndex,row in enumerate(newState):
            for elemIndex,elem in enumerate(row):
                self.__desiredState[rowIndex][elemIndex] = copy.deepcopy(elem)
        #set the graphics engine matrix to the new desired matrix state
        self.ge.read_matrix(self.__desiredState)

    def set_refreshProtocol(self, protocol):
        """ sets the protocol for refreshing the chip and generating the refresh states """
        self.__refreshInfo['refresh protocol'] = protocol

    def quick_refresh(self):
        """ is a quick refresh protocol for controling the board and not the visualizer """
        for rowIndex,row in enumerate(self.__desiredState):
            for elemIndex,elem in enumerate(row):
                self.__currentState[rowIndex][elemIndex] = copy.deepcopy(elem)

        #self.__currentState = copy.deepcopy(self.__desiredState)

    def generate_refreshStates(self):
        """ creates the minimum number of frames to get from current state to desired state
        returns the time it takes to get from current state to desired state """
        self.__refresh_chip()
        uniqueFrames = self.__refreshInfo['unique frame times']
        refreshFrames = {}
# =============================================================================
#         for time in uniqueFrames:
#             refreshFrames.update({time : self.__get_timeFrame(time)})
# =============================================================================

        self.__refreshInfo.update({'refresh frames' : refreshFrames})

        return uniqueFrames

    def set_stateTime(self, t):
        """ sets the current state to a point in time t milliseconds after the refresh occurs """
        #first look for the refreshFrames precollected by the unique frames list
        if t in self.__refreshInfo['refresh frames']:
# =============================================================================
#             for rowIndex,row in enumerate(self.__refreshInfo['refresh frames'][t]):
#                 for elemIndex,elem in enumerate(row):
#                     self.__currentState[rowIndex][elemIndex] = copy.deepcopy(elem)
# =============================================================================
            #self.__currentState = self.__refreshInfo['refresh frames'][t]
            self.__set_currentState(self.__refreshInfo['refresh frames'][t])
        else:
            self.__refreshInfo['refresh frames'].update({t : self.__get_timeFrame(t)})
# =============================================================================
#             for rowIndex,row in enumerate(self.__refreshInfo['refresh frames'][t]):
#                 for elemIndex,elem in enumerate(row):
#                     self.__currentState[rowIndex][elemIndex] = copy.deepcopy(elem)
# =============================================================================
            self.__set_currentState(self.__refreshInfo['refresh frames'][t])

    def establish_connection(self, COM, onOff):
        self.com = bc.BoardCom(COM)
        self.__connected = True
        self.com.echo(onOff)
        self.com.ARDturn_on()
        self.com.ARDclear_all()
        self.com.ARDset_matrix(self.__currentState)
        #self.com.ARDget_matrix()


# =============================================================================
#   This is when using the embedded control board not arduino
#         self.com.set_size(self.__rows,self.__columns)
#         self.com.get_size()
#         self.com.set_times(max(max(self.__ts)), max(max(self.__tpw)), max(max(self.__th)))
#         self.com.get_times()
#         self.com.set_row(self.__columns + 2,1)
#         self.com.get_row()
#         self.com.set_col(2, 1)
#         self.com.get_col()
#         self.com.set_trig(1)
#         self.com.get_trig()
#         self.com.set_source(0)
#         self.com.get_source()
#         self.com.set_matrix(self.__currentState)
#         self.com.get_matrix()
#         self.com.start()
#         self.com.refresh()
#         self.com.set_led(1,1)
# =============================================================================

    def end_connection(self):
        self.com.stop()
        self.com.close()
        del self.com
        self.__connected = False


    def check_connection(self):
        return self.__connected

    def send_toBoard(self):
        self.com.ARDset_matrix(np.fliplr(np.array(self.__currentState)).tolist())
        #self.com.ARDget_matrix()


# =============================================================================
#Old embedded send to board code
#         self.com.set_matrix(np.fliplr(np.array(self.__currentState)).tolist())
#         self.com.get_matrix()
#         self.com.refresh()
# =============================================================================


    def __set_currentState(self, newState):
        """ sets the current matrix to the state given """
        for rowIndex,row in enumerate(newState):
            for elemIndex,elem in enumerate(row):
                self.__currentState[rowIndex][elemIndex] = copy.deepcopy(elem)


    def __refresh_chip(self):
        """ creates the frames and to get from current state to desired state """

        #create a tweener to get the frames to get to the desired state
        tt = tac.TactileTweener()

        #tween the frames
        refreshFrames = tt.get_tweenFrames(copy.deepcopy(self.__currentState), copy.deepcopy(self.__desiredState), self.__refreshInfo['refresh protocol'])

        #set the current time to 0
        currentTime = 0

        #calculate the time when each element will refresh for each frame
        elementTiming = self.__refreshInfo['element refresh timing']
        timeMatrix = [[currentTime for i in range(0,self.__columns)] for j in range(0,self.__rows)]

        x = 0
        highest = 0
        #list for timing of each unique frame
        uniqueFrames = []
        for index, frame in enumerate(refreshFrames):
            for rowIndex, row in enumerate(frame['element change']):
                for columnIndex, elementChange in enumerate(row):
                    if elementChange == True:
                        val = timeMatrix[rowIndex][columnIndex] + elementTiming[rowIndex][columnIndex] + highest
                        timeMatrix[rowIndex][columnIndex] = val
                        uniqueFrames.append(timeMatrix[rowIndex][columnIndex] + 1)
            if highest < (max(map(max, timeMatrix))):
                highest = (max(map(max, timeMatrix)))
            #display_frame(frame['state'], frame['element change'], timeMatrix, x)
            x += 1
            refreshFrames[index].update({'timing data': copy.deepcopy(timeMatrix)})

        uniqueFrames = sorted(list(set(uniqueFrames)))
        self.__refreshInfo.update({'frame info' : refreshFrames, 'unique frame times' : uniqueFrames})

    def __get_timeFrame(self,time):
        """At a certain time(in milliseconds) show what the state would look like at that time"""
        #search through the timing data in frame by frame info and find the first frame with a higher timing data value than time
        #create a set of frames to store the refresh that occurs
        self.__set_currentState(copy.deepcopy(self.__refreshInfo['frame info'][0]['state']))
        for frameIndex,frame in enumerate(self.__refreshInfo['frame info']):
            for rowIndex,row in enumerate(frame['timing data']):
                for columnIndex,changeTime in enumerate(row):
                    if (changeTime < time) and (frameIndex > 0):
                        #get the frame before and the current frame
                        beforeFrame = self.__refreshInfo['frame info'][frameIndex - 1]
                        currentFrame = self.__refreshInfo['frame info'][frameIndex]
                         #set the appropriate value equal to the current state
                        if currentFrame['timing data'][rowIndex][columnIndex] < time:
                            self.__currentState[rowIndex][columnIndex] = copy.deepcopy(currentFrame['state'][rowIndex][columnIndex])
                        else:
                            self.__currentState[rowIndex][columnIndex] = copy.deepcopy(beforeFrame['state'][rowIndex][columnIndex])
        return self.__currentState



# =============================================================================
#
# def display_frame(state, element_change, timing_data, number):
#     print('frame: {0}'.format(number))
#     print('---------------------------\n\r')
#     print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
#                      for row in state]))
#     print('T/F')
#     print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
#                      for row in element_change]))
#     print('timing data')
#     print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
#                      for row in timing_data]))
#
# =============================================================================
