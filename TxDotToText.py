#-------------------------------------------------------------------------------
# Name:        TxDotToText
# Purpose:     gather output from TXDMV RTS database, save to text file
#
# Author:      mthornton
#
# Created:     24/11/2014
# Modified:    03AUG2016
# Copyright:   (c) mthornton 2014, 2015, 2016
# input(s)     plates.csv
# output(s)    txdotText.txt
#------------------------------------------------------------------------------
# open a page
# fill the search field and submit
# scrape the results
# close the page

# tested on win7, ie10, IE11
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from TxDot_LIB import query

if __name__ == '__main__':
    #create an instance of IE and set some options
    driver = webdriver.Ie()
    delay=10
    url = 'https://mvinet.txdmv.gov'
    driver.get(url)

    # read input values
    with open('plates.csv', 'r') as plateFile:
        csvInput = csv.reader(plateFile)
        plates = [row[0] for row in csvInput]

    # loop over input values, writing to  outfile
    with open('txdotText.txt', 'a') as outfile:
        outfile.truncate()
        for plate in plates:
            fileString = query(driver, delay, plate)
            try:
                outfile.write(fileString)
                outfile.write('\n\n------------------------------------\n\n')
            except:
                print "TxDotToText: error"
        outfile.flush()
    print "TxDotToText: Finished writing file."
    driver.close()