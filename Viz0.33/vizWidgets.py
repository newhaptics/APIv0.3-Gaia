# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:20:14 2020

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

import qrc_resources
import numpy as np
import NHAPI as nh

from pyqtconsole.console import PythonConsole
import pyqtconsole.highlighter as hl

#override close event
class guiConsole(PythonConsole):
    def __init__(self):

        super().__init__(formats={
            'keyword':    hl.format('blue', 'bold'),
            'operator':   hl.format('red'),
            'brace':      hl.format('darkGray'),
            'defclass':   hl.format('black', 'bold'),
            'string':     hl.format('magenta'),
            'string2':    hl.format('darkMagenta'),
            'comment':    hl.format('darkGreen', 'italic'),
            'self':       hl.format('black', 'italic'),
            'numbers':    hl.format('brown'),
            'inprompt':   hl.format('darkBlue', 'bold'),
            'outprompt':  hl.format('darkRed', 'bold'),
            })

        #add all the api functions to the gui console
        super().push_local_ns('erase', nh.erase)
        super().push_local_ns('fill', nh.fill)
        super().push_local_ns('stroke', nh.stroke)
        super().push_local_ns('direct', nh.direct)
        super().push_local_ns('dot', nh.dot)
        super().push_local_ns('line', nh.line)
        super().push_local_ns('curve', nh.curve)
        super().push_local_ns('circle', nh.circle)
        super().push_local_ns('rect', nh.rect)
        super().push_local_ns('triangle', nh.triangle)
        super().push_local_ns('polygon', nh.polygon)
        super().push_local_ns('latin', nh.latin)
        super().push_local_ns('braille', nh.braille)
        super().push_local_ns('clear', nh.clear)
        super().push_local_ns('state', nh.state)
        super().push_local_ns('desired', nh.desired)
        super().push_local_ns('refresh', nh.refresh)
        super().push_local_ns('setMat', nh.setMat)
        super().push_local_ns('quickRefresh', nh.quickRefresh)
        super().push_local_ns('times', nh.times)
        super().push_local_ns('frames', nh.frames)
        super().push_local_ns('connect', nh.connect)
        super().push_local_ns('disconnect', nh.disconnect)
        super().push_local_ns('settings', nh.settings)

    def closeEvent(event):
        if nh.engine.check_connection():
            nh.disconnect()
            event.accept()
        else:
            event.accept()
        
        

class displayMat(qw.QTableView):
    def __init__(self, state, dim):
        """
        reads in a list of the current FC state. displays that state of 1s and 0s in a matrix of png images
        if val is a one, that element in the table reads in the raised image png. If the element is a zero that element reads in the
        lowered image png.
        """
        super().__init__()
        self.state = stateMat(state)
        self.setModel(self.state)
        
        
        delegate = pinDelegate(state, dim, self)
        self.setItemDelegate(delegate)
        
# =============================================================================
#     def data(self, index, role):
#         """
#         Returns the text or formatting for a particular cell, depending on the 
#         role supplied.
#         """
#         if role == qc.Qt.DRole:
#             if self.state[index.row()][index.column()] == 1:
#                 return qc.QVariant(self.filledIcon)
#             else:
#                 return qc.QVariant(self.emptyIcon)
#             
#         #Note that it is first cast as a QIcon before
#         #being cast as a QVariant.
# =============================================================================

# =============================================================================
# 
#     def itemDelegate(self, index):
#         if self.state[index.row()][index.column()] == 1:
#             return qw.QAbstractItemDelegate()
#         else:
#             return qw.QAbstractItemDelegate()
# 
# =============================================================================



class stateMat(qc.QAbstractTableModel):
    def __init__(self, state):
        """
        Qt friendly container to hold the data of a state in a haptics engine
        state will be a list of lists
        """
        super().__init__()

        #store the list and the number of rows and columns
        self.__state = state
        newMat = np.array(state)
        dim = newMat.shape
        self.__columns = dim[1]
        self.__rows = dim[0]



    def rowCount(self, parent):
        return self.__rows

    def columnCount(self, parent):
        return self.__columns

    def data(self, index, role):
        """
        take in a list and parse the data inside the list and
        store inside the model container
        """
        
        return self.__state[index.row()][index.column()]

# =============================================================================
#     def setData(self, index, value, role):
#         """
#         sets the value of the state equal to the new state of the engine
#         """
#         self.__state = value
# =============================================================================

# =============================================================================
#     def flags():
#
#     def insertRows():
#
#     def removeRows():
#
#     def insertColumns():
#
#     def removeColumns():
# =============================================================================

class pinDelegate(qw.QStyledItemDelegate):
    def __init__(self, state, dim, parent = None):
        super().__init__(parent)
        self.__state = state
        self.__size = qc.QSize(dim[0], dim[1])
        self.filledIcon = qg.QIcon(":filledPin")
        self.emptyIcon = qg.QIcon(":emptyPin")
        
    def get_icon(self, index):
        # get the icon according to the condition:
        # In this case, for example, 
        # the icon will be repeated periodically
        if self.__state[index.row()][index.column()] == 1:
            return self.filledIcon
        else:
            return self.emptyIcon

    def paint(self, painter, option, index):
        icon = self.get_icon(index)
        icon.paint(painter, option.rect, qc.Qt.AlignCenter)


    def sizeHint(self, option, index):
        return self.__size
    
    
class MySwitch(qw.QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMaximumWidth(150)
        self.setMaximumHeight(150)

    def paintEvent(self, event):
        label = "ON" if self.isChecked() else "OFF"
        bg_color = qc.Qt.green if self.isChecked() else qc.Qt.red

        radius = 13
        width = 34
        center = self.rect().center()

        painter = qg.QPainter(self)
        painter.setRenderHint(qg.QPainter.Antialiasing)
        painter.setBrush(qg.QColor(0,0,0))

        pen = qg.QPen(qc.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        
        painter.drawText(self.rect(), qc.Qt.AlignTop, "{0}".format(self.text()))
        painter.translate(center)
        painter.drawRoundedRect(qc.QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(qg.QBrush(bg_color))
        sw_rect = qc.QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, qc.Qt.AlignCenter, label)