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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC

from VPS_LIB import *

import sys
import string
import time

def holdOpen():
    parameters = {
    'delay' : 15,
    'url' : 'https://google.com', # initial URL
    'operatorMessage' : "Use debug mode, enter credentials and run to completion",
    'startPageTextLocator' : (By.XPATH, '//TD/H1[contains(text(),"Violation Search")]'),
    'inputLocator' : (By.XPATH, '//input[@id = "P_LIC_PLATE_NBR"]'),
    'staleLocator' : (By.XPATH,'//h1[contains(text(),"Violation Search")]'),
    'staleLocator2' : (By.XPATH,'//h1[contains(text(),"Violation Search Result")]'),
    'buttonLocator' : (By.XPATH,'//input[@value="Query"]'),
    'frameParamters' : {'useFrames' : False},
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : 'Violation Search Results',
    'outputLocator' : (By.XPATH,'//BODY/P[contains(text(),"Record")]'),
    'resultIndexParameters' : {'regex' : "Records \d+ to \d+ of (\d+)", 'selector' : 'tail'},  # head, tail, or all
    'dataOutFileName' : 'LP_Repeats_Count_Out.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters


if __name__ == '__main__':


    delay = 3
    #url - 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp'
    #url = 'https://www.google.com'
    url = 'http://intranet/SitePages'
    regexPattens = loadRegExPatterns()
    driver = openBrowser(url)
    handles = driver.window_handles
    print handles
    print len(handles)
    elementLocator = (By.XPATH, '//input[@title="Search Everything"]')
    foundElem = findElementOnPage(driver, delay, elementLocator)
    foundElem.send_keys(Keys.CONTROL + 't')
    print driver.current_window_handle


    handles = driver.window_handles
    print len(handles)
    print 'start'
    count = 5
    while count>0:
        print count
        time.sleep(1)
        count -=1
    driver.close()

