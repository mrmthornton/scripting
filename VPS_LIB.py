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

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC


def timeout(msg="Took too much time!"):
    print msg

from selenium.webdriver.common.keys import Keys

def returnOrClick(element, switch):
    if switch =='R':
        element.send_keys(Keys.RETURN)
    if switch == 'C':
        element.click()

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

def getText(driver, window, element, plateString, txtLocator=("","")):
    delay = 5 # seconds
    driver.switch_to_window(window)
    #print window
    element.clear()
    element.send_keys(plateString)
    element.send_keys("\n")
    try:
        element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(txtLocator))
        return element.text
    except TimeoutException:
        timeout('text not found')

if __name__ == '__main__':
    # add unit test and asserts here
    pass
