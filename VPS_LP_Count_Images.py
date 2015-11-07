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
# Updates:     2015 NOV 03
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
from VPS_LIB import findTargetPage
from VPS_LIB import getTextResults
from VPS_LIB import loadRegExPatterns
from VPS_LIB import openBrowser
from VPS_LIB import returnOrClick
from VPS_LIB import timeout
from VPS_LIB import waitForNewPage

import re
import io
import csv
import sys
import string

def parseString(inputString,indexPattern, targetPattern, segment="all"): # segment may be start, end, or all
    # the iterator is used to search for all possible target pattern instances
    found = indexPattern.search(inputString)
    if found != None:
        indexStart = found.start()
        indexEnd = found.end()
        print "parseString: found start", indexStart #debug statement
        iterator = targetPattern.finditer(inputString)
        for found in iterator:
            if found.start() > indexStart and found != None:
                targetStart = found.start()
                targetEnd = found.end()
                print "findStartEnd: found end", targetStart #debug statement
                return inputString[indexEnd:targetEnd:]
    return None

def dataIO(driver, parameters):
    with open(parameters['dataInFileName'], 'r') as infile, open(parameters['dataOutFileName'], 'a') as outfile:
        outfile.truncate()
        csvInput = csv.reader(infile)
        for row in csvInput:
            rawString = row[0]
            if rawString == "" or rawString == 0:  #end when LP does not exist
                break
            plateString = cleanUpLicensePlateString(rawString)
            window, ReferenceElement = findTargetPage(driver, parameters['startPageTextLocator'], parameters['startPageVerifyText'])
            element = findElementOnPage(driver, parameters['inputLocator'])
            fillFormAndSubmit(driver, window, element, plateString, parameters)
            waitForNewPage(driver, ReferenceElement)
            text = getTextResults(driver, window, plateString, parameters)
            beginPattern = re.compile(parameters['resultIndexParameters']['index'])
            numCommaPattern = re.compile('[0-9,]+')
            if text!= None:
                stringSegment = parseString(text, beginPattern, numCommaPattern, "all")
                sys.stdout.write(plateString + ", " + str(stringSegment) + '\n')
                outfile.write(plateString + ", " + str(stringSegment) + '\n')
                outfile.flush()
            driver.back() # go back to 'startPage'
    print "main: Finished parsing plate file."


def googleValues():
    parameters = {
    'url' : 'http://www.google.com', # initial URL
    'operatorMessage' : "Google test: no operator actions needed.",
    'startPageTextLocator' : (By.XPATH,'//input[@value = "Google Search"]'),
    'startPageVerifyText' : '',
    'inputLocator' : (By.XPATH,'//input[@name = "q"]'),
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : '',
    'outputLocator' : (By.ID, "resultStats"),
    'resultIndexParameters' : {'index' : "About ", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'plates.csv',
    'dataOutFileName' : 'platesOut.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

def sigmaAldrichValues():
    parameters = {
    'url' : 'http://www.sigmaaldrich.com/united-states.html', # initial URL
    'operatorMessage' : "sigmaaldrich test run:  no operator actions needed.",
    'startPageTextLocator' : (By.XPATH, '//a'),
    'startPageVerifyText' : 'Hello. Sign in.',
    'inputLocator' : (By.XPATH,'//input[@name = "Query"]'),
    'resultPageTextLocator' : (By.XPATH, '//p[contains(text(),"matches found for"]'),
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
    'url' : 'http://www.hntb.com/about', # initial URL
    'operatorMessage' : "HNTB test run:  no operator actions needed.",
    'startPageTextLocator' : (By.XPATH, '//h2'),
    'startPageVerifyText' : 'About HNTB',
    'inputLocator' : (By.XPATH,'//input[@name = "s"]'),
    #'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
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
    'url' : 'http://www.cisco.com/univercd/cc/td/doc/product/voice/c_ipphone/index.html', # initial URL
    'operatorMessage' : "Cisco test: no operator actions needed.",
    'startPageTextLocator' : (By.XPATH, '//DIV/H1[@class="title-section"]'),
    'startPageVerifyText' : '404 Page Not Found',
    'inputLocator' : (By.XPATH, '(//input[@id = "searchPhrase"] | //input[@id = "search-Phrase search-Phrase-only"])'),
    'resultPageTextLocator' : (By.XPATH, '//H2[@class="title-page"]'),
    'resultPageVerifyText' : 'Search Results',
    'outputLocator' : (By.CLASS_NAME,'searchStatus'),
    'resultIndexParameters' : {'index' : "of ", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'plates.csv',
    'dataOutFileName' : 'platesOut.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

def productionValues():
    parameters = {
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    'operatorMessage' : "Use debug mode, open VPS, new violator search window, and run to completion",
    'startPageTextLocator' : (By.XPATH, '//TD/H1'),
    'startPageVerifyText' : 'Violation Search',
    'inputLocator' : (By.XPATH, '//input[@id = "P_LIC_PLATE_NBR"]'),
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : 'Violation Search Results',
    'outputLocator' : (By.XPATH,'//BODY/P[contains(text(),"Record")]'),
    'resultIndexParameters' : {'index' : "of ", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : 'LP_Repeats_Count.csv',
    'dataOutFileName' : 'LP_Repeats_Count_Out.txt',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters

if __name__ == '__main__':

    parameters = googleValues()
    #parameters = sigmaAldrichValues()
    #parameters = hntbValues()
    #parameters = ciscoValues() # should work on production systems
    #parameters = productionValues()

    print parameters['operatorMessage']
    loadRegExPatterns()
    driver = openBrowser(parameters['url'])
    dataIO(driver, parameters)
    driver.close()
