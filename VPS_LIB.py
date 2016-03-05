#-------------------------------------------------------------------------------
# Name:        VPS_LIB.py
# Purpose:     A library for common VPS actions.
#
# Author:      mthornton
#
# Created:     2015 AUG 01
# Updates:     2016 MAR 03
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

def cleanUpString(messyString):
    cleanString = messyString.replace(' ' , '') # remove any spaces
    cleanString = cleanString.replace('"' , '') # remove any double quotes
    cleanString = cleanString.replace('\t' , '') # remove any tabs
    cleanString = cleanString.replace(',' , '\n') # replace comma with \n
    for n in range(10):            # replace multiple newlines with a single \n
        cleanString = cleanString.replace('\n\n' , '\n')
    return cleanString

def fillFormAndSubmit(driver, window, element, textForForm, parameters):
    if type(element) == type(None): # skip the form submission
        return False
    #assert(driver.current_window_handle == window)
    #print "fillFormAndSubmit: " + driver.current_url # for debug purposes
    element.clear()
    element.send_keys(textForForm)
    returnOrClick(element, parameters['returnOrClick'])
    return True

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

''' 	recursive frame search
(A) search for target at current content
(B) if not found
        append all frames to list
(C) pop from list, select and recurse; if list empty error
'''
def findAndSelectFrame(driver, delay, parameters, frameName=None):
    frameList = []
    targetLocator = None

    if frameName is not None:   # build the target locator from the argument
        locatorText = '//frame[@name="' + frameName + '"]'
        # print locatorText
        targetLocator =  (By.XPATH, '//frame[@name="' + frameName + '"]' )
        # print targetLocator

    # use the target locator in the parameters dictionary
    if parameters['frameParamters']['useFrames'] and frameName is None:
        targetLocator = parameters['frameParamters']['frameLocator']
        # print targetLocator

    if targetLocator is not None:
        try:
            foundFrame = WebDriverWait(driver, delay).until(EC.presence_of_element_located(targetLocator))
            driver.switch_to_frame(foundFrame)
            return True
        except TimeoutException:
            frames = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.XPATH, '//frame' )))
            for frame in frames:
                frameList.append(frame)
            print "findAndSelectFrame: creating framelist: ", frameList
            print "findAndSelectFrame: ", targetLocator, " not found."

def findElementOnPage(driver, delay, elementLocator, window=None):
    if elementLocator == None:# skip finding the element
        return None
    if window is not None:
        driver.switch_to_window(window) # switch to window if supplied
        print "findElementOnPage: switched to target window"
    try:
        element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(elementLocator))
        return element
    except TimeoutException:
        timeout('findElementOnPage: element' + str(elementLocator) + 'not found')
        return None

def findTargetPage(driver, delay, locator):
    try:
        handle = driver.current_window_handle
    except NoSuchWindowException:
        print "findTargetPage: nothing to process, all windows finished?"
        return None
    handles = driver.window_handles
    for handle in handles:  # test each window for target
        driver.switch_to_window(handle)
        print "findTargetPage: Searching for  ", locator # for debug purposes
        try:
            elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            timeout('findTargetPage: locator element not found')
            continue
        #print "findTargetPage: found '", element.text, "'" # for debug purposes
        return handle
    print "findTargetPage: 'target page' not found"
    return None

def getTextResults(driver, delay, plateString, parameters, frameName=None):
    #print "getTextResults: " + driver.current_url # for debug
    text_regex = parameters['resultIndexParameters']['regex']
    pattern = re.compile(text_regex)
    if parameters['outputLocator']== None: # skip finding text
        return None
    while True:
        try:
            # short delay with retry loop
            resultElement = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located(parameters['outputLocator']))
        except TimeoutException:
            timeout('getTextResults: text not found, trying again...')
            #driver.switch_to_default_content()
            foundFrame = findAndSelectFrame(driver, delay, parameters, frameName)
            continue  # why does this not find the text
                        #try this with the locator using rEGEX, and  why not found? no frame? pass in frame?
        try:
            elemText = resultElement.text
        except StaleElementReferenceException:
            print "getTextResults: stale text element"
            elemText = ""  # reset the element text and continue

        if elemText == 'No Records returned':
            return 0

        text = pattern.findall(elemText)
        if len(text):
            #print "getTextResults", text # for debug
            return text[0]
    return None

def loadRegExPatterns():
    regex_patterns = dict(
        linePattern=re.compile('^.+'),
        wordPattern=re.compile('\w+'),
        numCommaPattern=re.compile('[0-9,]+'),
        csvPattern=re.compile('[A-Z0-9 .#&]*,'),
        commaToEOLpattern=re.compile(',[A-Z0-9 .#&]+$'),
        LICpattern=re.compile('^LIC '),
        issuedPattern=re.compile('ISSUED '),
        reg_dtPattern=re.compile('REG DT '),
        datePattern=re.compile('[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}'),
        dateYearFirstPattern=re.compile(r'\d{4,4}/\d{2,2}/\d{2,2}')
    )
    return regex_patterns

def newPageElementFound(driver, delay, frameLocator, elementlocator):
    if elementlocator is None: # skip finding text
        return None
    # move the loop outside of the try/except
    if frameLocator is not None:
        try:
            foundFrame = WebDriverWait(driver, delay).until(EC.presence_of_element_located(frameLocator))
            if foundFrame is not None:
                driver.switch_to_frame(foundFrame)
            else:
                return False
        except TimeoutException:
            print "newPageElementFound/findAndSelectFrame: ", frameLocator, " not found."
            return False
    try:
        while True:
            try:
                resultElement = WebDriverWait(driver, 1).until(EC.presence_of_element_located(elementlocator))
                driver.switch_to_default_content()
                return True
            except TimeoutException:
                print 'newPageElementFound: ',elementlocator, 'element not found'
                continue
    except TimeoutException:
            return None
    return None

def newPageIsLoaded(driver, delay, currentElement): # depricated ?
    def isStale(self):
        if type(currentElement) == type(None):# when there is no element to check,
            return True          # quit immediately
            #return False          # loop until timeout occurs
        try:
            # poll the current element with an arbitrary call
            WebDriverWait(driver, delay).until(EC.staleness_of(currentElement))
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
    assert(cleanUpString('123 45   6,,"\n\n') == '123456\n')
    driver = openBrowser(url)
    window = findTargetPage(driver, delay, elementLocator) # no window, why?
    #returnOrClick()
    #loadRegExPatterns()
    #timeout()

    #waitForNewPage()

    findElementOnPage(driver, delay, elementLocator)
    #getTextResults()
    driver.close()
    print "PASSED"
