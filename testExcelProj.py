#-------------------------------------------------------------------------------
# Name:        testExcel.py
# Purpose:
#
# Author:      mike
#
# Created:     01/12/2016
# Copyright:   (c) mike 2016
#-------------------------------------------------------------------------------

import xlwings as xw
import VPS_LIB

def world():
    plate = xw.Range('A1').value
    xw.Range('A1').value = plate + 1
    xw.Range('B1').value = plate
    #xw.Range('B1').value

if __name__ == '__main__':
    world()