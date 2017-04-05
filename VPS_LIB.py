#-------------------------------------------------------------------------------
# Name:        VPS_LIB.py
# Purpose:     A library for common VPS actions using Selenium WebDriver
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

import tkMessageBox
from Tkinter import *

import UTIL_LIB

import re
import time


def fillFormAndSubmit(driver, window, element, textForForm, parameters):
    if type(element) == type(None): # skip the form submission
        return False
    #assert(driver.current_window_handle == window)
    #print("fillFormAndSubmit: " , driver.current_url) # for debug purposes
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
        print("findAndClickButton: button not found.")
        return False
    button.click()
    return True


def findAndSelectFrame(driver, delay, frameName):
    ''' 	recursive frame search
    (A) search for target at current content
    (B1) if found return True
    (B2) if not found append all frames to local list
    (C) loop until list is empty or the frame is found
        (C1) pop from list
        (C2) select frame and recurse,
        (C3) end loop if recuse returns True
        (C4) if list empty return False (not found)
    '''
    def walkFrames(targetLocator, parentFrame):
        frameList = []
        frameDelay = 1
        #if targetLocator is not None:
        try:
            foundFrame = WebDriverWait(driver, frameDelay).until(EC.presence_of_element_located(targetLocator))
            foundFrameName = foundFrame.get_attribute("name")
            driver.switch_to_frame(foundFrame)
            print("walkFrames: found target frame ", foundFrameName)  # for debug purposes
            return True
        except TimeoutException:
            try:
                frames = WebDriverWait(driver, frameDelay).until(EC.presence_of_all_elements_located((By.XPATH, '//frame' )))
            except TimeoutException:
                return False
            for frame in frames:
                frameList.append(frame)
            print("findAndSelectFrame: creating framelist: length of ", len(frameList))
            while True:
                try:
                    nextParentFrame = frameList.pop()
                    nextParentFrameName = nextParentFrame.get_attribute("name")
                    driver.switch_to_frame(nextParentFrame)
                    print("walkFrames: next parent is ", nextParentFrameName)
                    if walkFrames(targetLocator, nextParentFrame):
                        return True
                    if parentFrame is None:
                        driver.switch_to_default_content()
                    else:
                        driver.switch_to_frame(parentFrame)
                except IndexError :
                    print("findAndSelectFrame: ", targetLocator, " not found.")
                    return False

    targetLocator = None
    # build the target locator from the argument
    if frameName is None: return False
    locatorText = '//frame[@name="' + frameName + '"]'
    # print(locatorText)
    targetLocator =  (By.XPATH, '//frame[@name="' + frameName + '"]' )
    # print(targetLocator)
    return walkFrames(targetLocator, None)


def findElementOnPage(driver, delay, elementLocator, window=None):
    if elementLocator == None:# skip finding the element
        return None
    if window is not None:
        driver.switch_to_window(window) # switch to window if supplied
        print("findElementOnPage: switched to target window")
    try:
        element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(elementLocator))
        return element
    except TimeoutException:
        timeout('findElementOnPage: element' + str(elementLocator) + 'not found')
        return None


def findTargetPage(driver, delay, locator, frameName=None):
    try:
        handle = driver.current_window_handle
    except NoSuchWindowException:
        print("findTargetPage: nothing to process, all windows finished?")
        return None
    handles = driver.window_handles
    for handle in handles:  # test each window for target
        driver.switch_to_window(handle)
        foundFrame = findAndSelectFrame(driver, delay, frameName)
        print("findTargetPage: Searching for  ", locator) # for debug purposes
        try:
            elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            timeout('findTargetPage: locator element not found')
            continue
        #print("findTargetPage: found '", element.text, "'") # for debug purposes
        return handle
    print("findTargetPage: 'target page' not found"
    return None


def getTextResults(driver, delay, plateString, parameters, frameName=None):
    #print("getTextResults: " + driver.current_url) # for debug
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
            foundFrame = findAndSelectFrame(driver, delay, frameName)
            continue  # why does this not find the text
                        #try this with the locator using rEGEX, and  why not found? no frame? pass in frame?
        try:
            elemText = resultElement.text
        except StaleElementReferenceException:
            print("getTextResults: stale text element")
            elemText = ""  # reset the element text and continue

        if elemText == 'No Records returned':
            return 0
        if elemText == 'Record 1 of 1':
            return elemText
        text = pattern.findall(elemText)
        if len(text):
            #print("getTextResults", text) # for debug
            return text[0]
    return None


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
            print("newPageElementFound/findAndSelectFrame: ", frameLocator, " not found.")
            return False
    try:
        while True:
            try:
                resultElement = WebDriverWait(driver, 1).until(EC.presence_of_element_located(elementlocator))
                driver.switch_to_default_content()
                return True
            except TimeoutException:
                print('newPageElementFound: ',elementlocator, 'element not found')
                # select the proper frame before the 'continue'
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
    #pyseldriver.get(url)
    #return pyseldriver
    driver.get(url)
    return driver


def parseString(inputString,indexPattern, targetPattern, segment="all"): # segment may be start, end, or all
    # the iterator is used to search for all possible target pattern instances
    found = indexPattern.search(inputString)
    if found != None:
        indexStart = found.start()
        indexEnd = found.end()
        #print("parseString: found start", indexStart) #debug statement
        iterator = targetPattern.finditer(inputString)
        for found in iterator:
            if found.start() > indexStart and found != None:
                targetStart = found.start()
                targetEnd = found.end()
                #print("parseString: found end", targetStart) #debug statement
                return inputString[indexEnd:targetEnd:]
    return None


def returnOrClick(element, select):
    if select =='return':
        element.send_keys(Keys.RETURN)
    elif select == 'click':
        element.click()
    else:
        print("ERROR: returnOrClick:")
        print("'select' should be one of 'return' or 'click'")


if __name__ == '__main__':

    # setup test parameters
    parameters = {
        'frameParamters' : {'useFrames' : True, 'frameLocator' : (By.XPATH, '//frame[@name="frame-middle"]')}
    }
    #url = 'file://C:/Users/IEUser/Documents/scripts/frames/nested_frames.html'
    url = 'http://the-internet.herokuapp.com/nested_frames'
    ##url = 'http://the-internet.herokuapp.com/iframe'
    elementLocator = (By.XPATH, '//div[contains(text(),"MIDDLE")]')
    window = None
    delay = 5

    # test library components
    assert(cleanUpString('123 45   6,,"\n\n') == '123456\n')
    driver = openBrowser(url)
    findAndSelectFrame(driver, delay, 'frame-middle')
    #time.sleep(10)
    #window = findTargetPage(driver, delay, elementLocator) # no window, why?
    #returnOrClick()
    #loadRegExPatterns()
    #timeout()

    #waitForNewPage()

    #findElementOnPage(driver, delay, elementLocator)
    #getTextResults()
    #driver.close()
    driver.quit()
    print("FINISHED")
