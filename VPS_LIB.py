#-------------------------------------------------------------------------------
# Name:        VPS_LIB.py
# Purpose:     A library for common VPS actions.
#
# Author:      mthornton
#
# Created:     2015 AUG 01
# Updates:     2015 NOV 03
# Copyright:   (c) michael thornton 2015
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import re


def returnOrClick(element, select):
    if select =='return':
        element.send_keys(Keys.RETURN)
    elif select == 'click':
        element.click()
    else:
        print "ERROR: returnOrClick:"
        print "'select' should be one of 'return' or 'click'"

def loadRegExPatterns():
    global linePattern
    global wordPattern
    global csvPattern
    global commaToEOLpattern
    global LICpattern
    global issuedPattern
    global reg_dtPattern
    global datePattern
    global dateYearFirstPattern

    linePattern = re.compile('^.+')
    wordPattern = re.compile('\w+')
    csvPattern = re.compile('[A-Z0-9 .#&]*,')
    commaToEOLpattern = re.compile(',[A-Z0-9 .#&]+$')
    LICpattern = re.compile('^LIC ')
    issuedPattern = re.compile('ISSUED ')
    reg_dtPattern = re.compile('REG DT ')
    datePattern = re.compile('[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}') # mo/day/year
    dateYearFirstPattern = re.compile(r'\d{4,4}/\d{2,2}/\d{2,2}') # year/mo/day

def timeout(msg="Took too much time!"):
    print msg

def openBrowser(url):
    driver = webdriver.Ie()
    #driver.maximize_window()
    driver.get(url)
    return driver

def cleanUpLicensePlateString(plateString):
    plateString = plateString.replace(' ' , '') # remove any spaces
    plateString = plateString.replace('"' , '') # remove any double quotes
    plateString = plateString.replace('\t' , '') # remove any tabs
    plateString = plateString.replace(',' , '\n') # replace comma with \n
    for n in range(10):            # replace multiple newlines with a single \n
        plateString = plateString.replace('\n\n' , '\n')
    return plateString

def waitForNewPage(driver, currentElement, delay=2):
    def isStale(self):
        try:
            # poll the current element with an arbitrary call
            nullText = currentElement.text
            return False
        except StaleElementReferenceException:
            return True
    try:
        WebDriverWait(driver, delay).until(isStale)
    except TimeoutException:
        timeout('waitForNewPage: old page reference never went stale')

def findTargetPage(driver, locator, targetText=""):
    delay = 5 # seconds
    while True:
        for handle in driver.window_handles:  # test each window for target text
            driver.switch_to_window(handle)
            print "findTargetPage: Searching for '" , targetText, "' in window ", handle # for debug purposes
            try:
                elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
                for element in elems:       # test each element for target
                    if (element.text == targetText) or (targetText == ""):   #all upper case
                        #print "findTargetPage: found '", element.text, "'" # for debug purposes
                        return handle, element
            except TimeoutException:
                timeout('findTargetPage: locator element not found')
                continue

def findElementOnPage(driver, elementLocator, window=None ):
    delay = 5 # seconds
    if window != None:
        driver.switch_to_window(window)
        print "findElementOnPage: switched to target window"
    while True:
        try:
            element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(elementLocator))
            return element
        except TimeoutException:
            timeout('findElementOnPage: element not found')
            continue

def fillFormAndSubmit(driver, window, element, formText, parameters):
    delay = 5 # seconds
    assert(driver.current_window_handle == window)
    print "fillFormAndSubmit: " + driver.current_url # for debug purposes
    element.clear()
    element.send_keys(formText)
    returnOrClick(element, parameters['returnOrClick'])

def getTextResults(driver, window, plateString, parameters):
    delay = 5 # seconds
    assert(driver.current_window_handle == window)
    #print "getTextResults: " + driver.current_url # for debug purposes
    try:
        resultElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located(parameters['outputLocator']))
        resultIndex = parameters['resultIndexParameters']['index']
        pattern = re.compile(resultIndex)
        isFound = pattern.search(resultElement.text)
        if (isFound) or (resultIndex == ""):
            print "getTextResults: TEXT: '", resultElement.text, "'" # for debug purposes
            return resultElement.text
        else: return None
    except TimeoutException:
        timeout('text not found')

if __name__ == '__main__':

    # setup test parameters
    url = 'file://C:/Users/IEUser/Documents/scripting/testPage.html'
    locator = (By.XPATH, '//*')
    window = None

    # test library components
    assert(cleanUpLicensePlateString('123 45   6,,"\n\n') == '123456\n')

    driver = openBrowser(url)
    window = findTargetPage(driver, locator)
    #returnOrClick()
    #loadRegExPatterns()
    #timeout()

    #waitForNewPage()

    findElementOnPage(driver, elementLocator)
    #getTextResults()
    driver.close()
    print "PASSED"
