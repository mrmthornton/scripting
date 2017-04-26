# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        Access_LIB.py
# Purpose:     A library for Microsoft Access functions.
#              extracted from ToAccess.py
# Author:      mthornton
#
# Created:     2017 APR 26
# Updates:     2017 APR 26
# Copyright:   (c) michael thornton 2017
#-------------------------------------------------------------------------------

import pyodbc
from selenium.webdriver.common.by import By
import string
import time
import tkFileDialog
from Tkinter import Tk

from structures_LIB import txDotDataInit, txDotDataFill, recordInit, ToDbRecord, makeSqlString
from TxDot_LIB import findResponseType, parseRecord, query, repairLineBreaks
from UTIL_LIB import openBrowser, waitForUser
from VPS_LIB import getTextResults, fillFormAndSubmit, findAndClickButton, findAndSelectFrame,\
                    findElementOnPage, findTargetPage, newPageElementFound


def printDbColumnNames(dbcursor):
    rowcount = 0
    while True:
        row = dbcursor.fetchone()
        if row is None:
            break
        rowcount += 1
        print("Plate {}".format(row[0]))
        #print("entire row -->", row)
    print(rowcount)

    for column in dbcursor.columns(table='US State'):
        print(column.column_name)
    dbcursor.execute('''SELECT Field1
                        FROM [US State]''')
    while True:
        row = dbcursor.fetchone()
        if row is None:
            break
        print("entire row -->{}").format(row[0])


def ConnectToAccessFile():
        #Prompt the user for db, create connection and cursor.
        root = Tk()
        dbname = tkFileDialog.askopenfilename(parent=root, title="Select database",
                    filetypes=[('locked', '*.accde')])
                    #filetypes=[('locked', '*.accde'), ('normal', '*.accdb')])
        root.destroy()
        # Connect to the Access database
        connectedDB = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+dbname+";")
        dbcursor=connectedDB.cursor()
        print("ConnectToAccessFile: Connected to {}".format(dbname))
        return connectedDB, dbcursor

if __name__ == '__main__':
    databaseName, cursor = ConnectToAccessFile()
    print("Access_LIB:main: database name ", databaseName)
    printDbColumnNames(cursor)
    print("Access_LIB:main: DONE ")

# 'd' Signed integer decimal.
# 'i' Signed integer decimal.
# 'o' Signed octal value.
# 'u' Obsolete type – it is identical to 'd'.
# 'x' Signed hexadecimal (lowercase).
# 'X' Signed hexadecimal (uppercase).
# 'e' Floating point exponential format (lowercase).
# 'E' Floating point exponential format (uppercase).
# 'f' Floating point decimal format.
# 'F' Floating point decimal format.
# 'g' Floating point format. Uses lowercase exponential format or decimal format
# 'G' Floating point format. Uses uppercase exponential format or decimal format
# 'c' Single character (accepts integer or single character string).
# 'r' String (converts any Python object using repr()).
# 's' String (converts any Python object using str()).
# '%' No argument is converted, results in a '%' character in the result.

