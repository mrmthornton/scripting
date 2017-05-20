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
        #time.sleep(1)  #text may not be there yet!  how long to wait?
        text = getTextResults(driver, delay, wrongPlate, parameters, "fraRL")
        if text == 0: # finished with
            print("VPS_LP_Change:common_code: Finished with ", wrongPlate, "No more records")
            break
        if text is not None: # there's more to correct

            #click on the Nth record
            locator =  (By.XPATH, '//td[@id = "LIC_PLATE_NBR1"]')
            element = findElementOnPage(driver, delay, locator)
            element.click()

            #change the value
            handle = driver.current_window_handle
            driver.switch_to_window(handle)
            foundFrame = findAndSelectFrame(driver, delay, "fraVF")

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

            time.sleep(1)  #page may not be there yet!  how long to wait?
            handle = driver.current_window_handle
            driver.switch_to_window(handle)
            continue
        break # go to next plate
    return

def changeStateOnly(driver, parameters):



        n=1
        vid=0
        while True:
            foundFrame = findAndSelectFrame(driver, delay, "fraRL")
            #time.sleep(1)  #text may not be there yet!  how long to wait?
            text = getTextResults(driver, delay, wrongPlate, parameters, "fraRL")
            if text == 0: # finished with
                print("VPS_LP_Change:common_code: Finished with ", wrongPlate, "No more records")
                break
            if text is not None: # there's more to correct
                if n>text: break  #end of list
                if n>10: # if end of page
                    # click next button
                    locator =  (By.XPATH, '//input[@value="Next"]')
                    element = findElementOnPage(driver, delay, locator)
                    element.click()
                    n=1 # start over
                    # continue loop

                #click on the Nth record
                locator =  (By.XPATH, '//td[@id = "LIC_PLATE_NBR'+str(n)+'"]')
                element = findElementOnPage(driver, delay, locator)
                element.click()
                # get vID
                vidLocator =  (By.XPATH, '//td[@id = "VIOLATION_ID'+str(n)+'"]')
                vidElement = findElementOnPage(driver, delay, vidLocator)
                vidUtext = vidElement.text
                newVid = vidUtext.encode('ascii', 'ignore')
                if newVid == vid:
                    n+=1
                vid = newVid

                #change the value
                handle = driver.current_window_handle
                driver.switch_to_window(handle)
                foundFrame = findAndSelectFrame(driver, delay, "fraVF")

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

                time.sleep(1)  #page may not be there yet!  how long to wait?
                handle = driver.current_window_handle
                driver.switch_to_window(handle)
                continue
            break
        handle = driver.current_window_handle
        driver.switch_to_window(handle)
        foundFrame = findAndSelectFrame(driver, delay, "fraRL")
        clicked = findAndClickButton(driver, delay, parameters)

