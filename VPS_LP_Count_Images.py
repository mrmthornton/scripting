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

import re
import io
import csv
import sys
import string

def dataIO(driver, dataInFileName, dataOutFileName, window, element, txtLocator=("","")):
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
            plateString = plateString.replace(',' , '\n') # replace , with \n
            for n in range(10):
                plateString = plateString.replace('\n\n' , '\n') # replace \n\n, with \n

            text = getText(driver, window, element, plateString, txtLocator)
            sys.stdout.write(plateString + ", " + str(text) + '\n')
            outfile.write(plateString + ", " + str(text) + '\n')

            outfile.flush()
    print "main: Finished parsing plate file."


if __name__ == '__main__':

    ## testing with google site
    pageLocator = (By.XPATH,'//input[@value = "Google Search"]')
    targetText = ''      # target text
    url = 'http://www.google.com'       # target URL
    dataInFileName = 'plates.csv'
    dataOutFileName = 'platesOut.txt'
    elemLocator = (By.XPATH,'//input[@name = "q"]')
    RoC = 'R' # use Return or Click to submit form
    textLocator = (By.ID, "resultStats")

    ## testing with hntb site
    #pageLocator = (By.XPATH, '//h2')
    #targetText = 'About HNTB'      # target text
    #url = 'http://www.hntb.com'       # target URL
    #dataInFileName = 'plates.csv'
    #dataOutFileName = 'platesOut.txt'
    #elemLocator = (By.XPATH,'//input[@name = "s"]')
    #RoC = 'R' # use Return or Click to submit form
    #textLocator = (By.ID, "resultStats")

    ## production values
    #pageLocator = (By.XPATH, '//TD/H1')
    #targetText = 'Violation Search'     # target text
    #url = 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp'  # start URL
    #dataInFileName = 'LP_Repeats_Count.csv'
    #dataOutFileName = 'LP_Repeats_Count_Out.txt'
    #elemLocator = (By.XPATH,'//input[@id = "P_LIC_PLATE_NBR"]')
    #RoC = 'R' # use Return or Click to submit form
    #textLocator = (By.ID, "resultStats")

    driver = openBrowser(url)
    window, element = waitForSelectedPage(driver, targetText, pageLocator)

    window, element = findElementOnPage(driver, window, elemLocator)

    dataIO(driver, dataInFileName, dataOutFileName, window, element, textLocator)
