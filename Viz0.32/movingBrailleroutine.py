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


def splitTextToTriplet(string):
    words = string.split()
    grouped_words = [' '.join(words[i: i + 5]) for i in range(0, len(words), 3)]
    return grouped_words

lyrics = "This was a triumph. I'm making a note here: HUGE SUCCESS. It's hard to overstate My satisfaction. Aperture Science We do what we must Because we can. For the good of all of us. Except the ones who are dead. But there's no sense crying Over every mistake. You just keep on trying Till you run out of cake. And the Science gets done. And you make a neat gun. For the people who are Still alive. I'm not even angry. I'm being so sincere right now. Even though you broke my heart. And killed me. And tore me to pieces. And threw every piece into a fire. As they burned it hurt because I was so happy for you! Now these points of data Make a beautiful line. And we're out of beta. We're releasing on time. So I'm GLaD. I got burned. Think of all the things we learned For the people who are Still alive. Go ahead and leave me. I think I prefer to stay inside. Maybe you'll find someone else To help you. Maybe Black Mesa... THAT WAS A JOKE, HA HA, FAT CHANCE. Anyway this cake is great It's so delicious and moist Look at me still talking when there's Science to do When I look out there It makes me GLaD I'm not you I've experiments to run There is research to be done On the people who are Still alive. And believe me I am still alive I'm doing science and I'm still alive I feel FANTASTIC and I'm still alive While you're dying I'll be still alive And when you're dead I will be still alive Still alive Still alive."

#lyrics = lyrics.replace(' ', '\n')

proccessed = splitTextToTriplet(lyrics)

def display_matrix(matrix,number):
    print('time: {0}'.format(number))
    print('---------------------------\n\r')
    print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                 for row in matrix]))

engine = he.HapticsEngine(tpw, th, ts, 15, 14, 'row by row')
#engine.establish_connection("COM4",0)


for word in proccessed:
    engine.ge.write_braille((0,0), word)

    clock1 = time.perf_counter()
    engine.quick_refresh()
    display_matrix(engine.get_currentState(),0)
    #engine.send_toBoard()
    time.sleep(2)
    clock1 = time.perf_counter() - clock1
    engine.ge.clear()
    print(clock1)


#engine.end_connection()