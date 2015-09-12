#-------------------------------------------------------------------------------
# Name:        MultiColToSingle.py
# Purpose:     get a name from column 1 and multiple plates from column 2,
#              create a new spreadsheet with a single column,
#              where each name is followed by the associated  plates.
#              save to text file, in CSV format.
# Author:      mthornton
#
# Created:     2015jul27
# Updates:     2015jul28
# Copyright:   (c) michael thornton 2015
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC


def timeout(msg="Took too much time!"):
    print msg


def openBrowser(url):
    driver = webdriver.Ie()
    #driver.maximize_window()
    driver.get(url)
    return driver


def waitForSelectedPage(driver, targetText, locator):
    # wait for page to load
    delay = 5 # seconds
    while True:
        for window in driver.window_handles:  # test each window for locator element
            driver.switch_to_window(window)
            print window
            try:
                elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
                for element in elems:       # test each element for target
                    if element.text == targetText:   #all upper case
                        print element.text
                        return window
            except TimeoutException:
                timeout('locator element not found')
                continue


def getCount(driver, plateString):
    loginDelay = 30 # seconds
    delay = 5 # seconds
    title = 'About Us | HNTB.com'     # target page


import re
import io
import csv
import sys
import string

def dataIO(driver, dataInFileName, dataOutFileName, window):
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

            count = 0
            #count = getCount(driver, plateString)

            sys.stdout.write(plateString + ", " + str(count) + '\n')
            outfile.write(plateString + ", " + str(count) + '\n')

            outfile.flush()
    print "main: Finished parsing plate file."


if __name__ == '__main__':

    ## testing with google site
    #url = 'http://www.google.com'       # target URL
    #locator = (By.XPATH, '//div')
    #targetText = 'about ...'      # target text
    #dataInFileName = 'plates.csv'
    #dataOutFileName = 'platesOut.txt'

    ## testing with hntb site
    url = 'http://www.hntb.com'       # target URL
    locator = (By.XPATH, '//h1')
    targetText = 'HNTB SOLUTIONS'      # target text
    dataInFileName = 'plates.csv'
    dataOutFileName = 'platesOut.txt'

    ## production values
    #targetText = 'Violation Search'     # target text
    #targetText = 'VIOLATION SEARCH'     # target text
    #locator = (By.XPATH, '//h1')
    #url = 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp'  # start URL
    #dataInFileName = 'LP_Repeats_Count.csv'
    #dataOutFileName = 'LP_Repeats_Count_Out.txt'


    driver = openBrowser(url)
    foundWindow = waitForSelectedPage(driver, targetText, locator)
    dataIO(driver, dataInFileName, dataOutFileName, foundWindow)
