# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 16:40:00 2020

@author: Derek Joslin
"""

import HapticsEngine as he
import HapticVisualizer as hv
import time

#timing matrices
ts = [[50 for i in range(0,20)] for j in range(0,20)]

th = [[100 for i in range(0,20)] for j in range(0,20)]

tpw = [[50 for i in range(0,20)] for j in range(0,20)]


def display_matrix(matrix,number):
    print('time: {0}'.format(number))
    print('---------------------------\n\r')
    print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                 for row in matrix]))

engine = he.HapticsEngine(tpw, th, ts, 15, 14, 'row by row')
#engine.establish_connection("COM4")
engine.ge.write_braille((0,0), "TEST")
#engine.ge.make_circle((7,7), 15, 1, 1)
#engine.ge.clear()

clock1 = time.perf_counter()
engine.quick_refresh()
display_matrix(engine.get_currentState(),0)
engine.send_toBoard()
clock1 = time.perf_counter() - clock1

print(clock1)
#engine.end_connection()
