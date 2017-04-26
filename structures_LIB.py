# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        ToAccessDBOneEach --> ToAccess3min.py
#              do one loop every 3 min to simulate human interaction
# Purpose:     Read LP from a DB, gather TxDot info, if any, and combine with
#              user input to form a complete record, write record to the DB.
#              Commit a record before gathering more info.
#
# Author:      mthornton
#
# Created:     2016 AUG 12
# Update:      2017 APR 19
# Copyright:   (c) mthornton 2016, 2017
# educational snippits thanks to Tim Greening-Jackson
# (timATgreening-jackson.com)
#-------------------------------------------------------------------------------

import datetime
import pyodbc
from selenium.webdriver.common.by import By
import string
import time
import tkFileDialog
from Tkinter import Tk
from TxDot_LIB import  csvStringFromList, findResponseType, parseRecord, query, repairLineBreaks
from UTIL_LIB import openBrowser, waitForUser
from VPS_LIB import getTextResults, fillFormAndSubmit, findAndClickButton, findAndSelectFrame,\
                    findElementOnPage, findTargetPage, newPageElementFound


def makeSqlString(dictStruct):
    sql = []
    sval = []
    sql.append("INSERT INTO Sheet1 (Plate, Plate_St, [Combined Name], Address, City, State")
    sval.append(" VALUES ( '{plate}', '{plate_st}', '{combined_name}', '{address}', '{city}', '{state}'")
    if dictStruct["zip"]!= 0:
        sql.append(", ZipCode")
        sval.append(", {zip}")
    if dictStruct["title_date"]!= '':
        sql.append(", [Title Date]")
        sval.append(", '{title_date}'")
    if dictStruct["start_date"]!='':
        sql.append(", [Start Date]")
        sval.append(", '{start_date}'")
    if dictStruct["end_date"]!='':
        sql.append(", [End Date]")
        sval.append(", '{end_date}'")
    sql.append(", [Vehicle Make], [Vehicle Model], [Vehicle Body]")
    sval.append(", '{make}', '{model}', '{body}'")
    if dictStruct["vehicle_year"]!=0:
        sql.append(", [Vehicle Year]")
        sval.append(", {vehicle_year}")
    if dictStruct["images_reviewed"]!=0: # #
        sql.append(", [Total Image Reviewed]") #
        sval.append(", {images_reviewed}")
    if dictStruct["images_corrected"]!=0: # #
        sql.append(", [Total Image corrected]")
        sval.append(", {images_corrected}")
    sql.append(", Reason")
    sval.append(", '{reason}'")
    sql.append(", [Time_Stamp], [Agent Initial]")
    sval.append(", '{time_stamp}', '{agent}'")
#    sql.append(", [Sent to Collections Agency],  Multiple, Unassign")
#    sval.append(", '{collections}', '{multiple}', '{unassign}'")
    sql.append(", [Completed: Yes / No Record]")
    sval.append(", '{completed}'")
    sql.append(", [E-Tags (Temporary Plates)], [Dealer Plates]")
    sval.append(", {temp_plate}, {dealer_plate}")
    sql.append(", Comment")
    sval.append(", '{comment}'")
    sql.append(" )")
    sval.append(" )")
    SQL = "".join(sql)
    SVAL = "".join(sval)
    return SQL + SVAL


def recordInit():
    return {
        "plate":'', "plate_st":'',
        "combined_name":'',
        "address":'', "city":'', "state":'', "zip":0,
        "title_date":'', "start_date":'', "end_date":'',
        "make":'' , "model":'' , "body":'' , "vehicle_year":0 ,
        "images_reviewed":0, "images_corrected":0, "reason":'',
        "time_stamp":'', "agent":'',
        "collections":0, "multiple":0, "unassign":0,
        "completed":'', "temp_plate":0, "dealer_plate":0,
        "comment":''
        }


def txDotDataInit():
    return {
        "type":'',
        "plate":'', "plate_st":'',
        "combined_name":'',
        "address":'', "city":'', "state":'', "zip":'',
        "ownedStartDate":'', "title_date":'', "start_date":'', "end_date":'', "reg_date":'' ,
        "make":'' , "model":'', "body":'', "vehicle_year":'', "vin":''
        }


def txDotDataFill(recordDictionary, csvRecord):
    #       0          1     2     3    4   5      6     7         8             9         10      11
    # responseType, plate, name, addr, '', city, state, zip, ownedStartDate, startDate, endDate, issued
        recordDictionary["type"]= csvRecord[0]
        recordDictionary["plate"]= csvRecord[1]
        recordDictionary["plate_st"]= 'TX'
        recordDictionary["combined_name"] = csvRecord[2]
        recordDictionary["address"]= csvRecord[3]
        recordDictionary["addr2"]= csvRecord[4]
        recordDictionary["city"]= csvRecord[5]
        recordDictionary["state"]= csvRecord[6]
        recordDictionary["zip"]= csvRecord[7]
        recordDictionary['ownedStartDate']= csvRecord[8]
        recordDictionary["start_date"]= csvRecord[9]
        recordDictionary["end_date"]= csvRecord[10]
        recordDictionary["title_date"]=csvRecord[11]
        recordDictionary["vehicle_year"]= csvRecord[12]
        recordDictionary["make"]= csvRecord[13]
        recordDictionary["model"]= csvRecord[14]
        recordDictionary["body"]= csvRecord[15]
        recordDictionary["vin"]= csvRecord[16]
        return recordDictionary
        '''
        Violator already exists in VPS and it matches with TXDOT
        Violator exists in TXDOT
        Missing address in TXDOT
        '''

def ToDbRecord(txDotRec, db):
    if txDotRec["type"]=='TEMPORARY': db["temp_plate"]= 1
    if txDotRec["type"]=='PERMIT': db["temp_plate"]= 1
    if txDotRec["type"]=='DEALER': db["dealer_plate"]= 1
    if txDotRec["type"]=='NORECORD': db["completed"]='No Record in TXDOT'
    elif txDotRec["address"]=='': db["completed"]='Missing address in TXDOT'
    else: db["completed"]='Violator exists in TXDOT'

    db["plate"] = txDotRec["plate"]
    db["plate_st"] = txDotRec["plate_st"]
    db["combined_name"] = txDotRec["combined_name"]
    db["address"] = txDotRec["address"]
    db["city"] = txDotRec["city"]
    db["state"]= txDotRec["state"]
    if txDotRec["zip"]!='': db["zip"] = int(txDotRec["zip"])
    db["title_date"] = txDotRec["title_date"]
    if txDotRec["ownedStartDate"] != '':
        db["start_date"] = txDotRec["ownedStartDate"]
    elif txDotRec["title_date"] != '':
        db["start_date"] = txDotRec["title_date"]
    elif txDotRec["reg_date"] != '':
        db["start_date"] = txDotRec["reg_date"] # TODO  what about only REG DT
    else: db["start_date"] = txDotRec["start_date"]
    if txDotRec["end_date"]!='': db["end_date"] = txDotRec["end_date"]
    db["make"] = txDotRec["make"]
    db["model"] = txDotRec["model"]
    db["body"] = txDotRec["body"]
    if txDotRec["vehicle_year"] !='': db["vehicle_year"] = txDotRec["vehicle_year"]
    db["images_reviewed"] = 10
    #db["images_corrected"] =  TODO
    #db["reason"] =   TODO
    db["time_stamp"] = time.strftime("%m/%d/%Y %I:%M:%S %p") # example: '9/13/2016 4:53:47 PM'
    db["agent"] = "mthornton"
    #db["VIN"] = txDotRec["VIN"]  # TODO
    db["comment"] = "test"

    '''
    Plate is correct
    Plate is incorrect
    Unclear image
    Multiple vehicles with the same plate
    NO images
    Out of State
    U.S. Government Plate
    First Responder
    Other
    '''
    return db

print("No unit tests.")

# 'd' Signed integer decimal.
# 'i' Signed integer decimal.
# 'o' Signed octal value.
# 'u' Obsolete type – it is identical to 'd'.
# 'x' Signed hexadecimal (lowercase).
# 'X' Signed hexadecimal (uppercase).
# 'e' Floating point exponential format (lowercase).
# 'E' Floating point exponential format (uppercase).
# 'f' Floating point decimal format.
# 'F' Floating point decimal format.
# 'g' Floating point format. Uses lowercase exponential format or decimal format
# 'G' Floating point format. Uses uppercase exponential format or decimal format
# 'c' Single character (accepts integer or single character string).
# 'r' String (converts any Python object using repr()).
# 's' String (converts any Python object using str()).
# '%' No argument is converted, results in a '%' character in the result.

