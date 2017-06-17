# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        TxViosOOS.py
# Purpose:     Share Texas DMV information with out of state Toll Authorities.
#
# Author:      mthornton
#
# Created:     2017 JUN 08
# Modified:    2017 JUN 16
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

def setParameters():
    parameters = {
    'delay' : 15,
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    #'url' : 'http://intranet/SitePages', # initial URL
    'operatorMessage' : "",
    'inputLocator' : (By.XPATH, '//input[@id = "P_LIC_PLATE_NBR"]'),
    'staleLocator' : (By.XPATH,'//h1[contains(text(),"Violation Search")]'),
    'staleLocator2' : (By.XPATH,'//h1[contains(text(),"Violation Search Result")]'),
    'buttonLocator' : (By.XPATH,'//input[@value="Query"]'),
    'frameParamters' : {'useFrames' : True, 'frameLocator' : (By.XPATH, '//frame[@name="fraRxL"]') },
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : 'Violation Search Results',
    'outputLocator' : (By.XPATH,'//BODY/P[contains(text(),"Record")]'),
    'resultIndexParameters' : {'regex' : "Records \d+ to \d+ of (\d+)", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : '',
    'dataOutFileName' : '',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters


def excelDataFill(csvRecord):
    #       0          1     2     3    4   5      6     7         8             9         10      11
    # responseType, plate, name, addr, '', city, state, zip, ownedStartDate, startDate, endDate, issued
        return [
            'first',
            csvRecord[2],
            csvRecord[3],
            csvRecord[5],
            csvRecord[6],
            csvRecord[7],
            ]


def commonCode(lpList):
    if txdotBool:
        txDriver = openBrowser('http://mvinet.txdmv.gov/mvdi/mvdi.html')
        #txDriver = openBrowser('https://ssoextprd.txdmv.gov/sso/UI/Login?goto=http%3A%2F%2Fmvinet.txdmv.gov%2Fmvdi%2Fmvdi.html')
        waitForUser('enter credentials for DMV and navigate to single plate inquiry')

    try:
        recordArray = []
        for cell in lpList:
            cell = str(cell).upper()
            if cell is None or cell == "NONE":
                print "main() : Finished, no more LP's ."
                break
            if cell == '#':
                continue
            plateString = cell.strip()


            if txdotBool:
                #TXDOT section   *****************************************************************
                results = query(txDriver, delay, plateString)
                DMVtext = results[0]
                DMVplate = results[1]
                if DMVtext is not None:
                    #print results # for debug
                    fileString = repairLineBreaks(DMVtext)
                    #fileString = repairLineBreaks([0])
                    #remove non-ascii
                    ##fileString = "".join(filter(lambda x:x in string.printable, fileString))
                foundCurrentPlate = False
                recordList = []
                while True:
                    try:
                        responseType, startNum, endNum = findResponseType(DMVplate, fileString)
                    except:
                        responseType = None
                        if foundCurrentPlate == False:
                            print plateString, DMVplate, 'commonCode: Plate/DMVplate not found. Unable to resolve record type.'
                            recordList.append("unknown record type",'','','','','','','','','','','','','','','','')
                            #time.sleep(3)
                        #break
                    if responseType != None: # there must be a valid text record to process
                        foundCurrentPlate = True
                        #print 'main:', responseType, startNum, endNum # for debug
                        typeString = fileString[startNum:endNum + 1]
                        #print typeString # for debug
                        fileString = fileString[:startNum] + fileString[endNum + 1:] # what is this for ?
                        listData = parseRecord(responseType, typeString)
                        # make txdot data record here
                        recordList.append(listData) # more than one record MAY be returned
                         #print listData # for debug
                        assert(len(listData)==12 or len(listData)==17)

            if not txdotBool:
                recordList = [['response type', 'plate', 'name', 'addr', 'addr2', 'city', 'state', 'zip',\
                              'ownedStartDate', 'startDate', 'endDate', 'issued']]
            if excelBool:
                # excel section   *****************************************************************
                for singleList in recordList:
                    excelVector = excelDataFill(singleList)
                    recordArray.append(excelVector)
                xlwings.Range((2,1)).value = recordArray



# from TxDot lib --> ['response type', 'plate', 'name', 'addr', 'addr2', 'city', 'state', 'zip', 'ownedStartDate', 'startDate', 'endDate', 'issued']
    finally:
        if dbBool:
            print("Closing databases")
            dbConnect.close()
        if vpsBool:
            driver.close() # close browser window
            driver.quit()  # close command (cmd) window
            resultBlock = results
        if txdotBool:
            #txDriver.close()
            txDriver.quit()
    return recordArray


def excelHook():
    firstRow = 2
    indexList = range(firstRow, NUMBERtoProcess + firstRow)
    rawPlatesCol = [str( xlwings.Range((i,7)).value) for i in indexList] # skip the non-lp chars
    plates = [plate[9:] for plate  in rawPlatesCol if plate != 'None' and plate != ""]
    #l = len(plates); #print l, plates
    excelRecord = commonCode(plates) # common code is used by all modules (in theory), with switches for VPS, TXDOT, Excel, database(db).
    #print("excelHook, full record: ", excelRecord) # for debug
    # field name-> type, plate, combined_name, address, city, state, zip, ownedStartDate, start_date, end_date
    ##xlwings.Range((2,2)).value = excelRecord


# global costants
NUMBERtoProcess = 5
vpsBool   = False # true when using VPS images
txdotBool = True  # true when using DMV records
excelBool = True  # true when using excel
dbBool    = False # true when using access file
findWindowDelay = 1
SLEEPTIME = 0 #180
delay=10
parameters = setParameters()
parameters['operatorMessage'] = "Use debug mode, \n open VPS, new violator search window, \n open DMV window, \n run to completion"
#print parameters['operatorMessage']


if __name__ == '__main__':
    excelHook()
    #commonCode(['ccy0042','dsv9060','notReal','letterO']) # for test purposes


