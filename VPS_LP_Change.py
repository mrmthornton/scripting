#-------------------------------------------------------------------------------
# Name:        VPS_LP_Count_Images.py
# Purpose:     Examine web pages until the VPS Violation Search page is found.
#              enter a licence plate in the search box
#              find the text number of images
#              write the licence plate and number of images to the output file.
#
# Author:      mthornton
#
# Created:     2015 AUG 01
# Updates:     2016 OCT 14
# Copyright:   (c) michael thornton 2015,2016
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


def violationSearch():
    parameters = {
    'delay' : 15,
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    #'url' : 'http://intranet/SitePages', # initial URL
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


def vps_body(driver, parameters):
    delay = parameters['delay']
    startPageTextLocator = (By.XPATH, '//TD/H1[contains(text(),"Violation Search")]')
    # pause on next line for entry of credentials, and window navigation.
    startWindow = findTargetPage(driver, findStartWindowDelay, startPageTextLocator)
    if startWindow is None:
        print "Start Page not found."
        return None
    with open(parameters['dataInFileName'], 'r') as infile:
        csvInput = csv.reader(infile)
        for row in csvInput:
            rawString = row[0]
            if rawString == "" or rawString == 0:  #end when first input does not exist
                break
            plateString = cleanUpString(rawString)
            rawString = row[1]
            if rawString == "" or rawString == 0:  #end when second input does not exist
                break
            replacementString = cleanUpString(rawString)

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
    driver = openBrowser(parameters['url'])
    waitForUser()
    vps_body(driver, parameters)
    driver.close()

