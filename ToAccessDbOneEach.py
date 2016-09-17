# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        ToAccessDBOneEach
# Purpose:     Read LP from DB, gather TxDot info, if any, and combine with
#              user input to form a complete record, write record to DB.
#              Process and complete a db record before gathering more info.
#
# Author:      mthornton
#
# Created:     2016 AUG 12
# Update:
# Copyright:   (c) mthornton 2016
# educational snippits thanks to Tim Greening-Jackson, (timATgreening-jackson.com)
#-------------------------------------------------------------------------------

import datetime
import pyodbc
#import re
import string
import tkFileDialog
from Tkinter import *
from TxDot_LIB import *


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


def ConnectToAccessFile():
        #Prompt the user for db, create connection and cursor.
        root = Tk()
        dbname = tkFileDialog.askopenfilename(parent=root, title="Select database",
                    filetypes=[('locked', '*.accde'), ('normal', '*.accdb')])
        root.destroy()
        # Connect to the Access database
        connectedDB = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+dbname+";")
        dbcursor=connectedDB.cursor()
        print("ConnectToAccessFile: Connected to {}".format(dbname))
        return connectedDB, dbcursor


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
        #recordDictionary["vehicle_year"]= csvRecord[x1]
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
    db["title_date"] = '1/1/1900'
    if txDotRec["start_date"]!='': db["start_date"] = txDotRec["start_date"]
    else: db["start_date"] = '01/01/1900'
    if txDotRec["end_date"]!='': db["end_date"] = txDotRec["end_date"]
    else: db["end_date"] = '01/01/1900'
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


if __name__ == '__main__':

    NUMBERtoProcess = 2
    delay=10
    url = 'https://mvinet.txdmv.gov'
    driver = openBrowser(url)

    incre = re.compile("INC\d{12}[A-Z]?") # Regex that matches incident references

    try:
        dbConnect, dbcursor = ConnectToAccessFile()
        #for row in dbcursor.columns(table='Sheet1'): # debug
        #    print row.column_name                    # debug
        #dbcursor.execute("SELECT * FROM Sheet1")
        dbcursor.execute("SELECT plate FROM [list of plate 4 without matching sheet1]") # (1),4,8,9,10, '11'  ,12
        #dbcursor.execute("SELECT plate FROM [list of plates 2 without matching sheet1]") # 2,3,5,6,7
        lpList = []
        loopCount = 0
        while loopCount< NUMBERtoProcess:
            lpRecord = dbcursor.fetchone()
            if lpRecord is None:
                print "main() : Finished, no more input records."
                break
            lpList.append(lpRecord)
            loopCount += 1

        for row in lpList:
            if row is None:
                print "main() : Finished, no more LP's ."
                break
            plate = str(row[0])
            results = query(driver, delay, plate)
            if results is not None:
                #print results # for debug
                fileString = repairLineBreaks(results)
                #remove non-ascii
                ##fileString = "".join(filter(lambda x:x in string.printable, fileString))
            foundCurrentPlate = False
            recordList = []
            while True:
                try:
                    responseType, startNum, endNum = findResponseType(plate, fileString)
                except:
                    responseType = None
                    if foundCurrentPlate == False:
                        print plate, ' Plate/Pattern not found. Unable to resolve record type.'
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
                    print listData
                    assert(len(listData)==12)

            for csvRecord in recordList:
                txDotRecord = txDotDataFill(txDotDataInit(), csvRecord)
                dbRecord = recordInit()
                dbRecord = txDotToDbRecord(txDotRecord, dbRecord)
                print dbRecord # for debug
                sql = "INSERT INTO Sheet1 (Plate, Plate_St, [Combined Name], Address, City, State, ZipCode, \
                                          [Title Date], [Start Date], [End Date], \
                                          [Vehicle Make], [Vehicle Model], [Vehicle Body], [Vehicle Year], \
                                          [Time Stamp], [Agent Initial], \
                                          [Sent to Collections Agency],  Multiple, Unassign, [Completed: Yes / No Record], \
                                          [E-Tags (Temporary Plates)], [Dealer Plates] ) \
                            VALUES (    '{plate}', '{plate_st}', '{combined_name}', '{address}', '{city}', '{state}', '{zip}', \
                                        '{title_date}', '{start_date}', '{end_date}', \
                                        '{make}', '{model}', '{body}', {vehicle_year},\
                                        '{time_stamp}', '{agent}', \
                                        {collections}, {multiple}, {unassign}, '{completed}', \
                                        {temp_plate}, {dealer_plate} ) "\
                                .format(**dbRecord)
                                #[Title Date], [Start Date], [End Date], \
                                #'{title_date}', '{start_date}', '{end_date}', \
                dbcursor.execute(sql)
            print("Comitting changes")
            dbcursor.commit()
# from TxDot lib --> ['response type', 'plate', 'name', 'addr', 'addr2', 'city', 'state', 'zip', 'ownedStartDate', 'startDate', 'endDate', 'issued']

#                                                               Plate, Plate_St, [Combined Name], Address, City, State, ZipCode,
#                                                               [Title Date], [Start Date], [End Date],
#                                                               [Vehicle Make], [Vehicle Model], [Vehicle Body], [Vehicle Year],
# [Total Image Reviewed], [Total Image corrected], Reason,      [Time Stamp], [Agent Initial] \
# Title_Month, Title_Day, Title_Year,
#                                                               [Sent to Collections Agency],  Multiple, Unassign, [Completed: Yes / No Record],
#                                                               [E-Tags (Temporary Plates)], [Dealer Plates]

#                           "plate":'', "plate_st":'', "combined_name":'', "address":'', "city":'', "state":'', "zip":0,
#  "title_date":'', "start_date":'', "end_date":'' ,
#                           "make":'' , "model":'' , "body":'' , "vehicle_year":0 ,
#                           "images_reviewed":0, "images_corrected":0, "reason":'',
#                           "time_stamp":'', "agent":'',
#  "title_month":'', "title_day":'', "title_year":'',
#                           "collections":0, "multiple":0, "unassign":0, "completed":'',
#                           "temp_plate":0, "dealer_plate":0

    finally:
        print("Closing databases")
        dbConnect.close()
        driver.close() # close browser window
        driver.quit()  # close command window

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

        #dbcursor.execute("DELETE * FROM {}".format(table))
        #rows = dbcursor.fetchall()
        #dbfacilities = {unicode(row[1]):row[0] for row in rows}
        #s7incidents = {unicode(row[0]):S7Incident(*row) for row in rows if incre.match(row[0])}
        #cursor.execute("SELECT DISTINCT RAISED FROM INCIDENTS")
        #s7productions = [r[0] for r in rows]
        #s7ad1s = [S7AD1(*row) for row in rows]
        # do the SELECT @@IDENTITY to give us the autonumber index.
        # To make sure everything is case-insensitive convert the hash keys to UPPERCASE.

        #for p in sorted(s7productions):
        #    dbcursor.execute("INSERT INTO PRODUCTIONS (PRODUCTION) VALUES ('{}')".format(p))
        #    dbcursor.execute("SELECT @@IDENTITY")
        #    dbproductions[p.upper()] = dbcursor.fetchone()[0]
        #[s7incidents[k].ProcessIncident(dbcursor, dbfacilities, dbproductions) for k in sorted(s7incidents)]

        # Match the new parent incident IDs in the AD1s and then write to the new table. Some
        # really old AD1s don't have the parent incident reference in the REF field, it is just
        # mentioned SOMEWHERE in the commentary. So if the REF field doesn't match then do a
        # re.search (not re.match!) for it. It isn't essential to match these older AD1s with
        # their parent incident, but it is quite useful (and tidy).

        #print("Matching and writing AD1s".format(len(s7ad1s)))
        #for a in s7ad1s:
        #    if a.ref in s7incidents:
        #        a.SetPID(s7incidents[a.ref].dbid)
        #        a.SetProduction(s7incidents[a.ref].production)
        #    else:
        #        z=incre.search(a.commentary)
        #        if z and z.group() in s7incidents:
        #            a.SetPID(s7incidents[z.group()].dbid)
        #            a.SetProduction(s7incidents[z.group()].production)
        #    a.Process(dbcursor)


'''

params = [filter(lambda x: x in string.printable, item.text)
          for item in row.find_all('td')]
'''

#Iterating over strings is unfortunately rather slow in Python.
#Regular expressions are over an order of magnitude faster.
'''
control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    return control_char_re.sub('', s)
'''

class S7Incident:
    """
    Class containing the records downloaded from the S7.INCIDENTS table
    """
    def __init__(self, id_incident, priority, begin, acknowledge, diagnose,
     workaround,fix, handoff, lro, nlro, facility, ctas, summary, raised, code):
        self.id_incident=unicode(id_incident)
        # a dictionary preceeding a list-comprehension
        self.priority = {u'P1':1, u'P2':2, u'P3':3, u'P4':4, u'P5':5} [unicode(priority.upper())]
        self.fix = fix
        self.handoff = True if handoff else False
        self.nlro = True if nlro else False
        self.facility = unicode(facility)
        self.summary = "** NONE ***" if type(summary) is NoneType else summary.replace("'","")
        self.raised = raised.replace("'","")
        self.code = 0 if code is None else code
        self.dbid = None

    def __repr__(self):
        return "[{}] ID:{} P{} Prod:{} Begin:{} A:{} D:+{}s W:+{}s F:+{}s\nH/O:{} LRO:{} NLRO:{} Facility={} CTAS={}\nSummary:'{}',Raised:'{}',Code:{}"\
            .format( self.id_incident,self.dbid, self.priority, self.production, self.begin,
                    self.acknowledge, self.diagnose, self.workaround, self.fix,
                    self.handoff, self.lro, self.nlro, self.facility, self.ctas,
                    self.summary, self.raised, self.code)

    def ProcessIncident(self, cursor, facilities, productions):
        sql="""INSERT INTO INCIDENTS
        (ID_INCIDENT, PRIORITY, FACILITY, BEGIN, ACKNOWLEDGE, DIAGNOSE, WORKAROUND, FIX, HANDOFF, SUMMARY, RAISED, CODE, PRODUCTION)
        VALUES ('{}', {}, {}, #{}#, {}, {}, {}, {}, {}, '{}', '{}', {}, {})
        """.format(self.id_incident, self.priority, facilities[self.facility], self.begin,
           self.acknowledge, self.diagnose, self.workaround, self.fix,
           self.handoff, self.summary, self.raised, self.code, self.production)
        cursor.execute(sql)
        cursor.execute("SELECT @@IDENTITY")
        self.dbid = cursor.fetchone()[0]

class S7AD1:
    """
    S7.AD1 records.
    """
    def __init__(self, id_ad1, date, ref, commentary, adjustment):
        self.date = date
        self.ref = unicode(ref)
        self.commentary = unicode(commentary)
        self.adjustment = float(adjustment)

    def __repr__(self):
        return "[{}] Date:{} Parent:{} PID:{} Amount:{} Commentary: {} "\
           .format(self.id_ad1, self.date.strftime("%d/%m/%y"), self.ref, self.pid, self.adjustment, self.commentary)

class S7Financial:
    """
    S7 monthly financial summary of income and penalties from S7.FINANCIALS table.
    These are identical in the new database
    """
    def __init__(self, month, year, gco, cta, support, sc1, sc2, sc3, ad1):
        self.begin = datetime.date(year, month, 1)
        self.gco = float(gco)
        self.cta = float(cta)
        self.support = float(support)
        self.sc1 = float(sc1)
        self.sc2 = float(sc2)
        self.sc3 = float(sc3)
        self.ad1 = float(ad1)

    def __repr__(self):
        return "Period: {} GCO:{:.2f} CTA:{:.2f} SUP:{:.2f} SC1:{:.2f} SC2:{:.2f} SC3:{:.2f} AD1:{:.2f}"\
           .format(self.start.strftime("%m/%y"), self.gco, self.cta, self.support, self.sc1, self.sc2, self.sc3, self.ad1)

    def Process(self, cursor):
        """
        Insert in to FINANCIALS table
        """
        sql = "INSERT INTO FINANCIALS (BEGIN, GCO, CTA, SUPPORT, SC1, SC2, SC3, AD1) VALUES (#{}#, {}, {}, {}, {}, {}, {},{})"\
              .format(self.begin, self.gco, self.cta, self.support, self.sc1, self.sc2, self.sc3, self.ad1)
        cursor.execute(sql)

class S7SC3:

    def __repr__(self):
        return "{} P1:{} P2:{} CHG:{} SUC:{} INC:{} FLD:{} EGY:{}"\
           .format(self.period.strftime("%m/%y"), self.p1ot, self.p1ot, self.changes, self.successful, self.incidents, self.failed, self.emergency)


    def Process(self, cursor):
        """
        Inserts a record in to the Access database
        (PLATE, PLATE_ST, COMBINED NAME, ADDRESS, CITY, ZIPCODE, STATE,
         TITLE DATE, START DATE, END DATE, VEHICLE MAKE, VEHICLE MODEL, VEHICLE BODY)
        """
        sql = "INSERT INTO SC3 (BEGIN, P1OT, P2OT, CHANGES, SUCCESSFUL, INCIDENTS, FAILED, EMERGENCY) VALUES\
            (#{}#, {}, {}, {}, {}, {}, {}, {})"\
              .format(self.begin, self.p1ot, self.p2ot, self.changes, self.successful, self.incidents, self.failed, self.emergency)
        cursor.execute(sql)
