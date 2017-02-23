# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        TxDotTestQuery.py
#
# Purpose:
#
# Author:      mthornton
#
# Created:     2017 FEB 22
# Update:
# Copyright:   (c) mthornton 2017
#-------------------------------------------------------------------------------

import datetime
import pyodbc
import string
import tkFileDialog
from Tkinter import *
import TxDot_LIB
from VPS_LIB import waitForUser
from VPS_LIB import openBrowser


class TxDotTestQuery(object):
    def __init__(self, licencePlate=None):
        self._licencePlate = licencePlate
        if licencePlate is None:
            self._licencePlate = 'CCY0042'
            print "using default" + self._licencePlate

    @property
    def licencePlate(self):
        """The licence plate string"""
        return self._licencePlate

    @licencePlate.setter
    def licencePlate(self, value):
        self._licencePlate = value

    @licencePlate.deleter
    def licencePlate(self):
        del self._licencePlate

    def query(self, driver):
        result = TxDot_LIB.query(driver, 10, self._licencePlate)


if __name__ == '__main__':
    delay=10
    #parameters = setParameters()
    parameters = {}
    parameters['operatorMessage'] = "Use debug mode, \n open VPS, new violator search window, \n open DMV window, \n run to completion"
    print parameters['operatorMessage']

    driver = openBrowser('https://mvinet.txdmv.gov')
    waitForUser()
    singleQuery = TxDotTestQuery()
    text = singleQuery.query(driver)
    print text



# from TxDot lib --> ['response type', 'plate', 'name', 'addr', 'addr2', 'city', 'state', 'zip', 'ownedStartDate', 'startDate', 'endDate', 'issued']
#"""  ALMOST FULL WRITE TO DATABASE missing title day, month, year -->  this will never happen. some fields are exclusive of others. """



'''
class TxDotTestQuery(object):
    def __init__(self, url=None):
        self._url = url
        if url is None:
            self._url = 'https://mvinet.txdmv.gov'
        driver = openBrowser(url)

    @property
    def url(self):
        """URL for TX DMV RTS database"""
        return self._url

    @x.setter
    def x(self, value):
        self._url = value

    @x.deleter
    def x(self):
        del self._url

'''