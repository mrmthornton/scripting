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
# Updates:     2015jul14
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
                        return window, element
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
    #url = 'http://www.hntb.com'       # target URL
    #locator = (By.XPATH, '//h1')
    #targetText = 'HNTB SOLUTIONS'      # target text
    #dataInFileName = 'plates.csv'
    #dataOutFileName = 'platesOut.txt'

    ## production values
    id = "P_LIC_PLATE_NBR"
    #targetText = ""
    #works#locator = (By.ID, id)
    locator = (By.XPATH, '//TD/H1')
    targetText = 'Violation Search'     # target text
    #targetText = 'VIOLATION SEARCH'     # target text
    url = 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp'  # start URL
    dataInFileName = 'LP_Repeats_Count.csv'
    dataOutFileName = 'LP_Repeats_Count_Out.txt'


    driver = openBrowser(url)
    window, element = waitForSelectedPage(driver, targetText, locator)

    driver.switch_to_window(window)
    element.send_keys("test")
    element.submit()

    dataIO(driver, dataInFileName, dataOutFileName, foundWindow)
