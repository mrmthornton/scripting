#-------------------------------------------------------------------------------
# Name:        VPS_LIB.py
# Purpose:     A library for common VPS actions.
#
# Author:      mthornton
#
# Created:     2015 AUG 01
# Updates:     2015 NOV 17
# Copyright:   (c) michael thornton 2015
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import re

def cleanUpLicensePlateString(plateString):
    plateString = plateString.replace(' ' , '') # remove any spaces
    plateString = plateString.replace('"' , '') # remove any double quotes
    plateString = plateString.replace('\t' , '') # remove any tabs
    plateString = plateString.replace(',' , '\n') # replace comma with \n
    for n in range(10):            # replace multiple newlines with a single \n
        plateString = plateString.replace('\n\n' , '\n')
    return plateString

def fillFormAndSubmit(driver, window, element, textForForm, parameters):
    if type(element) == type(None): # skip the form submission
        return
    #assert(driver.current_window_handle == window)
    #print "fillFormAndSubmit: " + driver.current_url # for debug purposes
    element.clear()
    element.send_keys(textForForm)
    returnOrClick(element, parameters['returnOrClick'])

def findAndClickButton(driver, delay, parameters):
    if type(parameters['buttonLocator']) == type(None):
        return False
    try:
        button = WebDriverWait(driver, delay).until(EC.presence_of_element_located(parameters['buttonLocator']))

    except TimeoutException:
        print "findAndClickButton: button not found."
        return False
    button.click()
    return True

def findAndSelectFrame(driver, delay, parameters):
    if parameters['frameParamters']['useFrames']:
        for locator in parameters['frameParamters']['frameLocator']:
            try:
                foundFrame = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
            except TimeoutException:
                print "findAndSelectFrame: ", locator, " not found."
                return False
            driver.switch_to_frame(foundFrame)
        return True

def findElementOnPage(driver, delay, elementLocator, window=None):
    if elementLocator == None:# skip finding the element
        return None
    if window != None:
        driver.switch_to_window(window) # switch to window if supplied
        print "findElementOnPage: switched to target window"
    try:
        element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(elementLocator))
        return element
    except TimeoutException:
        timeout('findElementOnPage: element' + str(elementLocator) + 'not found')
        return None

def findTargetPage(driver, delay, locator, targetText=""):
    try:
        handle = driver.current_window_handle
    except NoSuchWindowException:
        print "findTargetPage: nothing to process, all windows finished?"
        return None, None
    handles = driver.window_handles
    for handle in handles:  # test each window for target
        driver.switch_to_window(handle)
        print "findTargetPage: Searching for '" , targetText, "' in window ", handle # for debug purposes
        try:
            elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            timeout('findTargetPage: locator element not found')
            continue
        for element in elems:       # test each element for target
            if (element.text == targetText) or (targetText == ""):
                #print "findTargetPage: found '", element.text, "'" # for debug purposes
                return handle, element
    print "findTargetPage: 'target text' not found"
    return None, None

def getTextResults(driver, delay, plateString, parameters):
    #print "getTextResults: " + driver.current_url # for debug purposes
    if parameters['outputLocator']== None: # skip finding text
        return None
    try:
        resultElement = WebDriverWait(driver, delay).until(EC.presence_of_element_located(parameters['outputLocator']))
    except TimeoutException:
        timeout('getTextResults: text not found')
        return None
    text = resultElement.text
    resultIndex = parameters['resultIndexParameters']['index']
    pattern = re.compile(resultIndex)
    isFound = pattern.search(text)
    if isFound != None:
        #print "getTextResults: TEXT: '", text, "'" # for debug purposes
        return text
    else:
        return None

def loadRegExPatterns():
    patterns = {
    'linePattern' : re.compile('^.+'),
    'wordPattern' : re.compile('\w+'),
    'csvPattern' : re.compile('[A-Z0-9 .#&]*,'),
    'commaToEOLpattern' : re.compile(',[A-Z0-9 .#&]+$'),
    'LICpattern' : re.compile('^LIC '),
    'issuedPattern' : re.compile('ISSUED '),
    'reg_dtPattern' : re.compile('REG DT '),
    'datePattern' : re.compile('[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}'), # mo/day/year
    'dateYearFirstPattern' : re.compile(r'\d{4,4}/\d{2,2}/\d{2,2}'), # year/mo/day
    }

def newPageIsLoaded(driver, delay, currentElement):
    def isStale(self):
        if type(currentElement) == type(None):# when there is no element to check,
            return True          # quit immediately
            #return False          # loop until timeout occurs
        try:
            # poll the current element with an arbitrary call
            nullText = currentElement.text
            #nullText = currentElement.find_elements_by_id('doesnt_matter')
            return False
        except StaleElementReferenceException:
            return True
    try:
        WebDriverWait(driver, delay).until(isStale)
        return True
    except TimeoutException:
        timeout('newPageLoaded: old page reference never went stale')
        return False

def openBrowser(url):
    driver = webdriver.Ie()
    #driver.maximize_window()
    driver.get(url)
    return driver

def parseString(inputString,indexPattern, targetPattern, segment="all"): # segment may be start, end, or all
    # the iterator is used to search for all possible target pattern instances
    found = indexPattern.search(inputString)
    if found != None:
        indexStart = found.start()
        indexEnd = found.end()
        #print "parseString: found start", indexStart #debug statement
        iterator = targetPattern.finditer(inputString)
        for found in iterator:
            if found.start() > indexStart and found != None:
                targetStart = found.start()
                targetEnd = found.end()
                #print "parseString: found end", targetStart #debug statement
                return inputString[indexEnd:targetEnd:]
    return None

def returnOrClick(element, select):
    if select =='return':
        element.send_keys(Keys.RETURN)
    elif select == 'click':
        element.click()
    else:
        print "ERROR: returnOrClick:"
        print "'select' should be one of 'return' or 'click'"

def timeout(msg="Took too much time!"):
    print msg

if __name__ == '__main__':

    # setup test parameters
    url = 'file://C:/Users/IEUser/Documents/scripting/testPage.html'
    elementLocator = (By.XPATH, '//p')
    window = None
    delay = 1

    # test library components
    assert(cleanUpLicensePlateString('123 45   6,,"\n\n') == '123456\n')
    driver = openBrowser(url)
    window = findTargetPage(driver, delay, locator) # no window, why?
    #returnOrClick()
    #loadRegExPatterns()
    #timeout()

    #waitForNewPage()

    findElementOnPage(driver, delay, elementLocator)
    #getTextResults()
    driver.close()
    print "PASSED"
