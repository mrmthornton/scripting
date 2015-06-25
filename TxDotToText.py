#-------------------------------------------------------------------------------
# Name:        TxDotToText
# Purpose:     gather output from TXDMV RTS database, save to CSV text file
#
# Author:      mthornton
#
# Created:     24/11/2014
# Copyright:   (c) mthornton 2014, 2015
#------------------------------------------------------------------------------
# open a page
# fill the search field and submit
# scrape the results
# close the page

# works on win7, ie10
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#create an instance of IE and set some options
driver = webdriver.Ie()
driver.maximize_window()
delay=10

def timeout():
    print "TxDotQuery: timeout!"
    quit()

def credentials():
    # Go to the main web page and wait while the user enters credentials
    url = 'https://mvdinet.txdmv.govX'
    driver.get(url)

def query(plate):
    try:
        locator =(By.NAME,'plate_1')
        plateField = WebDriverWait(driver, delay,20).until(EC.presence_of_element_located(locator))
        plateField.clear()
        plateField.send_keys(plate)
        plateField.submit()
    except TimeoutException:
        timeout()

    try:
        locator = (By.XPATH, '//pre')
        results = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(locator))
    except TimeoutException:
        timeout()

    return results


if __name__ == '__main__':
    credentials()
    print query("12345TX")
    with open('dealerPlates.csv', 'r') as plateFile:
        csvInput = csv.reader(plateFile)
        plates = [row[0] for row in csvInput]

    with open('txdotText.txt', 'a') as outfile:
        outfile.truncate()
        for plate in plates:
            fileString = query(plate)
            try:
                outfile.write(fileString)
                outfile.write('\n\n------------------------------------\n\n')
            except:
                print "TxDotToText: error"
        outfile.flush()
    print "TxDotToText: Finished writing file."
