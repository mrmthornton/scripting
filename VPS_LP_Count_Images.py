#-------------------------------------------------------------------------------
# Name:        VPS_LP_Count_Images.py
# Purpose:     Examine web pages until the VPS Violation Search page is found.
#              enter a licence plate in the search box
#              find the text number of images
#              write the licence plate and number of images to the output file.
#
# Author:      mthornton
#
# Created:     2015aug01
# Updates:     2015sep22
# Copyright:   (c) michael thornton 2015
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC

from VPS_LIB import timeout
from VPS_LIB import returnOrClick
from VPS_LIB import openBrowser
from VPS_LIB import waitForSelectedPage
from VPS_LIB import findElementOnPage
from VPS_LIB import getText
from VPS_LIB import loadRegExPatterns

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
        #print "parseString: found start", indexStart #debug statement
        iterator = targetPattern.finditer(inputString)
        for found in iterator:
            if found.start() > indexStart and found != None:
                targetStart = found.start()
                targetEnd = found.end()
                #print "findStartEnd: found end", targetStart #debug statement
                return inputString[indexEnd:targetEnd:]
    return None

def dataIO(driver, dataInFileName, dataOutFileName, window, element, txtLocator=("",""), targetText=""):
    with open(dataInFileName, 'r') as infile, open(dataOutFileName, 'a') as outfile:
        outfile.truncate()
        csvInput = csv.reader(infile)
        for row in csvInput:
            plateString = row[0]
            if plateString == "" or plateString == 0:  #end when LP does not exist
                break
            plateString = plateString.replace(' ' , '') # remove any spaces
            plateString = plateString.replace('"' , '') # remove any quotes
            plateString = plateString.replace('\t' , '') # remove any tabs
            plateString = plateString.replace(',' , '\n') # replace comma with \n
            for n in range(10):
                plateString = plateString.replace('\n\n' , '\n') # replace \n\n, with \n

            text = getText(driver, window, element, plateString, txtLocator, targetText)
            beginPattern = re.compile(targetText)
            numberCommaPattern = re.compile('[0-9,]+')
            linePattern = re.compile('^.+')
            eolPattern = re.compile('$')
            stringSegment = parseString(text, beginPattern, eolPattern, "all")
            sys.stdout.write(plateString + ", " + str(stringSegment) + '\n')
            outfile.write(plateString + ", " + str(stringSegment) + '\n')

            outfile.flush()
            driver.back()

            # return to query window and test for correct location
            # using waitForSelectedPage ? and stored url? or return vector ?

    print "main: Finished parsing plate file."

if __name__ == '__main__':

    ## testing with google site
    #print "Google test: no operator actions needed."
    #pageLocator = (By.XPATH,'//input[@value = "Google Search"]')
    #targetText = ''      # target text
    #url = 'http://www.google.com'       # target URL
    #dataInFileName = 'plates.csv'
    #dataOutFileName = 'platesOut.txt'
    #elemLocator = (By.XPATH,'//input[@name = "q"]')
    #RoC = 'R' # use Return or Click to submit form
    #textLocator = (By.ID, "resultStats")
    #resultIndexText = "About "

    ## testing with hntb site
    #print "HNTB test run: use debug mode?, open new window with About link."
    #print "click on search icon, continue run. "
    #print "results are displayed in a different window. "
    #pageLocator = (By.XPATH, '//h2')
    #targetText = 'About HNTB'      # target text
    #url = 'http://www.hntb.com'       # target URL
    #dataInFileName = 'plates.csv'
    #dataOutFileName = 'platesOut.txt'
    #elemLocator = (By.XPATH,'//input[@name = "s"]')
    #RoC = 'R' # use Return or Click to submit form
    #textLocator = (By.CSS_SELECTOR, 'p:contains("HNTB")')
    #resultIndexText = 'HNTB'

    ## testing with hntb site
    #print "The Colony library."
    #print "No operator actions needed."
    #print "Fails after one successful pass."
    #pageLocator = (By.XPATH, '//h1')
    #targetText = 'The Colony Public Library'      # target text
    #url = 'http://thecolony.ploud.net/'       # target URL
    #dataInFileName = 'plates.csv'
    #dataOutFileName = 'platesOut.txt'
    #elemLocator = (By.XPATH,'//input[@name = "SearchableText"]')
    #RoC = 'R' # use Return or Click to submit form
    #textLocator = (By.XPATH, '//*[contains(text(), "results ")]')
    #resultIndexText = 'No results'

    ## production values
    #print "Use debug mode, open VPS, new violator search window, "
    #print "and run to completion"
    #pageLocator = (By.XPATH, '//TD/H1')
    #targetText = 'Violation Search'     # target text
    #url = 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp'  # start URL
    #dataInFileName = 'LP_Repeats_Count.csv'
    #dataOutFileName = 'LP_Repeats_Count_Out.txt'
    #elemLocator = (By.XPATH,'//input[@id = "P_LIC_PLATE_NBR"]')
    #RoC = 'R' # use Return or Click to submit form
    #textLocator = (By.ID, "resultStats")
    #resultIndexText = "Records "

    loadRegExPatterns()
    driver = openBrowser(url)
    window, element = waitForSelectedPage(driver, targetText, pageLocator)

    window, element, urlVector = findElementOnPage(driver, window, elemLocator)

    dataIO(driver, dataInFileName, dataOutFileName, window, element, textLocator, resultIndexText)
