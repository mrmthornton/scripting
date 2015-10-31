#-------------------------------------------------------------------------------
# Name:        VPS_VioFind.py
# Purpose:     Query "Violation Search" for a name, with broad search latitude.
#              For each violator found, match street address.
#              Allow operator to decide on close matches. (what constitutes close?)
#              Add licence plate to licence plate list.
#              Add comment, with specific information for this group.
#              Add annotation to each violator in the licence plate list for this group.
# Author:      mthornton
#
# Created:     2015JUL27
# Updates:     2015AUG07
# Copyright:   (c) michael thornton 2015
#-------------------------------------------------------------------------------

import re
import io
import csv
import string

# stringValue = stringValue.replace(',' , '') # remove any commas
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC

import string

def timeout(msg="Took too much time!"):
    print msg

driver = webdriver.Ie()
driver.maximize_window()
delay = 5 # seconds

def openVio():
    url = 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp'  # start URL
    header = 'Violator Maintenance'     # target header
    driver.get(url)

    while True:
        form = False
        windows = driver.window_handles
        for window in windows:
            print window
            try:
                driver.switch_to.window(window)
                #locator = (By.XPATH, '//h1[@text="VIOLATOR MAINTENANCE"]')
                locator = (By.CSS_SELECTOR, 'h1')
                element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(locator))
                if element:
                    try:
                        locator = (By.NAME, "P_LIC_PLATE_NBR")
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
    searchKey = "42W0012"
    form.send_keys(searchKey)
    form.submit()

try:
    locator = (By.XPATH, '//div[@id="search-results"]')
    results = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))

    for e in results:
        s = filter(lambda x: x in string.printable, e.text)
        print s

    with open('results.txt', 'w') as pageFile:  # open the file to store html
        for e in results:
            pageFile.write(filter(lambda x: x in string.printable, e.text))        # write to file

except TimeoutException:
    timeout()

def main():

    openVio()
    with open('VioFindInput.csv', 'r') as infile, open('VioFindOutput.txt', 'a') as outfile:
        outfile.truncate()
        csvInput = csv.reader(infile)
        for row in csvInput:


            outfile.write(nameString + plateStrings)
            outfile.flush()
    print "main: Finished parsing TxDot file."

if __name__ == '__main__':
    main()
