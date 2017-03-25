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
# Updates:     2016 MAR 03
# Copyright:   (c) michael thornton 2015,2016
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from VPS_LIB import *

import sys
import string


def violationExcusal():
    parameters = {
    'delay' : 15,
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    'operatorMessage' : "Use debug mode, open VPS, new violation excusal window, and run to completion",
    'startPageTextLocator' : (By.XPATH, '//TD/H1[contains(text(),"Violation Excusal")]'),
    'inputLocator' : (By.XPATH, '//input[@id = "P_VIOLATION_ID"]'),
    'headerLocator' : (By.XPATH,'//h1[contains(text(),"Violation Excusal")]'),
    'buttonLocator' : (By.XPATH,'//input[@value="Excuse"]'),
    'frameParamters' : {'useFrames' : True, 'frameLocator' : (By.XPATH, '//frame[@name="fraRL"]' ) },
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
    waitForUser('VPS login')
    startPageTextLocator = (By.XPATH, '//TD/H1[contains(text(),"ThisWillNeverBeFound")]')
    count = 0
    while True:
        touchWindows = findTargetPage(driver, findStartWindowDelay, startPageTextLocator)
        count = count + 1; print count + 1
        time.sleep(10*60)


if __name__ == '__main__':

    parameters = violationExcusal()

    findStartWindowDelay = 3
    print parameters['operatorMessage']
    driver = openBrowser(parameters['url'])
    excuse_violation(driver, parameters)
    driver.close()
    driver.quit()

