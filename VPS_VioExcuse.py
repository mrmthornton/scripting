#-------------------------------------------------------------------------------
# Name:        VPS_LP_Count_Images.py
# Purpose:     Examine web pages until the VPS Violation Search page is found.
#              enter a licence plate in the search box
#              find the text number of images
#              write the licence plate and number of images to the output file.
#
# Author:      mthornton
#
# Created:     2015 AUG 01
# Updates:     2016 FEB 05
# Copyright:   (c) michael thornton 2015,2016
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from VPS_LIB import *
from TxDot_LIB import *

import re
import io
import csv
import sys
import string

def violationExcusal():
    parameters = {
    'delay' : 15,
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    'operatorMessage' : "Use debug mode, open VPS, new violation excusal window, and run to completion",
    'startPageTextLocator' : (By.XPATH, '//TD/H1[contains(text(),"Violation Excusal")]'),
    'inputLocator' : (By.XPATH, '//input[@id = "P_VIOLATION_ID"]'),
    'staleLocator' : (By.XPATH,'//h1[contains(text(),"Violation Excusal")]'),
    'buttonLocator' : (By.XPATH,'//input[@value="Excuse"]'),
    'frameParamters' : {'useFrames' : True, 'frameLocator' : [ (By.XPATH, '//frame[@name="fraVF"]'),
                                                               (By.XPATH, '//frame[@name="fraTOP"]') ] },
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : 'Violation Search Results',
    'outputLocator' : (By.XPATH,'//BODY/P[contains(text(),"Record")]'),
    'resultIndexParameters' : {'regex' : "Records \d+ to \d+ of (\d+)", 'selector' : 'tail'},  # head, tail, or all
    #'dataInFileName' : 'LP_Repeats_Count_short.csv',
    'dataInFileName' : 'vio_excuse.csv',
    'dataOutFileName' : 'vio_excuse.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

def excuse_violation(driver, parameters):
    delay = parameters['delay']
    # pause on next line for entry of credentials, and window navigation.
    startWindow = findTargetPage(driver, findStartWindowDelay, parameters['startPageTextLocator'])
    if startWindow is None:
        print "Start Page not found."
        return None
    with open(parameters['dataInFileName'], 'r') as infile, open(parameters['dataOutFileName'], 'a') as outfile:
        outfile.truncate()
        csvInput = csv.reader(infile)
        for row in csvInput:
            rawString = row[0]
            if rawString == "" or rawString == 0:  #end when input does not exist
                break
            inputString = cleanUpString(rawString)
            element = findElementOnPage(driver, delay, parameters['inputLocator'])
            submitted = fillFormAndSubmit(driver, startWindow, element, inputString, parameters)
            #check for excusal page found
            pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['staleLocator'])
            #move to the correct frame
            foundFrame = findAndSelectFrame(driver, delay, parameters)

            #select from drop down menu
            # if the menu is missing check for reason excused
            menuLocator = (By.XPATH, '//select[@name="P_L_EXR_EXCUSED_REAS_DESCR"]')
            menuElement = findElementOnPage(driver, delay, menuLocator)
            Selector = Select(menuElement)
            Selector.select_by_visible_text("Bankruptcy") # does this need to be instanciated each time?

            #click excuse button
            # 'buttonLocator' : (By.XPATH,'//input[@value="Excuse"]'),
            clicked = findAndClickButton(driver, delay, parameters)
            pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['staleLocator'])

            #navigate to search page
            # navigate to search position

            clicked = findAndClickButton(driver, delay, parameters)
            pageLoaded = newPageElementFound(driver, delay, None, parameters['staleLocator'])

    print "main: Finished parsing plate file."

if __name__ == '__main__':


    parameters = violationExcusal()

    findStartWindowDelay = 3
    print parameters['operatorMessage']
    regexPattens = loadRegExPatterns()
    driver = openBrowser(parameters['url'])
    excuse_violation(driver, parameters)
    driver.close()

