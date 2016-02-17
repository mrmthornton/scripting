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

from TxDot_LIB import *
from VPS_LIB import *

if __name__ == '__main__':
    #create an instance of IE and set some options
    driver = webdriver.Ie()
    delay = 15
    findStartWindowDelay = 5
    url = 'https://mvinet.txdmv.gov'
    driver.get(url)
    #startPageLocator = (By.XPATH,'//H3[contains(text(),"VTR Inquiry")]')
    startPageLocator = (By.XPATH,'//title[contains(text(),"Vehicle")]')
    startPageHandle = startWindow = findTargetPage(driver, findStartWindowDelay, startPageLocator)
    #   "v-textfield v-widget iw-child v-textfield-iw-child iw-mandatory v-textfield-iw-mandatory v-has-width"
    inputFieldLocator =(By.XPATH, '//nobr[contains(text(), "Enter Plate Number")]')
    element = findElementOnPage(driver, delay, inputFieldLocator)
    print element.text
    element.clear()
    element.send_keys(textForForm)
    element.send_keys('\n')
