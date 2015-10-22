#-------------------------------------------------------------------------------
# Name:        VPS_LIB.py
# Purpose:     A library for common VPS actions.
#
# Author:      mthornton
#
# Created:     2015aug01
# Updates:     2015oct21
# Copyright:   (c) michael thornton 2015
#-------------------------------------------------------------------------------

import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC

from selenium.webdriver.common.keys import Keys

def returnOrClick(element, switch):
    if switch =='R':
        element.send_keys(Keys.RETURN)
    if switch == 'C':
        element.click()

def loadRegExPatterns():
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
            print "Searching for '" , targetText, "' in window ", window
            try:
                elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
                for element in elems:       # test each element for target
                    if (element.text == targetText) or (targetText == ""):   #all upper case
                        print "found '", element.text, "'"
                        return window, element
            except TimeoutException:
                timeout('locator element not found')
                continue

def findElementOnPage(driver, window, locator):
    delay = 5 # seconds
    while True:
        driver.switch_to_window(window)
        print "switched to target window"
        try:
            element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
            return window, element
        except TimeoutException:
            timeout('locator element not found')
            continue

def getText(driver, window, element, plateString, txtLocator=("",""), targetText=""):
    delay = 5 # seconds
    driver.switch_to_window(window)
    #print window
    element.clear()
    element.send_keys(plateString)
    element.send_keys("\n")
    try:
        pattern = re.compile('^' + targetText)
        elem = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(txtLocator))
        for element in elem:       # test each element for target
            found = pattern.search(element.text)
            if (found) or (targetText == ""):
                print "TEXT: '", element.text, "'"
                return element.text
    except TimeoutException:
        timeout('text not found')

if __name__ == '__main__':
    # add unit test and asserts here
    pass
