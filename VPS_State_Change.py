#-------------------------------------------------------------------------------
# Name:        VPS_State_Change.py
# Purpose:     Accept input from LP_Change,
#              a violation list, wrong ST (opt), correct ST
#              correct each violator, write to donefile
#
# Author:      mthornton
#
# Created:     2015 AUG 01
# Updates:     2017 MAY 19
# Copyright:   (c) michael thornton 2015,2016, 2017
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


def changeStateOnly(driver, parameters):
    delay = parameters['delay']
    startPageTextLocator = (By.XPATH, '//TD/H1[contains(text(),"Violation Search")]')
    # pause on next line for entry of credentials, and window navigation.
    startWindow = findTargetPage(driver, findStartWindowDelay, startPageTextLocator)
    if startWindow is None:
        print "Start Page not found."
        return None
    with open(parameters['dataInFileName'], 'r') as infile, open(parameters['dataOutFileName'], 'a') as outfile:
        outfile.truncate()
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

    parameters = violatorSearch()

    findStartWindowDelay = 3
    print parameters['operatorMessage']
    regexPattens = loadRegExPatterns()
    driver = openBrowser(parameters['url'])
    dataIO(driver, parameters)
    driver.close()

