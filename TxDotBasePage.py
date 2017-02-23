# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        TxDotBasePage.py
#
# Purpose:     contain all methods for talking to selenium
#
# Author:      mthornton
#
# Created:     2017 FEB 20
# Update:      2017 FEB 22
# Copyright:   (c) mthornton 2017
#-------------------------------------------------------------------------------

import datetime
import pyodbc
import string
import tkFileDialog
from Tkinter import *
from TxDot_LIB import *
from VPS_LIB import waitForUser


def setParameters():
    parameters = {
    'delay' : 15,
    'url' : 'https://lprod.scip.ntta.org/scip/jsp/SignIn.jsp', # initial URL
    #'url' : 'http://intranet/SitePages', # initial URL
    'operatorMessage' : "",
    'inputLocator' : (By.XPATH, '//input[@id = "P_LIC_PLATE_NBR"]'),
    'staleLocator' : (By.XPATH,'//h1[contains(text(),"Violation Search")]'),
    'staleLocator2' : (By.XPATH,'//h1[contains(text(),"Violation Search Result")]'),
    'buttonLocator' : (By.XPATH,'//input[@value="Query"]'),
    'frameParamters' : {'useFrames' : True, 'frameLocator' : (By.XPATH, '//frame[@name="fraRxL"]') },
    'resultPageTextLocator' : (By.XPATH, '//TD/H1'),
    'resultPageVerifyText' : 'Violation Search Results',
    'outputLocator' : (By.XPATH,'//BODY/P[contains(text(),"Record")]'),
    'resultIndexParameters' : {'regex' : "Records \d+ to \d+ of (\d+)", 'selector' : 'tail'},  # head, tail, or all
    'dataInFileName' : '',
    'dataOutFileName' : '',
    'returnOrClick' : 'return', # use Return or Click to submit form
    }
    return parameters


def printDbColumnNames():
    rowcount = 0
    while True:
        row = dbcursor.fetchone()
        if row is None:
            break
        rowcount += 1
        print "Plate {}".format(row[0])
        #print "entire row -->", row
    print rowcount

    for column in dbcursor.columns(table='US State'):
        print column.column_name
    dbcursor.execute('''SELECT Field1
                        FROM [US State]''')
    while True:
        row = dbcursor.fetchone()
        if row is None:
            break
        print "entire row -->{}".format(row[0])


def recordInit():
    recordDictionary = {
        "plate":'', "plate_st":'',
        "combined_name":'',
        "address":'', "city":'', "state":'', "zip":0,
        "title_date":'', "start_date":'', "end_date":'',
        "make":'' , "model":'' , "body":'' , "vehicle_year":0 ,
        "images_reviewed":0, "images_corrected":0, "reason":'',
        "time_stamp":'', "agent":'',
        "title_month":'', "title_day":'', "title_year":'',
        "collections":0, "multiple":0, "unassign":0,
        "completed":'', "temp_plate":0, "dealer_plate":0
        }
    return recordDictionary


def txDotDataInit():
    recordDictionary = {
        "type":'',
        "plate":'', "plate_st":'',
        "combined_name":'',
        "address":'', "city":'', "state":'', "zip":'',
        "ownedStartDate":'', "title_date":'', "start_date":'', "end_date":'' ,
        "make":'' , "model":'', "body":'', "vehicle_year":''
        }
    return recordDictionary


def txDotDataFill(recordDictionary, csvRecord):
    #       0          1     2     3    4   5      6     7         8             9         10      11
    # responseType, plate, name, addr, '', city, state, zip, ownedStartDate, startDate, endDate, issued
        recordDictionary["type"]= csvRecord[0]
        recordDictionary["plate"]= csvRecord[1]
        recordDictionary["plate_st"]= 'TX'
        recordDictionary["combined_name"] = csvRecord[2]
        recordDictionary["address"]= csvRecord[3]
        recordDictionary["city"]= csvRecord[5]
        recordDictionary["state"]= csvRecord[6]
        recordDictionary["zip"]= csvRecord[7]
        recordDictionary['ownedStartDate']= csvRecord[8]
        recordDictionary["start_date"]= csvRecord[9]
        recordDictionary["end_date"]= csvRecord[10]
        #recordDictionary["title_date"]=
        #recordDictionary["make"]= csvRecord[x1]
        #recordDictionary["model"]= csvRecord[x1]
        #recordDictionary["body"]= csvRecord[x1]
        recordDictionary["vehicle_year"]= 0
        #recordDictionary["images_reviewed"]= csvRecord[x1]
        #recordDictionary["images_corrected"]= csvRecord[x1]
        #recordDictionary["reason"]= csvRecord[x1]
        #recordDictionary["time_stamp"]= csvRecord[x1]
        #recordDictionary["agent"]= csvRecord[x1]
        #recordDictionary["title_month"]= csvRecord[x1]
        #recordDictionary["title_day"]= csvRecord[x1]
        #recordDictionary["title_year"]= csvRecord[x1]
        #recordDictionary["collections"]= 0
        #recordDictionary["multiple"]=
        #recordDictionary["unassign"]=
        #recordDictionary["completed"]=
        #recordDictionary["temp_plate"]= csvRecord[x1]
        #recordDictionary["dealer_plate"]= csvRecord[x1]
        return recordDictionary


def txDotToDbRecord(txDotRec, db):
    if txDotRec["type"]=='NORECORD': db["completed"]='NO RECORD'
    else: db["completed"]='YES'
    db["plate"] = txDotRec["plate"]
    db["plate_st"] = txDotRec["plate_st"]
    db["combined_name"] = txDotRec["combined_name"]
    db["address"] = txDotRec["address"]
    db["city"] = txDotRec["city"]
    db["state"]= txDotRec["state"]
    if txDotRec["zip"]!='': db["zip"] = int(txDotRec["zip"])
    #db["title_date"] = txDotRec["title_date"]
    db["title_date"] = ''
    if txDotRec["start_date"]!='': db["start_date"] = txDotRec["start_date"]
    if txDotRec["end_date"]!='': db["end_date"] = txDotRec["end_date"]
    #db["make"] = txDotRec["make"]
    #db["model"] = txDotRec["model"]
    #db["body"] = txDotRec["body"]
    #db["vehicle_year"] = txDotRec["vehicle_year"]
    #db["images_reviewed"] = txDotRec["images_reviewed"]
    #db["images_corrected"] = txDotRec["images_corrected"]
    #db["reason"] = txDotRec["reason"]
    db["time_stamp"] = time.strftime("%m/%d/%Y %I:%M:%S %p") # month, day, long year, 12 hr, AM/PM
    #db["time_stamp"] = '9/13/2016 4:53:47 PM'
    db["agent"] = "mthornton"
    #db["title_month"] = txDotRec["title_month"]
    #db["title_day"] = txDotRec["title_day"]
    #db["title_year"] = txDotRec["title_year"]
    #db["collections"] = txDotRec["collections"]
    #db["multiple"] = txDotRec["multiple"]
    #db["unassign"] = txDotRec["unassign"]
    #db["completed"] = txDotRec["completed"]
    if txDotRec["type"]=='TEMPORARY': db["temp_plate"]= 1
    if txDotRec["type"]=='DEALER': db["dealer_plate"]= 1

    return db

class TxDotObject(object):
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



if __name__ == '__main__':

    NUMBERtoProcess = 10
    delay=10
    SLEEPTIME = 5
    parameters = setParameters()
    parameters['operatorMessage'] = "Use debug mode, \n open VPS, new violator search window, \n open DMV window, \n run to completion"
    print parameters['operatorMessage']
    txDriver = openBrowser('https://mvinet.txdmv.gov')
    driver = openBrowser(parameters['url'])

    try:
            results = query(txDriver, delay, plateString)
            if results is not None:
                #print results # for debug
                fileString = repairLineBreaks(results)
                #remove non-ascii
                ##fileString = "".join(filter(lambda x:x in string.printable, fileString))
            foundCurrentPlate = False
            recordList = []
            while True:
                try:
                    responseType, startNum, endNum = findResponseType(plateString, fileString)
                except:
                    responseType = None
                    if foundCurrentPlate == False:
                        print plateString, ' Plate/Pattern not found. Unable to resolve record type.'
                        time.sleep(3)
                    break
                if responseType != None: # there must be a valid text record to process
                    foundCurrentPlate = True
                    #print 'main:', responseType, startNum, endNum # for debug
                    typeString = fileString[startNum:endNum + 1]
                    #print typeString # for debug
                    fileString = fileString[:startNum] + fileString[endNum + 1:] # what is this for ?
                    listData = parseRecord(responseType, typeString)
                    # make txdot data record here
                    recordList.append(listData)
                    #print listData # for debug
                    assert(len(listData)==12)



# from TxDot lib --> ['response type', 'plate', 'name', 'addr', 'addr2', 'city', 'state', 'zip', 'ownedStartDate', 'startDate', 'endDate', 'issued']
#"""  ALMOST FULL WRITE TO DATABASE missing title day, month, year -->  this will never happen. some fields are exclusive of others. """

    finally:
        print("Closing TxDot pages")
        txDriver.close()
        txDriver.quit()


