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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC

from VPS_LIB import *

import re
import io
import csv
import sys
import string
import time

def violatorSearch():
    parameters = {
    'delay' : 15,
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    #'url' : 'http://intranet/SitePages', # initial URL
    'operatorMessage' : "Use debug mode, open VPS, new violator search window, and run to completion",
    'staleLocator' : (By.XPATH,'//h1[contains(text(),"Violation Search")]'),
    'staleLocator2' : (By.XPATH,'//h1[contains(text(),"Violation Search Result")]'),
    'buttonLocator' : (By.XPATH,'//input[@value="Query"]'),
    'frameParamters' : {'useFrames' : True, 'frameLocator' : (By.XPATH, '//frame[@name="fraRxL"]') },
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : 'Violation Search Results',
    'outputLocator' : (By.XPATH,'//BODY/P[contains(text(),"Record")]'),
    'resultIndexParameters' : {'regex' : "Records \d+ to \d+ of (\d+)", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'LP_Repeats_Count_short.csv',
    #'dataInFileName' : 'LP_Repeats_Count.csv',
    #'dataInFileName' : 'LP_Repeats_Count_200.csv',
    'dataOutFileName' : 'vps_find_vio_by_lp.csv',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

def dataIO(driver, parameters):
    delay = parameters['delay']
    vioPageTextLocator = (By.XPATH, '//TD/H1[contains(text(),"Violator Maintenance")]')
    # pause on next line for entry of credentials, and window navigation.
    startWindow = findTargetPage(driver, findStartWindowDelay, vioPageTextLocator)
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
            plateString = cleanUpString(rawString)
            inputLocator = (By.XPATH, '//input[@id = "P_LIC_PLATE_NBR"]')
            element = findElementOnPage(driver, delay, inputLocator)
            submitted = fillFormAndSubmit(driver, startWindow, element, plateString, parameters) # why so slow?
            time.sleep(1)  #page may not be there yet!  how long to wait?
            pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), vioPageTextLocator)
            foundFrame = findAndSelectFrame(driver, delay, "fraRL")
            #time.sleep(1)  #text may not be there yet!  how long to wait?
  #lost here          text = getTextResults(driver, delay, plateString, parameters, "fraRL")
            if text is not None: # if there is text, process it
                sys.stdout.write(plateString + ", " + str(text) + '\n')
                outfile.write(plateString + ", " + str(text) + '\n')
                outfile.flush()
            # navigate to search position
            if type(parameters['buttonLocator']) is None: # no button, start at 'top' of the page
                driver.switch_to_default_content()
            else: # there is a button. find it/click it/wait for page to load
                clicked = findAndClickButton(driver, delay, parameters)
                pageLoaded = newPageElementFound(driver, delay, None, parameters['staleLocator'])

    print "main: Finished parsing plate file."

if __name__ == '__main__':

    parameters = violatorSearch()

    findStartWindowDelay = 3
    print parameters['operatorMessage']
    regexPattens = loadRegExPatterns()
    driver = openBrowser(parameters['url'])
    dataIO(driver, parameters)
    driver.close()

