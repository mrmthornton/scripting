#-------------------------------------------------------------------------------
# Name:        UTIL_LIB.py
# Purpose:     A library for common behaviors.
#              extracted from VPS_LIB
# Author:      mthornton
#
# Created:     2015 AUG 01
# Updates:     2017 APR 08
# Copyright:   (c) michael thornton 2015, 2016, 2017
#-------------------------------------------------------------------------------


import re
from selenium import webdriver 
import time

from Tkinter import Tk
#import tkMessageBox
import tkMessageBox

def cleanUpString(messyString):
    cleanString = messyString.replace(' ' , '') # remove any spaces
    cleanString = cleanString.replace('"' , '') # remove any double quotes
    cleanString = cleanString.replace('\t' , '') # remove any tabs
    cleanString = cleanString.replace(',' , '\n') # replace comma with \n
    for n in range(10):            # replace multiple newlines with a single \n
        cleanString = cleanString.replace('\n\n' , '\n')
    return cleanString


def loadRegExPatterns():
    regex_patterns = dict(
        linePattern=re.compile('^.+'),
        wordPattern=re.compile('\w+'),
        numCommaPattern=re.compile('[0-9,]+'),
        csvPattern=re.compile('[A-Z0-9 .#&]*,'),
        commaToEOLpattern=re.compile(',[A-Z0-9 .#&]+$'),
        LICpattern=re.compile('^LIC '),
        issuedPattern=re.compile('ISSUED '),
        reg_dtPattern=re.compile('REG DT '),
        datePattern=re.compile('[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}'),
        dateYearFirstPattern=re.compile(r'\d{4,4}/\d{2,2}/\d{2,2}')
    )
    return regex_patterns


def openBrowser(url):
    driver = webdriver.Ie()
    #driver.maximize_window()
    #pyseldriver.get(url)
    #return pyseldriver
    driver.get(url)
    return driver


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
                #print "parseString: found end", targetStart #debug statement
                return inputString[indexEnd:targetEnd:]
    return None


def timeout(msg="Took too much time!"):
    print msg


def waitForUser(msg="enter login credentials"):
    #Wait for user input
    root = Tk()
    tkMessageBox.askokcancel(message=msg)
    root.destroy()


if __name__ == '__main__':
    pass

