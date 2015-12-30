#-------------------------------------------------------------------------------
# Name:        TxDotQuery
# Purpose:     establish connection to TXDMV RTS database
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
delay=30

def timeout():
    print "TxDotQuery: timeout!"
    quit()

def credentials():
    # Go to the main web page and wait while the user enters credentials
<<<<<<< HEAD
    url = 'https://mvdinet.txdmv.govX'
=======
    url = 'https://mvdinet.txdmv.gov'
>>>>>>> c4a95a9e05e29d475bb078e903c178926551f7b2
    driver.get(url)

def connect():
    try:
        locator =(By.NAME,'plate_1')
        plateField = WebDriverWait(driver, delay,20).until(EC.presence_of_element_located(locator))
    except TimeoutException:
        timeout()

def query(plate):
    try:
        locator =(By.NAME,'plate_1')
        plateField = WebDriverWait(driver, delay,2).until(EC.presence_of_element_located(locator))
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
    connect()
    print query("12345TX")
