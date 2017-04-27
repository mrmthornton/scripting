# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        ToAccess.py
#              do one loop every N min to simulate human interaction
# Purpose:     Read LP from a DB, gather TxDot info, if any, and combine with
#              other input to form a complete record, write record to the DB.
#              Commit a record before gathering more info.
#
# Author:      mthornton
#
# Created:     2016 AUG 12
# Update:      2017 APR 26
# Copyright:   (c) mthornton 2016, 2017
# educational snippits thanks to Tim Greening-Jackson
# (timATgreening-jackson.com)
#-------------------------------------------------------------------------------


import pyodbc
from selenium.webdriver.common.by import By
import string
import time
import tkFileDialog
from Tkinter import Tk

from Access_LIB import ConnectToAccess, duplicateKey
from structures_LIB import txDotDataInit, txDotDataFill, recordInit, ToDbRecord, makeSqlString
from TxDot_LIB import findResponseType, parseRecord, query, repairLineBreaks
from UTIL_LIB import openBrowser, waitForUser
from VPS_LIB import getTextResults, fillFormAndSubmit, findAndClickButton, findAndSelectFrame,\
                    findElementOnPage, findTargetPage, newPageElementFound


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


if __name__ == '__main__':

    NUMBERtoProcess = 20
    vpsBool = False
    txBool = True
    dbBool = True
    delay=10
    SLEEPTIME = 0 # seconds 180 for standard time delay
    parameters = setParameters()
    parameters['operatorMessage'] = "Use debug mode, \n open VPS, new violator search window, \n open DMV window, \n run to completion"
    print(parameters['operatorMessage'])
    if txBool:
        txDriver = openBrowser('https://mvinet.txdmv.gov')
        waitForUser('enter DMV credentials,\nnavigate to single entry page.')
    if vpsBool:
        driver = openBrowser(parameters['url'])
        waitForUser('login to VPS,\nopen violator maintenance')
    try:
        # Database Read section   *****************************************************************
        if dbBool:
            dbConnect, dbcursor = ConnectToAccess()
            #for row in dbcursor.columns(table='Sheet1'): # debug
            #    print(row.column_name)                   # debug
            dbcursor.execute("SELECT plate FROM [list of plate 8 without matching sheet1]") # (1),4,8,9,10, '11'  ,12
            #dbcursor.execute("SELECT plate FROM [list of plates 5 without matching sheet1]") # 2,3,5,6,7
            lpList = []
            loopCount = 0
            while loopCount< NUMBERtoProcess:
                lpRecord = dbcursor.fetchone()
                if lpRecord is None:
                    print("main() : Finished, no more input records.")
                    break
                lpList.append(lpRecord)
                loopCount += 1

            for row in lpList:
                if row is None:
                    print("main() : Finished, no more LP's .")
                    break
                plateString = str(row[0])

                #VPS section   *****************************************************************
                if vpsBool:
                    startPageTextLocator = (By.XPATH, '//TD/H1[contains(text(),"Violation Search")]')
                    # pause on next line for entry of credentials, and window navigation.
                    ##startWindow = findTargetPage(driver, delay, startPageTextLocator, "mainframe")
                    startWindow = findTargetPage(driver, delay, startPageTextLocator)
                    if startWindow is None:
                        print("main: Start Page not found.")
                        raise ValueError("main: Start Page not found.", startPageTextLocator)
                    element = findElementOnPage(driver, delay, parameters['inputLocator'])
                    submitted = fillFormAndSubmit(driver, startWindow, element, plateString, parameters) # why so slow?  IeDriver64 ??
                    time.sleep(1)  #page may not be there yet!  how long to wait?
                    pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['staleLocator2'])
                    foundFrame = findAndSelectFrame(driver, delay, "fraRL")
                    #time.sleep(1)  #text may not be there yet!  how long to wait?
                    text = getTextResults(driver, delay, plateString, parameters, "fraRL")
                    if text is not None: # if there is text, process it
                        ##stdout.write("Initial # of " + plateString + ", " + str(text) + '\n')
                        startNum = int(str(text))
                        # insert orm to wait for user input
                        # navigate to search position
                        if type(parameters['buttonLocator']) is None: # no button, start at 'top' of the page
                            driver.switch_to_default_content()
                        else: # there is a button. find it/click it/wait for page to load
                            clicked = findAndClickButton(driver, delay, parameters)
                            pageLoaded = newPageElementFound(driver, delay, None, parameters['staleLocator'])
                        submitted = fillFormAndSubmit(driver, startWindow, element, plateString, parameters) # why so slow?  IeDriver64 ??
                        time.sleep(1)  #page may not be there yet!  how long to wait?
                        pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['staleLocator2'])
                        foundFrame = findAndSelectFrame(driver, delay, "fraRL")
                        #time.sleep(1)  #text may not be there yet!  how long to wait?
                        text = getTextResults(driver, delay, plateString, parameters, "fraRL")
                        endNum = int(str(text))
                        diffNum = startNum - endNum
                        print( startNum, endNum, diffNum)
                    # navigate to search position
                    if type(parameters['buttonLocator']) is None: # no button, start at 'top' of the page
                        driver.switch_to_default_content()
                    else: # there is a button. find it/click it/wait for page to load
                        clicked = findAndClickButton(driver, delay, parameters)
                        pageLoaded = newPageElementFound(driver, delay, None, parameters['staleLocator'])


                #TXDOT section   *****************************************************************
                if txBool:
                    text, DMVplate  = query(txDriver, delay, plateString)  # TODO remove unprintable chars
                    if text is not None:
                        cleanText = "".join(filter(lambda x:x in string.printable, text)) # TODO move to query
                        fileString = repairLineBreaks(cleanText)  # TODO remove non-ascii  TODO move to query
                        ##fileString = "".join(filter(lambda x:x in string.printable, fileString))
                    foundCurrentPlate = False
                    recordList = []
                    while True:
                        try:
                            responseType, startNum, endNum = findResponseType(DMVplate, fileString)
                        except:
                            responseType = None
                            if foundCurrentPlate == False:
                                print(DMVplate, ' Plate/Pattern not found. Unable to resolve record type.')
                                time.sleep(3)
                            break
                        if responseType != None: # there must be a valid text record to process
                            foundCurrentPlate = True
                            #print('main:', responseType, startNum, endNum) # for debug
                            typeString = fileString[startNum:endNum + 1]
                            #print(typeString) # for debug
                            fileString = fileString[:startNum] + fileString[endNum + 1:] # what is this for ?
                            listData = parseRecord(responseType, typeString)
                            assert(len(listData)==17)
                            recordList.append(listData)
                            #print(listData) # for debug
                else:
                    recordList = [
['STANDARD',   plateString,    'name',  'addr',  'addr2',  'city',  'state',  '75000', '1/1/2000', '1/3/2000', '1/4/2000', '1/2/2000','2000','NISS','AC','4D','vin'],
['SPECIAL',   'C'+plateString, 'name',  'addr',  'addr2',  'city',  'state',  '75000', '',         '1/3/2000', '1/4/2000', '1/2/2000','2000','NISS','AC','4D','vin'],
['TEMPORARY', 'T'+plateString, 'name2', 'addr2', 'addr22', 'city2', 'state2', '75002', '',         '1/3/2002', '1/4/2002', '',        '2002','BMW', 'AC','2D','vin'],
['DEALER',    'D'+plateString, 'name2', 'addr2', 'addr22', 'city2', 'state2', '75002', '',         '',         '6/1/2017', '',        '',    '',    '',  '',  ''],
['DEALER',    'D'+plateString, 'name2', 'addr2', 'addr22', 'city2', 'state2', '75002', '',         '',         '6/1/2017', '',        '',    '',    '',  '',  ''],
]

#' type',     'plate',         'name',  'addr',  'addr2',  'city',  'state',  'zip',   'Assigned', 'startDate', 'endDate', 'title'    'year', make',modl,body,vin

                # Database Write section   *****************************************************************
                if dbBool:
                    for csvRecord in recordList:
                    #  if DMVplate is in db, skip, if DMVplate is not same as plateString, comment is fix image lable.  TODO
                        #print(recordList) # for debug
                        txDotRecord = txDotDataFill(txDotDataInit(), csvRecord)
                        dbRecord = ToDbRecord(txDotRecord, recordInit())
                        #print(dbRecord) # for debug
                        duplicateFound = duplicateKey(dbcursor, "Sheet1", "Plate", dbRecord["plate"])
                        if duplicateFound:
                            print("ToAccess:main: DUPLICATE FOUND")
                            continue
                        sqlString = makeSqlString(dbRecord)
                        #print(sqlString) # for debug
                        sql = sqlString.format(**dbRecord)
                        #print(sql) # for debug
                        dbcursor.execute(sql)
                    print("Comitting changes")
                    dbcursor.commit()
                    time.sleep(SLEEPTIME)

    except ValueError as e:
        print(e)
    finally:
        print("Closing databases")
        if dbBool:
            dbConnect.close()
        if vpsBool:
            driver.close() # close browser window
            driver.quit()  # quit command shell
        if txBool:
            txDriver.close()
            txDriver.quit()

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

