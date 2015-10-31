#-------------------------------------------------------------------------------
# Name:        VPS_LIB.py
# Purpose:     A library for common VPS actions.
#
# Author:      mthornton
#
# Created:     2015aug01
# Updates:     2015oct29
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


def waitForSelectedPage(driver, targetText, locator):
    # wait for page to load
    delay = 5 # seconds
    while True:
        for window in driver.window_handles:  # test each window for locator element
            driver.switch_to_window(window)
            print "Searching for '" , targetText, "' in window ", window #debug
            try:
                elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
                for element in elems:       # test each element for target
                    if (element.text == targetText) or (targetText == ""):   #all upper case
                        #print "found '", element.text, "'" # for debug purposes
                        return window, element
            except TimeoutException:
                timeout('locator element not found')
                continue

def findElementOnPage(driver, window, locator):
    delay = 5 # seconds
    while True:
        driver.switch_to_window(window)
        print "switched to target window" # for debug purposes
        try:
            element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
            return window, element
        except TimeoutException:
            timeout('locator element not found')
            continue

def getTextResults(driver, window, element, plateString, parameters):
    delay = 5 # seconds
    driver.switch_to_window(window)
    #print window
    element.clear()
    element.send_keys(plateString)
    element.send_keys("\n")
    try:
        pattern = re.compile('^' + parameters['resultIndexParameters']['index'])
        elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(parameters['outputLocator']))
        for resultElement in elems:       # test each element for target
            found = pattern.search(resultElement.text)
            if (found) or (targetText == ""): # ###########is the empty string needed???
                print "TEXT: '", resultElement.text, "'" # for debug purposes
                return resultElement.text
    except TimeoutException:
        timeout('text not found')

if __name__ == '__main__':
    # add unit test and asserts here
    pass
