# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        combinedNames.py
# Purpose:     parse a name field for first, last, or business names
#
# Author:      mthornton
#
# Created:     2017 JUN 20
# Modified:    2017 JUN 20
# Copyright:   (c) mthornton 2017
#-------------------------------------------------------------------------------


import datetime
import pyodbc
from selenium.webdriver.common.by import By
import string
import tkFileDialog
import tkMessageBox
import time
#python 3 ? #from tk import tkFileDialog
import tkFileDialog
from Tkinter import Tk
from TxDot_LIB import query, repairLineBreaks, findResponseType, parseRecord
from UTIL_LIB import openBrowser, waitForUser
from VPS_LIB import getTextResults
import xlwings



def excelHook(n):
    firstRow = 1
    indexList = range(firstRow, n + firstRow)

#    for element in elems:
#        stringText = filter(lambda x: x in aString.printable, element.text)
#        print stringText
#        ouputFileHandle.write(stringText)

    rawNameCol = [filter(lambda x: x in aString.printable, xlwings.Range((i,1)).value) for i in indexList] # get the first column
    #rawNameCol = [str( xlwings.Range((i,1)).value) for i in indexList] # get the first column
    combinedName = [name for name  in rawNameCol if name != 'None' and name != ""]
    l = len(combinedName); print l, combinedName

    xlwings.Range((2,6)).value = excelRecord



# global costants
NUMBERtoProcess = 5

if __name__ == '__main__':

    excelHook(NUMBERtoProcess)



