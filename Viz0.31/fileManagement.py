# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 17:35:39 2020

@author: Derek Joslin
"""
import csv
from PIL import Image 
import numpy

def openTxt(filename):
# =============================================================================
#     print(repr(open(filename, 'rb').read(200))) # dump 1st 200 bytes of file
#     data = open(filename, 'rb').read()
#     print(data.find('\x00'))
#     print(data.count('\x00'))
# =============================================================================
    d = {}
    with open(filename, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            d[row[0]] = row[1:]
    return d
    
def openCsv(filename):
# =============================================================================
#     print(repr(open(filename, 'rb').read(200))) # dump 1st 200 bytes of file
#     data = open(filename, 'rb').read()
#     print(data.find('\x00'))
#     print(data.count('\x00'))
# =============================================================================
    d = []
    with open(filename, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            d.append(row)
    return d

def openPng(filename):
    size = (14,15)
    with Image.open(filename) as p:
        print(p.format)
        print(p.mode)
        print(p.size)
        p = p.resize(size,Image.ANTIALIAS)
        pix = (numpy.array(p)).tolist()
        #go through image and convert all lists in list to black and white
        for (i,row) in enumerate(pix):
            for (j,RGB) in enumerate(row):
                if p.mode == "RGBA":
                    if RGB[3] > 100:
                        pix[i][j] = 1
                    else:
                        pix[i][j] = 0
                else:
                    if (sum(RGB)/3) < 250:
                        pix[i][j] = 1
                    else:
                        pix[i][j] = 0
        print(pix)
        return pix
        

def saveCsv(filename, mat):
    
    with open(filename, "w") as f:
        for row in mat:
            for (i,elem) in enumerate(row):
                if elem == True:
                    f.write("{0}".format(1))
                elif elem == False:
                    f.write("{0}".format(0))
                if i is not len(row) - 1:
                    f.write(",")
            f.write("\n")
    f.close()
    
    
