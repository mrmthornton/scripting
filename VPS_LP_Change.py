#-------------------------------------------------------------------------------
# Name:        VPS_LP_Change.py
# Purpose:     Examine
#              enter a licence plate and state
#              find uninvoiced images
#              write the correct lable
#
# Author:      mthornton
#
# Created:     2015 AUG 01
# Updates:     2017 APR 21
# Copyright:   (c) michael thornton 2015,2016, 2017
# input(s):    (see parameters, dataInFileName)
# output(s):   (see parameters, dataOutFileName)
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import selenium.webdriver.support.expected_conditions as EC

from VPS_LIB import fillFormAndSubmit, findAndClickButton, findAndSelectFrame, findElementOnPage, findTargetPage, getTextResults, newPageElementFound
from UTIL_LIB import cleanUpString, openBrowser, waitForUser

from VPS_State_Change import changeLP, changeStateOnly

import re
import io
import csv
import sys
import string
import time

import datetime
import pyodbc
import string
import tkFileDialog # python 2
#from tkinter import filedialog, messagebox # python 3
import tkMessageBox # python 2
import xlwings

def setParameters():
    parameters = {
    'delay' : 15,
    'findStartWindowDelay' : 15,
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    'operatorMessage' : "Open VPS violator search window, and run to completion",
    'inputLpLocator' : (By.XPATH, '//input[@id = "P_LIC_PLATE_NBR"]'),
    'inputStateLocator' : (By.XPATH, '//select[@id = "P_LIC_PLATE_STATE"]'),
    'LpLocator' : (By.XPATH, '//td[@id = "LIC_PLATE_NBR1"]'),
    'staleLocator' : (By.XPATH,'//h1[contains(text(),"Violation Search")]'),
    'pageLocator2' : (By.XPATH,'//h1[contains(text(),"Violation Search Result")]'),
    'buttonLocator' : (By.XPATH,'//input[@value="Query"]'),
    'frameParamters' : {'useFrames' : True, 'frameLocator' : (By.XPATH, '//frame[@name="fraRxL"]') },
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : 'Violation Search Results',
    'outputLocator' : (By.XPATH,'//BODY/P[contains(text(),"Record")]'),
    'resultIndexParameters' : {'regex' : "Records \d+ to \d+ of (\d+)", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'VPS_LP_Change_list.csv',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters


def common_code(driver, parameters, plates):
    delay = parameters['delay']
    startPageTextLocator = (By.XPATH, '//TD/H1[contains(text(),"Violation Search")]')
    startWindow = findTargetPage(driver, parameters['findStartWindowDelay'], startPageTextLocator)
    if startWindow is None:
        print("Start Page not found.")
        return None

    for row in plates:
        wrongPlate = row[0]; wrongState = row[1]; correctPlate = row[2]; correctState = row[3]
        # minimum requirements  wrongPlate, and  (correctPlate or correctState)
        if wrongPlate is None or (correctPlate is None and correctState is None):
            print("VPS_LP_Change:common_code: The Minimum requirements are not met.")
            break

        wrongPlate = cleanUpString(wrongPlate)
        wrongState = cleanUpString(wrongState)
        correctPlate = cleanUpString(correctPlate)
        correctState = cleanUpString(correctState)

        #select a type of violation from the Violation Status menu
        menuLocator = (By.XPATH, '//select[@name="P_L_VST_VIOL_STATUS_DESCR"]')
        menuElement = findElementOnPage(driver, delay, menuLocator)
        Selector = Select(menuElement)
        count = 0
        while Selector is None:  # menu select is sometimes None, why ?
            count = count + 1
            print("retrying excusal menu selection. Count: ", count)
            Selector = Select(menuElement)
        Selector.select_by_visible_text("ZipCash; Uninvoiced") # does this need to be instanciated each time?
        #Selector.select_by_visible_text("Excused") # does this need to be instanciated each time?

        element = findElementOnPage(driver, delay, parameters['inputLpLocator'])
        submitted = fillFormAndSubmit(driver, startWindow, element, wrongPlate, parameters) # why so slow?
        time.sleep(1)  #page may not be there yet!  how long to wait?
        pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['pageLocator2'])

        if wrongPlate == correctPlate: # if the plate is the same, change only the state
            changeStateOnly(driver, delay, parameters, startWindow, wrongPlate, correctPlate, correctState)
        else:
            changeLP(driver, delay, parameters, startWindow, wrongPlate, correctPlate, correctState)

        handle = driver.current_window_handle  # what do these four lines do?
        driver.switch_to_window(handle)
        foundFrame = findAndSelectFrame(driver, delay, "fraRL")
        clicked = findAndClickButton(driver, delay, parameters)

            # click the query button.
        #test with multiple plate changes

    print("main: Finished with LP_correction file.")


def openRunClose(plates):
    parameters = setParameters()
    parameters['findStartWindowDelay'] = 3
    print(parameters['operatorMessage'])
    #regexPattens = loadRegExPatterns()
    driver = openBrowser(parameters['url'])
    waitForUser()
    common_code(driver, parameters, plates)
    driver.close()
    driver.quit()


def excelEntryPoint():
    startRow = 3
    startCol = 1
    endRow = startRow + NUMBERtoProcess
    endCol = 5
    #inputArray = [str( xlwings.Range((i,1)).value ) for i in indexList]
    #inputArray = xlwings.Range('A3:E7').options(ndim=2).value
    inputArray = xlwings.Range((startRow,startCol),(endRow,endCol)).options(ndim=2).value
    plates = []
    #[plates.append([str(e) for  e in plate]) for plate  in inputArray if plate[0] != 'None' and plate[0] != ""]
    [plates.append(elem[0:4]) for elem  in inputArray if elem[0] is not None and elem[0] != ""]
    # test the plate array for empty strings or zeros (0),  TODO
    #l = len(plates) ; print(l, plates)
    excelRecord = openRunClose(plates)
    #print(excelRecord) # debug
    # field name-> type, plate, combined_name, address, city, state, zip, ownedStartDate, start_date, end_date
    ##xlwings.Range((2,2)).value = excelRecord # example of writing


# global costants
NUMBERtoProcess = 20
vpsBool   = False # true when using VPS images
txdotBool = False # true when using DMV records
excelBool = False # true when using excel
dbBool    = False # true when using access file
findWindowDelay = 1
SLEEPTIME = 0 #180
delay=10

if __name__ == '__main__':
    excelEntryPoint()
