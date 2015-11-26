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
# Updates:     2015 NOV 20
# Copyright:   (c) michael thornton 2015
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC

from VPS_LIB import cleanUpLicensePlateString
from VPS_LIB import findElementOnPage
from VPS_LIB import fillFormAndSubmit
from VPS_LIB import findAndSelectFrame
from VPS_LIB import findAndClickButton
from VPS_LIB import findTargetPage
from VPS_LIB import getTextResults
from VPS_LIB import loadRegExPatterns
from VPS_LIB import newPageIsLoaded
from VPS_LIB import openBrowser
from VPS_LIB import parseString
from VPS_LIB import returnOrClick
from VPS_LIB import timeout

import re
import io
import csv
import sys
import string

def googleValues():
    parameters = {
    'delay' : 5,
    'url' : 'http://www.google.com', # initial URL
    'operatorMessage' : "Google test: no operator actions needed.",
    'startPageTextLocator' : (By.XPATH,'//input[@value = "Google Search"]'),
    'startPageVerifyText' : '',
    'inputLocator' : (By.XPATH,'//input[@name="q"]'),
    'staleLocator' : None,
    'buttonLocator' : (By.XPATH,'//button[@value="Search"]'),
    'frameParamters' : {'useFrames' : False},
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : '',
    'outputLocator' : (By.XPATH, '//div[@id="resultStats"][contains(text(),"About")]'),
    'resultIndexParameters' : {'index' : "About ", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'google.csv',
    'dataOutFileName' : 'output.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

def sigmaAldrichValues():
    parameters = {
    'delay' : 5,
    'url' : 'http://www.sigmaaldrich.com/united-states.html', # initial URL
    'operatorMessage' : "sigmaaldrich test run:  no operator actions needed.",
    'startPageTextLocator' : (By.XPATH, '//a'),
    'startPageVerifyText' : 'Hello. Sign in.',
    'inputLocator' : (By.XPATH,'//input[@name = "Query"]'),
    'staleLocator' : (By.XPATH,'//A[contains(text(),"query?")]'),
    'frameParamters' : {'useFrames' : False},
    'resultPageTextLocator' : (By.XPATH, '//p[contains(text(),"matches found for")]'),
    'resultPageVerifyText' : '',
    'outputLocator' : (By.XPATH, '//p[@class="resultsFoundText"]'),
    'resultIndexParameters' : {'index' : "matches found for", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'plates.csv',
    'dataOutFileName' : 'platesOut.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

def hntbValues():
    parameters = {
    'delay' : 5,
    'url' : 'http://www.hntb.com', # initial URL
    'operatorMessage' : "HNTB test run:  run in debug mode, click magnifying glass.",
    'startPageTextLocator' : (By.XPATH, '//h2'),
    'startPageVerifyText' : 'About HNTB',
    'inputLocator' : (By.XPATH,'//input[@name = "s"]'),
    'frameParamters' : {'useFrames' : False},
    'resultPageTextLocator' : (By.XPATH, '//TITLE'),
    'resultPageVerifyText' : 'Search Result',
    'outputLocator' : (By.ID, "resultStats"),
    'resultIndexParameters' : {'index' : " Results", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'plates.csv',
    'dataOutFileName' : 'platesOut.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

def ciscoValues():
    parameters = {
    'delay' : 5,
    'url' : 'http://www.cisco.com/univercd/cc/td/doc/product/voice/c_ipphone/index.html', # initial URL
    'operatorMessage' : "Cisco test: no operator actions needed.",
    'startPageTextLocator' : (By.XPATH, '(//DIV/H1[@class="title-section"] | //div/h1[@class="title-section title-section-only"])'),
    'startPageVerifyText' : '404 Page Not Found',
    'inputLocator' : (By.XPATH, '(//input[@id = "searchPhrase"] | //input[@id = "search-Phrase search-Phrase-only"])'),
    'frameParamters' : {'useFrames' : False},
    'resultPageTextLocator' : (By.XPATH, '//H2[@class="title-page"]'),
    'resultPageVerifyText' : 'Search Results',
    'outputLocator' : (By.CLASS_NAME,'searchStatus'),
    'resultIndexParameters' : {'index' : "of ", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'plates.csv',
    'dataOutFileName' : 'platesOut.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

def theInternetNavigate():
    parameters = {
    'delay' : 5,
    'url' : 'http://the-internet.herokuapp.com/dynamic_controls', # initial URL
    'operatorMessage' : "the-internet test: no operator actions needed.",
    'startPageTextLocator' : (By.XPATH, '//H4[contains(text(), "Dynamic Controls")]'),
    'startPageVerifyText' : '',
    'inputLocator' : None,
    'staleLocator' : None,
    'buttonLocator' : (By.XPATH, '//button[@id="btn"]'),
    'frameParamters' : {'useFrames' : False },
    'resultPageTextLocator' : (By.XPATH, '//input[@id="checkbox"]'),
    'resultPageVerifyText' : None,
    'outputLocator' : None,
    'resultIndexParameters' : {'index' : '', 'selector' : ''},  # head, tail, or all
    'dataInFileName' : 'google.csv',
    'dataOutFileName' : 'output.txt',
    'returnOrClick' : 'click', # use Return or Click to submit form
    }
    return parameters

def theInternetFrames():
    parameters = {
    'delay' : 5,
    'url' : 'http://the-internet.herokuapp.com/nested_frames', # initial URL
    'operatorMessage' : "the-internet test: no operator actions needed.",
    'startPageTextLocator' : (By.XPATH, '//frameset'),
    'startPageVerifyText' : '',
    'inputLocator' : None,
    'staleLocator' : None,
    'buttonLocator' : None,
    'frameParamters' : {'useFrames' : True, 'frameLocator' : [(By.XPATH, '//frame[@name="frame-top"]'),
                                                             (By.XPATH, '//frame[@name="frame-middle"]')]},
    'resultPageTextLocator' : (By.XPATH, '//frame[@name="frame-top"]'),
    'resultPageVerifyText' : None,
    'outputLocator' : None,
    'resultIndexParameters' : {'index' : "", 'selector' : ''},  # head, tail, or all
    'dataInFileName' : 'google.csv',
    'dataOutFileName' : 'output.txt',
    'returnOrClick' : 'click', # use Return or Click to submit form
    }
    return parameters

def violatorSearch():
    parameters = {
    'delay' : 5,
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    'operatorMessage' : "Use debug mode, open VPS, new violator search window, and run to completion",
    'startPageTextLocator' : (By.XPATH, '//TD/H1'),
    'startPageVerifyText' : 'Violation Search',
    'inputLocator' : (By.XPATH, '//input[@id = "P_LIC_PLATE_NBR"]'),
    'staleLocator' : (By.XPATH, '//TD/H1[contains(text(),"Violation Search")]'),
    'buttonLocator' : (By.XPATH,'//input[@value="Query"]'),
    'frameParamters' : {'useFrames' : True, 'frameLocator' : [(By.XPATH, '//frame[@name="fraRL"]')] },
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : 'Violation Search Results',
    'outputLocator' : (By.XPATH,'//BODY/P[contains(text(),"Record")]'),
    'resultIndexParameters' : {'index' : "of ", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'LP_Repeats_Count.csv',
    'dataOutFileName' : 'LP_Repeats_Count_Out.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

def dataIO(driver, parameters):
    beginPattern = re.compile(parameters['resultIndexParameters']['index'])
    numCommaPattern = re.compile('[0-9,]+')
    delay = parameters['delay']
    startWindow, ReferenceElement = findTargetPage(driver, delay, parameters['startPageTextLocator'], parameters['startPageVerifyText'])
    with open(parameters['dataInFileName'], 'r') as infile, open(parameters['dataOutFileName'], 'a') as outfile:
        outfile.truncate()
        csvInput = csv.reader(infile)
        for row in csvInput:
            rawString = row[0]
            if rawString == "" or rawString == 0:  #end when LP does not exist
                break
            plateString = cleanUpLicensePlateString(rawString)
            #print plateString # debug
            element = findElementOnPage(driver, delay, parameters['inputLocator'])
            goesStaleElement = findElementOnPage(driver, delay, (By.XPATH, '//TD/H1[contains(text(),"Violation Search")]'))
            fillFormAndSubmit(driver, startWindow, element, plateString, parameters)
            wentStale = newPageIsLoaded(driver, delay, goesStaleElement)
            #wait for page load
            foundFrame = findAndSelectFrame(driver, delay, parameters)
            text = getTextResults(driver, 10, plateString, parameters)
            if text!= None:
                stringSegment = parseString(text, beginPattern, numCommaPattern, "all")
                sys.stdout.write(plateString + ", " + str(stringSegment) + '\n')
                outfile.write(plateString + ", " + str(stringSegment) + '\n')
                outfile.flush()
            # navigate to search page
            goesStaleElement = findElementOnPage(driver, delay, parameters['outputLocator'])
            clicked = findAndClickButton(driver, delay, parameters)
            if clicked:
                wentStale = newPageIsLoaded(driver, delay, goesStaleElement)
                #wait for page load
            else:
                driver.switch_to_default_content()

    print "main: Finished parsing plate file."

if __name__ == '__main__':

    #parameters = googleValues()
    #parameters = sigmaAldrichValues()
    #parameters = hntbValues()
    #parameters = ciscoValues() # should work on production systems
    parameters = theInternetNavigate()
    #parameters = theInternetFrames() # sites for testing
    parameters = violatorSearch()

    print parameters['operatorMessage']
    loadRegExPatterns()
    driver = openBrowser(parameters['url'])
    dataIO(driver, parameters)
    driver.close()
