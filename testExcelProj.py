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
    for i in range(1,10):
        plate = xw.Range((i,1)).value
        xw.Range((i,2)).value = plate
#    for plate in plates:
#        strPlate = str(plate)
#        xw.Range('B2').value = strPlate

if __name__ == '__main__':
    world()