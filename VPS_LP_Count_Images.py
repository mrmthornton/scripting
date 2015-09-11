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


def openBrowser():
    driver = webdriver.Ie()
    #driver.maximize_window()
    #url = 'http://www.hntb.com'       # target URL
    url = 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp'  # start URL
    driver.get(url)
    return driver


def waitForSelectedPage(driver):
    # wait for page to load
    #header = 'HNTB SOLUTIONS'      # target header
    #header = 'Violation Search'     # target header
    header = 'VIOLATION SEARCH'     # target header
    delay = 60 # seconds
    while True:
        form = False
        windows = driver.window_handles
        for window in windows:
            print window
            try:
                #element = WebDriverWait(driver, 5).until(EC.title_contains(title))
                locator = (By.XPATH, '//h1')
                #locator = (By.CSS_SELECTOR, 'h1')
                elems = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
                for element in elems:
                    if element.text == header:     # why all upper case?
                        print element.text
                        try:
                            locator = (By.NAME, "search_block_form")
                            form = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
                            break
                        except TimeoutException:
                            timeout("no search block found")
                            continue
            except TimeoutException:
                timeout('"' + header + '" window not found')
                continue
                if form:
                    break


def getCount(driver, plateString):
    loginDelay = 30 # seconds
    delay = 5 # seconds
    title = 'About Us | HNTB.com'     # target page


import re
import io
import csv
import sys
import string

# stringValue = stringValue.replace(',' , '') # remove any commas

def dataIO(driver):

    with open('LP_Repeats_Count.csv', 'r') as infile, open('LP_Repeats_Count_Out.txt', 'a') as outfile:
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
    driver = openBrowser()
    waitForSelectedPage(driver)
    #driver = webdriver.Ie()
    dataIO(driver)
