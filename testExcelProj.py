import xlwings as xw

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
def main():
    plate = xw.Range('A1').value
    xw.Range('B1').value = plate
    #xw.Range('B1').value
