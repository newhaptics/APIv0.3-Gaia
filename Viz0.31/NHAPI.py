# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:43:20 2020

@author: Derek Joslin
"""

import HapticsEngine as he
import time


#timing matrices
ts = [[500 for i in range(0,20)] for j in range(0,20)]

th = [[1000 for i in range(0,20)] for j in range(0,20)]

tpw = [[500 for i in range(0,20)] for j in range(0,20)]

state = [[1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
         [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
         [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, ],
         [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, ],
         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
         [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, ],
         [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, ],
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, ],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]]


#create the backend haptics engine
engine = he.HapticsEngine(tpw,th,ts, 15, 14, 'row by row')
#engine.set_desiredState(state)
full = 0
width = 1
update = 0
times = 0



def boardControl():
    global update
    if update:
        engine.quick_refresh()
    if engine.check_connection():
        engine.send_toBoard()

def display_matrix(matrix,number):
    print('---------------------------\n')
    print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                     for row in matrix]))
    print('---------------------------\n')


def erase(onOff):
    if onOff == "on":
        engine.ge.set_output(False)
        print("erase on")
    else:
        engine.ge.set_output(True)
        print("erase off")

def fill(onOff):
        global full
        if onOff == "on":
            full = 1
            print("fill on")
        else:
            full = 0
            print("fill off")

def direct(onOff):
    global update
    if onOff == "on":
        update = 1
        print("direct on")
    else:
        update = 0
        print("direct off")

def stroke(size):
    global width
    print("stroke is {0}".format(size))
    width = size

def settings():
    global full
    global width
    global update
    print("fill setting {0}".format(full))
    print("stroke setting {0}".format(width))
    print("direct setting {0}".format(update))
    print("connection setting {0}".format(engine.check_connection()))


def dot(coord):
    engine.ge.select_element(coord)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def line(start, end):
    engine.ge.make_line(start, end, width)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def curve(start, control1, control2, end):
    engine.ge.make_bezierCurve(start, control1, control2, end, width)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def circle(center, radius):
    engine.ge.make_circle(center, radius, width, full)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def rect(corner1, corner2):
    engine.ge.make_rectangle(corner1, corner2, width, full)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def triangle(point1, point2, point3):
    engine.ge.make_polygon(point1, [point2, point3], width, full)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def polygon(points):
    engine.ge.make_polygon(points[0], points[1:-1], width, full)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def braille(point, text):
    engine.ge.write_braille(point, text)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def latin(point, text, font, size):
    engine.ge.write_latin(point, text, font, size)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def clear():
    engine.ge.clear()
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    boardControl()

def state():
    print("current state \n")
    display_matrix(engine.get_currentState(), 0)
    return engine.get_currentState()

def desired():
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    return engine.get_desiredState()

def refresh():
    global times
    times = engine.generate_refreshStates()
    clock2 = time.perf_counter()
    elapsed_time = 0
    for now in times:
        while elapsed_time != now:
            elapsed_time = round((time.perf_counter() - clock2)*1000)
        else:
            engine.set_stateTime(now)
            print("state at {0} milliseconds".format(now))
            display_matrix(engine.get_currentState(), now)
    clock2 = time.perf_counter() - clock2
    print(clock2)
    if engine.check_connection():
        engine.send_toBoard()

def setMat(mat):
    engine.set_desiredState(mat)
    boardControl()

def quickRefresh():
    engine.quick_refresh()
    if engine.check_connection():
        engine.send_toBoard()

def times(now):
    engine.set_stateTime(now)
    display_matrix(engine.get_currentState(), now)
    boardControl()

def frames():
    print(times)

def connect(COM, *args):
    if len(args) > 0:
        engine.establish_connection(COM, 1)
    else:
        engine.establish_connection(COM, 0)

def disconnect():
    engine.end_connection()
