#-------------------------------------------------------------------------------
# Name:        VPS_VioCreate.py
# Purpose:     Find violator page based on VID
#              Extract :LP, State, make, model, body, year
#              Modify the Violator Type, based on user input, Leased, Rented, Sold
#              Enter the end date/time from documents, or based on VID info,
#              if the plate is a temporary.
#
#              Request user input: name(s), address, apt, city, state, zip
#
#              Test for existing Violator, based on LP search, and looking for
#              matching name and address, and date range ?
#              If dne, create vio, with LP, name, addr, Violator Type (based on input type)
#              Enter appropriate comment
#
# Author:      mthornton
#
# Created:     2016 AUG 13
# Updates:     2016 AUG 16
# Copyright:   (c) michael thornton 2016
# input(s):    (see parameters, dataInFileName)
# output(s):   (see parameters, dataOutFileName)
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import selenium.webdriver.support.expected_conditions as EC

from VPS_LIB import *

import re
import io
import csv
import sys
import string
import time

def VPSdataFill(VPSdata, record):
    VPSdata["comment"] = record[0]
    VPSdata["type"] = record[1]
    VPSdata["VID"] = record[2]
    VPSdata["LP"] = record[3]
    VPSdata["LP_ST"] = record[4]
    VPSdata["lessor"] = record[5]
    VPSdata["lessee"] = record[6]
    VPSdata["address"] = record[7]
    VPSdata["address2"] = record[8]
    VPSdata["city"] = record[9]
    VPSdata["state"] = record[10]
    VPSdata["zip"] = record[11]
    VPSdata["startDate"] = record[12]
    VPSdata["startTime"] = record[13]
    VPSdata["endDate"] = record[14]
    VPSdata["endTime"] = record[15]
    VPSdata["make"] = record[16]
    VPSdata["model"] = record[17]
    VPSdata["body"] = record[18]
    VPSdata["year"] = record[19]
    VPSdata["name2"] = record[20]
    VPSdata["leaseDate"] = record[21]
    return VPSdata

def VPSdataInit():
    VPSdata = {
    "comment" : "",
    "type" : "",
    "VID" : "",
    "LP" : "",
    "LP_ST" : "",
    "lessor" : "",
    "lessee" : "",
    "address" : "",
    "address2" : "",
    "city" : "",
    "state" : "",
    "zip" : "",
    "startDate" : "",
    "startTime" : "",
    "endDate" : "",
    "endTime" : "",
    "make" : "",
    "model" : "",
    "body" : "",
    "year" : "",
    "name2" : "",
    "leaseDate" : ""
    }
    return VPSdata

def violationSearch():
    parameters = {
    'delay' : 15,
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    'operatorMessage' : "Use debug mode, open VPS new Violations/VIOLATORS window, and run to completion",
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
    'dataInFileName' : 'lessee info.csv',
    'dataOutFileName' : 'violators_created.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters


def processInput(fileName):
    dataList = []
    VPSdataInit()
    with open(fileName, 'r') as infile:
        csvInput = csv.reader(infile)
        for row in csvInput:
            inputDict = VPSdataFill(VPSdataInit(), row) # fill the shared data structure
            if inputDict["comment"] == "#":   #input is a comment, continue with next row
                continue
            if inputDict["type"] == "" or inputDict["type"] == 0:  #end -> when first input does not exist
                break
            dataList.append(inputDict)
    return dataList

def vps_body(driver, parameters, fromVPSdata):
    delay = parameters['delay']
    startPageTextLocator = (By.XPATH, '//TD/H1[contains(text(),"Violator Maintenance")]')
    # pause on next line for entry of credentials, and window navigation.
    startWindow = findTargetPage(driver, findStartWindowDelay, startPageTextLocator)
    if startWindow is None:
        print "Start Page not found."
        return None
    with open(parameters['dataOutFileName'], 'a') as outfile:
        outfile.truncate()
        for row in fromVPSdata:

            #Find the VID
            #   find, fill and submit: Violator ID "P_VIOLATOR_ID"
            #   for type "L"
            #       compare first name to "lessor"
            #       compare value of "P_LIC_PLATE_NBR"
            #       change "P_L_VT2_VIOLATOR_TYPE_DESCR" to match "type"
            #       click save button, 'input value="Save" '
            #
            #       verify violator record does not exist
            #       click new button, 'input value="New" '
            #       fill plate, first, last, first2, last2, type(renter/lessee)
            #       create and fill start, end,
            #       fill make, model, body, year
            #       click save button, 'input value="Save" '
            #
            #       click new button frame=fraVF 'input value="New" '
            #       verify Violator Address Maintenance page
            #       fill address, address, city, zip
            #       select or verify ? state
            #       click save button
            #       select new VID
            #
            #       click comment button  Form=  'input name="vpscomments$vps_comments$QForm" '
            #       click new button
            #       in text box enter """Received a leasing agreement between LESSOR and LESSEE .
            #     The agreement states LESSEE leased a {YEAR MAKE MODEL} on STARTDATE ."""
            #     click save button


            #select from Violation Status menu
            menuLocator = (By.XPATH, '//select[@name="P_L_VST_VIOL_STATUS_DESCR"]')
            menuElement = findElementOnPage(driver, delay, menuLocator)
            Selector = Select(menuElement)
            count = 0
            while Selector is None:  # menu select is sometimes None, why ?
                count = count + 1
                print "retrying excusal menu selection. Count: ", count
                Selector = Select(menuElement)
            Selector.select_by_visible_text("ZipCash; Uninvoiced") # does this need to be instanciated each time?

            element = findElementOnPage(driver, delay, parameters['inputLpLocator'])
            submitted = fillFormAndSubmit(driver, startWindow, element, plateString, parameters) # why so slow?
            time.sleep(1)  #page may not be there yet!  how long to wait?
            pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['pageLocator2'])

            #while there is a violation to correct
            while True:
                foundFrame = findAndSelectFrame(driver, delay, "fraRL")
                #time.sleep(1)  #text may not be there yet!  how long to wait?
                text = getTextResults(driver, delay, plateString, parameters, "fraRL")
                if text is not None and text != 0: # there's more to correct
                    #click on the first record
                    element = findElementOnPage(driver, delay, parameters['LpLocator'])
                    element.click()
                    #change the value
                    handle = driver.current_window_handle
                    driver.switch_to_window(handle)
                    foundFrame = findAndSelectFrame(driver, delay, "fraVF")
                    element = findElementOnPage(driver, delay, parameters['inputLpLocator'])
                    submitted = fillFormAndSubmit(driver, startWindow, element, replacementString, parameters)
                    #loop
                    time.sleep(1)  #page may not be there yet!  how long to wait?
                    handle = driver.current_window_handle
                    driver.switch_to_window(handle)
                    continue
                break
            handle = driver.current_window_handle
            driver.switch_to_window(handle)
            foundFrame = findAndSelectFrame(driver, delay, "fraRL")
            clicked = findAndClickButton(driver, delay, parameters)

                # click the query button.
            #test with multiple plate changes

    print "main: Finished with LP_correction file."


if __name__ == '__main__':
    parameters = violationSearch()
    findStartWindowDelay = 3
    print parameters['operatorMessage']
    regexPattens = loadRegExPatterns()
    dataFileName = parameters['dataInFileName']
    inputList = processInput(dataFileName) # add parameters when working
    for dataDict in inputList:
        print dataDict['lessee'], '\t',  dataDict['address']
#        for key,value in dataDict.iteritems():
#            print value
    driver = openBrowser(parameters['url'])
    vps_body(driver, parameters, inputList)
    driver.close()

