# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 12:34:51 2020

@author: Derek Joslin
"""

from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
import qrc_resources
import numpy as np
import NHAPI as nh

from pyqtconsole.console import PythonConsole
import pyqtconsole.highlighter as hl
import string




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
    def __init__(self, state):
        """
        reads in a list of the current FC state. displays that state of 1s and 0s in a matrix of png images
        if val is a one, that element in the table reads in the raised image png. If the element is a zero that element reads in the
        lowered image png.
        """
        super().__init__()
        self.state = stateMat(state)
        self.setModel(self.state)





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




#GUI object for function selection
class vizWindow(qw.QMainWindow):
    """ Window that holds all the operation functions """

    def __init__(self, parent = None):
        super().__init__(parent)
        FCIcon = qg.QIcon(":main_symbol")
        HELogo = qg.QPixmap(":HE_logo")
        HELogo = HELogo.scaled(175,175,qc.Qt.KeepAspectRatio)

# =============================================================================
#         style guide
#         rgb(85,216,211) -> light turquoise
#         rgb(41,178,170) -> dark turquoise
#         rgb(37,64,143) -> reflex blue
#         rgb(65,67,77) -> persian nights
# =============================================================================


        #create window
        self.setWindowTitle("FC Lab operation functions")
        self.setWindowIcon(FCIcon)
# =============================================================================
#         self.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
#                             "font-family : Comfortaa;"
#                             "color: rgb(255,255,245);"
#                             "font-size: 13px;"
#                             "background-color: rgb(85,216,211);"
#                             "selection-color: rgb(65,67,77);"
#                             "selection-background-color: rgba(37,64,143, 10%);" ))
# =============================================================================


        #create status bar with the status and haptic engine ad
        self.statusBar = qw.QStatusBar()
        self.setStatusBar(self.statusBar)


        self.HEad = qw.QLabel()
        self.HEad.setPixmap(HELogo)
        self.centralWidget = qw.QLabel("Hello World")
        self.pwr = qw.QLabel("POWERED BY")
        self.statusBar.addWidget(self.centralWidget,30)
        self.statusBar.addWidget(self.pwr)
        self.statusBar.addWidget(self.HEad)

# =============================================================================
#         self.statusBar.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
#                             "font-family : Comfortaa;"
#                             "color: rgb(255,255,245);"
#                             "font-size: 18px;"
#                             "background-color: rgb(41,178,170);"
#                             "selection-color: rgb(65,67,77);"
#                             "selection-background-color: rgba(37,64,143, 10%);" ))
# =============================================================================


        #console creation
        self.console = guiConsole()
        self.console.setMaximumWidth(900)
        self.console.interpreter.exec_signal.connect(lambda: self.__updateDocks())

# =============================================================================
#         self.console.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
#                             "font-family : Comfortaa;"
#                             "color: rgb(255,255,245);"
#                             "font-size: 18px;"
#                             "background-color: rgb(85,216,211);"
#                             "selection-color: rgb(65,67,77);"
#                             "selection-background-color: rgba(37,64,143, 10%);" ))
# =============================================================================

        #create state views
        self.currentView = displayMat(nh.engine.get_currentState())
        self.desiredView = displayMat(nh.engine.get_desiredState())
        self.currentDock = qw.QDockWidget("current state", self, qc.Qt.Widget)
        self.currentDock.setWidget(self.currentView)
        self.desiredDock = qw.QDockWidget("desired state", self, qc.Qt.Widget)
        self.desiredDock.setWidget(self.desiredView)

# =============================================================================
#         self.currentDock.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
#                             "font-family : Comfortaa;"
#                             "color: rgb(255,255,245);"
#                             "font-size: 18px;"
#                             "background-color: rgb(41,178,170);"
#                             "selection-color: rgb(65,67,77);"
#                             "selection-background-color: rgba(37,64,143, 10%);" ))
# =============================================================================

# =============================================================================
#         self.desiredDock.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
#                             "font-family : Comfortaa;"
#                             "color: rgb(255,255,245);"
#                             "font-size: 18px;"
#                             "background-color: rgb(41,178,170);"
#                             "selection-color: rgb(65,67,77);"
#                             "selection-background-color: rgba(37,64,143, 10%);" ))
# =============================================================================

        #align widgets
        self.setCentralWidget(self.console)
        self.addDockWidget(qc.Qt.LeftDockWidgetArea, self.desiredDock, qc.Qt.Vertical)
        self.addDockWidget(qc.Qt.LeftDockWidgetArea, self.currentDock, qc.Qt.Vertical)
        #self.addDockWidget(qc.Qt.BottomDockWidgetArea, self.labelDock)
        #self.currentView.setAlignment(qc.Qt.AlignTop | qc.Qt.AlignLeft)
        #self.desiredView.setAlignment(qc.Qt.AlignBottom | qc.Qt.AlignLeft)

        #create the command dictionary, parameter dictionary, and coordinate history
        self.__commandDict = {}
        self.__coordHist = [None,None,None,None]
        self.__paramDict = {}

        #create dictionary formatter
        self.__commandFMT = PartialFormatter()



        self.__createActions()
        self.__createMenuBar()
        self.__createToolBars()
        self.__connectControls()

        #resize the state views
        self.desiredView.resizeColumnsToContents()
        self.currentView.resizeColumnsToContents()
        self.desiredView.resizeRowsToContents()
        self.currentView.resizeRowsToContents()


    def flashSplash(self):
        FCLogo = qg.QPixmap(":main_logo")
        FCLogo = FCLogo.scaled(1000,1000)

        self.splash = qw.QSplashScreen(FCLogo)

        # By default, SplashScreen will be in the center of the screen.
        # You can move it to a specific location if you want:
        # self.splash.move(10,10)

        self.splash.show()

        # Close SplashScreen after 2 seconds (2000 ms)
        qc.QTimer.singleShot(1000, self.splash.close)


    def __connectControls(self):
        self.desiredView.clicked.connect(lambda index = self.desiredView.currentIndex: self.__coordSelector((index.row(),index.column())))

    def __createMenuBar(self):
        menuBar = qw.QMenuBar(self)
        self.setMenuBar(menuBar)
        #create menu bars
        #file menu
        fileMenu = qw.QMenu("&File", self)



        #edit menu
        editMenu = qw.QMenu("&Edit", self)
        editMenu.addAction(self.clear)
        editMenu.triggered.connect(lambda: self.executeTool())

        #help menu
        helpMenu = qw.QMenu("&Help", self)
        helpMenu.addAction(self.settings)
        helpMenu.addAction(self.frames)
        helpMenu.triggered.connect(lambda: self.executeTool())

        #control menu
        controlMenu = qw.QMenu("Control",self)
        controlMenu.addAction(self.refresh)
        controlMenu.addAction(self.times)
        controlMenu.addAction(self.setMat)
        controlMenu.triggered.connect(lambda: self.executeTool())


        #board menu
        boardMenu = qw.QMenu("Board", self)
        boardMenu.addAction(self.connect)
        boardMenu.addAction(self.disconnect)
        boardMenu.addAction(self.quickRefresh)
        boardMenu.addAction(self.direct)
        boardMenu.triggered.connect(lambda: self.executeTool())

        #add menu bars
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(helpMenu)
        menuBar.addMenu(controlMenu)
        menuBar.addMenu(boardMenu)


    def __createToolBars(self):
        #cursor Bar
        cursors = qw.QToolBar("cursors", self)
        cursors.addAction(self.erase)
        cursors.addAction(self.fill)
        cursors.addAction(self.stroke)
        self.onOFF = qw.QPushButton("on/off")
        self.onOFF.setCheckable(True)
        self.onOFF.clicked.connect(lambda: self.__optionUpdated("on/off", self.onOFF.isChecked()))
        self.onOFF.setFocusPolicy(qc.Qt.NoFocus)
        cursors.addWidget(self.onOFF)
        self.strokeSize = qw.QSpinBox()
        self.strokeSize.valueChanged.connect(lambda: self.__optionUpdated("stroke size", self.strokeSize.value()))
        self.strokeSize.setFocusPolicy(qc.Qt.NoFocus)
        cursors.addWidget(self.strokeSize)
        cursors.setIconSize(qc.QSize(50,50))
        cursors.setMovable(False)

# =============================================================================
#         cursors.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
#                             "font-family : Comfortaa;"
#                             "color: rgb(255,255,245);"
#                             "font-size: 13px;"
#                             "background-color: rgb(41,178,170);"
#                             "selection-color: rgb(65,67,77);"
#                             "selection-background-color: rgba(37,64,143, 10%);" ))
# =============================================================================

        #shape Bar
        shapes = qw.QToolBar("shapes", self)
        shapes.addAction(self.dot)
        shapes.addAction(self.line)
        shapes.addAction(self.curve)
        shapes.addAction(self.circle)
        shapes.addAction(self.rect)
        shapes.addAction(self.triangle)
        shapes.addAction(self.polygon)
        shapes.setIconSize(qc.QSize(50,50))
        shapes.setMovable(False)

# =============================================================================
#         shapes.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
#                             "font-family : Comfortaa;"
#                             "color: rgb(255,255,245);"
#                             "font-size: 13px;"
#                             "background-color: rgb(41,178,170);"
#                             "selection-color: rgb(65,67,77);"
#                             "selection-background-color: rgba(37,64,143, 10%);" ))
# =============================================================================

        #character Bar
        characters = qw.QToolBar("characters", self)
        characters.addAction(self.braille)
        characters.addAction(self.latin)
        self.fontSize = qw.QSpinBox()
        self.fontSize.setFocusPolicy(qc.Qt.NoFocus)
        self.fontSize.valueChanged.connect(lambda: self.__optionUpdated("font size", self.fontSize.value()))
        characters.addWidget(self.fontSize)
        characters.setIconSize(qc.QSize(50,50))
        characters.setMovable(False)

# =============================================================================
#         characters.setStyleSheet(("border: 1px solid rgba(65,67,77, 100%);"
#                             "font-family : Comfortaa;"
#                             "color: rgb(255,255,245);"
#                             "font-size: 13px;"
#                             "background-color: rgb(41,178,170);"
#                             "selection-color: rgb(65,67,77);"
#                             "selection-background-color: rgba(37,64,143, 10%);" ))
# =============================================================================

        #add tool bars
        self.addToolBar(qc.Qt.TopToolBarArea, cursors)
        self.addToolBar(qc.Qt.LeftToolBarArea, shapes)
        self.addToolBar(qc.Qt.BottomToolBarArea, characters)

    def __createActions(self):
          #create the icons for the tools
        filledIcon = qg.QIcon(":filledPin")
        emptyIcon = qg.QIcon(":emptyPin")
        fillIcon = qg.QIcon(":fill")
        strokeIcon = qg.QIcon(":stroke")
        eraseIcon = qg.QIcon(":erase")
        dotIcon = qg.QIcon(":dot")
        lineIcon = qg.QIcon(":line")
        curveIcon = qg.QIcon(":curve")
        circleIcon = qg.QIcon(":circle")
        rectIcon = qg.QIcon(":square")
        triangleIcon = qg.QIcon(":triangle")
        polygonIcon = qg.QIcon(":polygon")
        brailleIcon = qg.QIcon(":braille")
        latinIcon = qg.QIcon(":text")


        #cursor tools
        self.erase = qw.QAction(eraseIcon, "Erase", self)
        self.erase.triggered.connect(lambda: self.__toolSelected("erase","({on/off})"))
        self.fill = qw.QAction(fillIcon, "Fill", self)
        self.fill.triggered.connect(lambda: self.__toolSelected("fill","({on/off})"))
        self.stroke = qw.QAction(strokeIcon, "Stroke", self)
        self.stroke.triggered.connect(lambda: self.__toolSelected("stroke","({stroke size})"))

        #shape tools
        self.dot = qw.QAction(dotIcon, "Dot", self)
        self.dot.triggered.connect(lambda: self.__toolSelected("dot","({coord1})"))
        self.line = qw.QAction(lineIcon, "Line", self)
        self.line.triggered.connect(lambda: self.__toolSelected("line","({coord2},{coord1})"))
        self.curve = qw.QAction(curveIcon, "Curve", self)
        self.curve.triggered.connect(lambda: self.__toolSelected("curve","({coord4},{coord3},{coord2},{coord1})"))
        self.circle = qw.QAction(circleIcon, "Circle", self)
        self.circle.triggered.connect(lambda: self.__toolSelected("circle","({coord1},{font size})"))
        self.rect = qw.QAction(rectIcon, "Rect", self)
        self.rect.triggered.connect(lambda: self.__toolSelected("rect","({coord2},{coord1})"))
        self.triangle = qw.QAction(triangleIcon, "Triangle", self)
        self.triangle.triggered.connect(lambda: self.__toolSelected("triangle","({coord3},{coord2},{coord1})"))
        self.polygon = qw.QAction(polygonIcon, "Polygon", self)
        self.polygon.triggered.connect(lambda: self.__toolSelected("polygon","({list1})"))

        #character tools
        self.braille = qw.QAction(brailleIcon, "Braille", self)
        self.braille.triggered.connect(lambda: self.__toolSelected("braille","({coord1},{text})"))
        self.latin = qw.QAction(latinIcon, "Latin", self)
        self.latin.triggered.connect(lambda: self.__toolSelected("latin","({coord1},{text})"))

        #control actions
        self.clear = qw.QAction(eraseIcon, "Clear", self)
        self.clear.triggered.connect(lambda: self.__toolSelected("clear","()"))
        self.refresh = qw.QAction("Refresh", self)
        self.refresh.triggered.connect(lambda: self.__toolSelected("refresh","()"))
        self.times = qw.QAction("Times", self)
        self.times.triggered.connect(lambda: self.__toolSelected("times","({now})"))
        self.setMat = qw.QAction("Set Matrix", self)
        self.setMat.triggered.connect(lambda: self.__toolSelected("setMat","({matrix})"))

        #board actions
        self.connect = qw.QAction("Connect", self)
        self.connect.triggered.connect(lambda: self.__toolSelected("connect","({com})"))
        self.disconnect = qw.QAction("Disconnect", self)
        self.disconnect.triggered.connect(lambda: self.__toolSelected("disconnect","()"))
        self.quickRefresh = qw.QAction("Quick Refresh", self)
        self.quickRefresh.triggered.connect(lambda: self.__toolSelected("quickRefresh","()"))
        self.direct = qw.QAction("Direct", self)
        self.direct.triggered.connect(lambda: self.__toolSelected("direct", "()"))

        #help actions
        self.settings = qw.QAction("Settings", self)
        self.settings.triggered.connect(lambda: self.__toolSelected("settings","()"))
        self.frames = qw.QAction("Frames", self)
        self.frames.triggered.connect(lambda: self.__toolSelected("frames","()"))

    def __coordSelector(self, index):

        #only log a coord if coordinates are in the parameters
        coordList = [key for key, value in self.__paramDict.items() if 'coord' in key.lower()]
        print(coordList)
        print(len(coordList))
        if len(coordList) != 0:
            #create a list of coordinates up to 50 long
            self.__coordHist.append(index)
            while len(self.__coordHist) > 50:
                self.__coordHist.pop(0)
            #assign the dynamic parameter coordinates
            else:
                self.__coordUpdater(index)

            self.centralWidget.setText("<b>coordinate is ({0},{1})".format(index[0],index[1]))
            self.processCommand()

        else:
            self.centralWidget.setText("<b>coordinate is ({0},{1})".format(index[0],index[1]))


    def __coordUpdater(self, newCoord):
        #create a dictionary of just the coordinate parameters
        coordDict = {key: value for key, value in self.__paramDict.items() if 'coord' in key.lower()}
        #create the assign order of the dictionary (so coord3 = coord2, coord2 = coord1... and so forth)
        assignOrder = [i + 1 for i in range(1,len(coordDict))][::-1]
        for i in range(0,len(coordDict) - 1):
            coordDict["coord{0}".format(assignOrder[i])] = coordDict["coord{0}".format(assignOrder[i] - 1)]
        coordDict["coord1"] = newCoord
        self.__paramDict.update(coordDict)


    def __optionUpdated(self, param, value):
        if value == True and not type(value) == int:
            value = '"on"'
        elif value == False and not type(value) == int:
            value = '"off"'
        self.__paramDict[param] = value
        self.centralWidget.setText("<b>{0} is {1}".format(param,value))



        #process the command when an option changes
        self.processCommand()


    def __toolSelected(self, tool, parameters):
        self.__commandDict["parameters"] = parameters
        self.__commandDict["command"] = tool
        #dynamically populate the parameter Dictionary with the parameters
        self.__assignParam(parameters)
        self.centralWidget.setText("<b>{command} selected with {parameters} parameters".format(**self.__commandDict))
        self.consoleFill()


    def processCommand(self):
        #if the string formats without errors then execute otherwise display
        parameters = self.__commandFMT.format(self.__commandDict["parameters"],**self.__paramDict)
        if parameters.find("~~") == -1:
            print("execute tool executed with {0}".format(parameters))
            self.executeTool()
        else:
            print("console fill executed with {0}".format(parameters))
            self.consoleFill()


    def consoleFill(self):
        self.console.clear_input_buffer()
        #format the parameters with values
        parameters = self.__commandFMT.format(self.__commandDict["parameters"],**self.__paramDict)
        commandStr = "{0}{1}".format(self.__commandDict["command"], parameters)
        self.console.insert_input_text(commandStr)



    def executeTool(self):
        #self.desiredView.state.layoutAboutToBeChanged.emit()
        #self.currentView.state.layoutAboutToBeChanged.emit()
        self.console.clear_input_buffer()
        parameters = self.__commandFMT.format(self.__commandDict["parameters"],**self.__paramDict)
        commandStr = "{0}{1}".format(self.__commandDict["command"], parameters)
        self.console.insert_input_text(commandStr)
        self.console.process_input(self.console.input_buffer())
        self.centralWidget.setText("<b>{0} was executed".format(commandStr))
        self.__updateDocks()
        #once the tool has been executed clear the previous command
        self.__clearParam()

    def __updateDocks(self):
        self.desiredView.state.layoutChanged.emit()
        self.currentView.state.layoutChanged.emit()
        #self.desiredView.update()
        #self.currentView.update()
# =============================================================================
#         self.currentDock.show()
#         self.desiredDock.show()
#         self.labelDock.show()
# =============================================================================


    def __assignParam(self, parameters):
        #replace all the invalid characters inside the string
        parameters = parameters.replace(")","")
        parameters = parameters.replace("(","")
        parameters = parameters.replace("{","")
        parameters = parameters.replace("}","")
        #create the list of keys
        keyList = parameters.split(",")
        #create the None list
        noneList = [None for i in range(0,len(keyList))]
        #merge into paramDict using Dictionary comprehension
        self.__paramDict = {keyList[i]: noneList[i] for i in range(len(noneList))}

    def __clearParam(self):
        self.__paramDict = {}

    def __clearCommand(self):
        self.__commandDict = {}


class PartialFormatter(string.Formatter):
    def __init__(self, missing='~~', bad_fmt='!!'):
        self.missing, self.bad_fmt=missing, bad_fmt

    def get_field(self, field_name, args, kwargs):
        # Handle a key not found
        try:
            val=super(PartialFormatter, self).get_field(field_name, args, kwargs)
            # Python 3, 'super().get_field(field_name, args, kwargs)' works
        except (KeyError, AttributeError):
            val=None,field_name
        return val

    def format_field(self, value, spec):
        # handle an invalid format
        if value==None: return self.missing
        try:
            return super(PartialFormatter, self).format_field(value, spec)
        except ValueError:
            if self.bad_fmt is not None: return self.bad_fmt
            else: raise
