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


def changeLP(driver, delay, parameters, startWindow, wrongPlate, correctPlate, correctState):
    while True:
        foundFrame = findAndSelectFrame(driver, delay, "fraRL")
        text = getTextResults(driver, delay, wrongPlate, parameters, "fraRL")
        if text == 0: # finished with
            print("VPS_LP_Change:common_code: Finished with ", wrongPlate, "No more records")
            break
        if text is not None: # there's more to correct

            #click on the first record
            locator =  (By.XPATH, '//td[@id = "LIC_PLATE_NBR1"]')
            element = findElementOnPage(driver, delay, locator)
            element.click()

            #change the to the form frame
            handle = driver.current_window_handle
            driver.switch_to_window(handle)
            foundFrame = findAndSelectFrame(driver, delay, "fraVF")

            #change the STATE value and the LP value
            menuElement = findElementOnPage(driver, delay, parameters['inputStateLocator'])
            Selector = Select(menuElement)
            count = 0
            while Selector is None:  # menu select is sometimes None, why ?
                count = count + 1
                print("retrying excusal menu selection. Count: ", count)
                Selector = Select(menuElement)
            option = Selector.first_selected_option
            # #print("VPS_LP_Change:common code: menu value is ", option.opt)  ### how to find selected value?
            Selector.select_by_visible_text(correctState) # does this need to be instanciated each time?
            if wrongPlate != correctPlate: # if the plate changed, update it.
                element = findElementOnPage(driver, delay, parameters['inputLpLocator'])
                submitted = fillFormAndSubmit(driver, startWindow, element, correctPlate, parameters)
            else:
                saveLocator = (By.XPATH, '//input[@value = "Save"]')
                saveButton = findElementOnPage(driver, delay, saveLocator)
                saveButton.click()

            time.sleep(1)  #page may not be there yet, wait.
            handle = driver.current_window_handle
            driver.switch_to_window(handle)
            continue
        break # go to next plate
    return

def changeStateOnly(driver, delay, parameters, startWindow, wrongPlate, correctPlate, correctState):
    pass

def findAllViolations(driver, delay, parameters, startWindow, wrongPlate, correctPlate, correctState):
        saveButtonLocator = (By.XPATH,'//input[@value="Query"]')
        parameters['buttonLocator'] = (By.XPATH, '//input[@value="Next"]')

        vids = []
        while True:
            foundFrame = findAndSelectFrame(driver, delay, "fraRL")
            count = getTextResults(driver, delay, wrongPlate, parameters, "fraRL")
            count = int(count)
            if count == 0: # finished with
                print("VPS_LP_Change:common_code: Finished with ", wrongPlate, "No more records")
                break
            if count is not None: # there's more to correct
                # get the Nth violation ID
                for i in range(1,11):
                    vidLocator =  (By.XPATH, '//td[@id = "VIOLATION_ID'+str(i)+'"]')
                    vidElement = findElementOnPage(driver, delay, vidLocator)
                    if vidElement is not None:
                        vidUtext = vidElement.text
                        vid = vidUtext.encode('ascii', 'ignore')
                        vids.append(vid)
                print(len(vids)) # for debug

                # click next button
                parameters['buttonLocator'] = (By.XPATH, '//input[@value="Next"]')
                if not findAndClickButton(driver, delay, parameters):
                    assert(count == len(vids))
                    break

                time.sleep(1)  #page may not be there yet!  how long to wait?
                handle = driver.current_window_handle
                driver.switch_to_window(handle)
                continue
            break
        return vids
        #handle = driver.current_window_handle
        #driver.switch_to_window(handle)
        #foundFrame = findAndSelectFrame(driver, delay, "fraRL")
        #clicked = findAndClickButton(driver, delay, parameters)

if __name__ == '__main__':
    print('NO tests defined')