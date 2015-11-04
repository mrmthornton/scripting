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

import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC

from selenium.webdriver.common.keys import Keys

def returnOrClick(element, select):
    if select =='return':
        element.send_keys(Keys.RETURN)
    elif select == 'click':
        element.click()
    else:
        print "ERROR: returnOrClick - assert failed"

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

def waitForNewPage(driver, currentElement):
    def isStale():
        try:
            # poll the link with an arbitrary call
            #driver.find_elements_by_id('doesnt-matter')
            newElement = currentElement
            return False
        except StaleElementReferenceException:
            return True
    wait_for(isStale)

def findTargetPage(driver, targetText, locator):
    delay = 5 # seconds
    while True:
        for window in driver.window_handles:  # test each window for taget text
            driver.switch_to_window(window)
            print "findTargetPage: Searching for '" , targetText, "' in window ", window # for debug purposes
            try:
                elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
                for element in elems:       # test each element for target
                    if (element.text == targetText) or (targetText == ""):   #all upper case
                        print "findTargetPage: found '", element.text, "'" # for debug purposes
                        return window, element
            except TimeoutException:
                timeout('locator element not found')
                continue

def findElementOnPage(driver, window, locator):
    delay = 5 # seconds
    while True:
        driver.switch_to_window(window)
        print "findElementOnPage: switched to target window" # for debug purposes
        try:
            element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
            return window, element
        except TimeoutException:
            timeout('findElementOnPage: locator element not found')
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
    print "getTextResults: " + driver.current_url # for debug purposes
    try:
        print "getTextResults: " + driver.current_url # for debug purposes
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
    #returnOrClick()
    #loadRegExPatterns()
    #timeout()
    #openBrowser()
    assert(cleanUpLicensePlateString('123 45   6,,"\n\n') == '123456\n')
    #waitForNewPage()
    #findTargetPage()
    #findElementOnPage()
    #getTextResults()
    print "PASSED"
