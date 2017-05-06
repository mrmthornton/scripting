# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        UTIL_LIB.py
# Purpose:     A library for common behaviors.
#              extracted from VPS_LIB
# Author:      mthornton
#
# Created:     2015 AUG 01
# Updates:     2017 APR 13
# Copyright:   (c) michael thornton 2015, 2016, 2017
#-------------------------------------------------------------------------------


import re
from selenium import webdriver
from Tkinter import Tk # python 2
#from tkinter import Tk, messagebox
import tkMessageBox # python 2


def cleanUpString(messyString):
    cleanString = messyString.replace(' ' , '') # remove any spaces
    cleanString = cleanString.replace('"' , '') # remove any double quotes
    cleanString = cleanString.replace('\t' , '') # remove any tabs
    cleanString = cleanString.replace(',' , '\n') # replace comma with \n
    for _ in range(10):            # replace multiple newlines with a single \n
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


from functools import partial
def nextIndex(aString):
    def func(s,n):
        while True:
            yield s[n+1:]
            n+=n
    return partial(func, aString)


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
                #targetStart = found.start()
                targetEnd = found.end()
                #print "parseString: found end", targetStart #debug statement
                return inputString[indexEnd:targetEnd:]
    return None


def permutationPattern(lp):
    """
    return a compiled regex which matches on either 'o' or 0, or 'i' or 1,
    for each position where any of these four characters are found.
    """
    lp = lp.upper()
    l = ['(']
    for nextChar in lp:
        if nextChar=='0' or nextChar=='O':
            nextChar = "[0O]"
        if nextChar=='1' or nextChar=='I':
            nextChar = "[1I]"
        l.append(nextChar)
    #print("UTIL_LIB:permutatinPattern:list: ", l) # for debug
    l.append(')')
    i = iter(l)
    regexString = "".join(i)
    print("UTIL_LIB:permutatinPattern:regexString: ", regexString) # for debug
    return re.compile(regexString)


def testPermutaionPattern():
    licencePlate = "loseit"
    io10Pattern = permutationPattern(licencePlate)
    found = io10Pattern.search("LOSEIT")
    if found:
        print(found.start(),found.end())
        print(found.group())
    found = io10Pattern.search("L0SEIT")
    if found:
        print(found.start(),found.end())
    found = io10Pattern.search("LOSE1T")
    if found:
        print(found.start(),found.end())
    found = io10Pattern.search("L0SE1T")
    if found:
        print(found.start(),found.end())

    licencePlate = "nooodle"
    io10Pattern = permutationPattern(licencePlate)
    found = io10Pattern.search("N0O0DLE")
    if found:
        print(found.start(),found.end())
    found = io10Pattern.search("I am a NOO0DLE")
    if found:
        print(found.start(),found.end())


def returnLargest(a,b):
    int
    if int(a)>int(b): return a
    return b

def testReturnLargest():
    assert(returnLargest(0,1)==1)
    assert(returnLargest('0','1')=='1')


def returnSmallest(a,b):
    int
    if int(a)<int(b): return a
    return b

def testReturnSmallest():
    assert(returnSmallest(0,1)==0)
    assert(returnSmallest('0','1')=='0')


def timeout(msg="Took too much time!"):
    print(msg)


def waitForUser(msg="enter login credentials"):
    #Wait for user input
    root = Tk()
    tkMessageBox.askokcancel(message=msg) # python 2
    #messagebox.askokcancel(message=msg) # python 3
    root.destroy()


if __name__ == '__main__':
    testPermutaionPattern()
    testReturnSmallest()
    testReturnLargest()

    x = nextIndex("helloWorld")
    print(x(2).next())
    print(x(4).next())


