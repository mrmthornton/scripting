# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        ToAccessDB
# Purpose:     Read LP from DB, gather TxDot info, if any, and combine with
#              user input to form a complete record, write record to DB.
#
# Author:      mthornton
#
# Created:     2016 AUG 1
# Update:      2016 SEP 9
# Copyright:   (c) mthornton 2016
# educational snippits thanks to Tim Greening-Jackson, (timATgreening-jackson.com)
#-------------------------------------------------------------------------------

import datetime
import pyodbc
import re
import string
import tkFileDialog
from Tkinter import *


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
        "address":'', "city":'', "state":'', "zip":'',
        "title_date":'', "start_date":'', "end_date":'' ,
        "make":'' , "model":'' , "body":'' , "vehicle_year":'' ,
        "images_reviewed":'', "images_corrected":'', "reason":'',
        "time_stamp":'', "agent":'',
        "title_month":'', "title_day":'', "title_year":'',
        "collections":'', "multiple":'', "unassign":'',
        "completed":'', "temp_plate":'', "dealer_plate":''
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
        #recordDictionary["title_date"]= csvRecord[x1]
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
        #recordDictionary["collections"]= csvRecord[x1]
        #recordDictionary["multiple"]= csvRecord[x1]
        #recordDictionary["unassign"]= csvRecord[x1x]
        #recordDictionary["completed"]= ''
        #recordDictionary["temp_plate"]= csvRecord[x1]
        #recordDictionary["dealer_plate"]= csvRecord[x1]
        return recordDictionary


def txDotToDbRecord(txDotRec, db):

    if txDotRec["type"]=='NORECORD':
        db["completed"]='NO RECORD'
    if txDotRec["type"]=='TEMPORARY':
        db["temp_plate"]= True

    if txDotRec["zip"]!='':
        db["zip"] = int(txDotRec["zip"])
    else:
        db["zip"] = 0

    #if txDotRec["start_date"]!='':
    #    db["start_date"] = int(txDotRec["start_date"])
    #else:
    #    db["start_date"] = 0

    #if txDotRec["end_date"]!='':
    #    db["end_date"] = int(txDotRec["end_date"])
    #else:
    #    db["end_date"] = 0

    return db


from TxDot_LIB import *

if __name__ == '__main__':

    delay=10
    url = 'https://mvinet.txdmv.gov'
    driver = openBrowser(url)

    incre = re.compile("INC\d{12}[A-Z]?") # Regex that matches incident references

    try:
        dbConnect, dbcursor = ConnectToAccessFile()
        #for row in dbcursor.columns(table='Sheet1'): # debug
        #    print row.column_name                    # debug
        #dbcursor.execute("SELECT * FROM Sheet1")
        dbcursor.execute("SELECT plate FROM [list of plate 4 without matching sheet1]") #  ,4,8,9,10, '11'  ,12
        #dbcursor.execute("SELECT plate FROM [list of plates ? without matching sheet1]") # 2,3,5,6,7

        recordList = []
        loopCount = 0       # debug loop
        while loopCount<3:  # debug loop
        #while True:
        #while False:  # skip this loop
            row = dbcursor.fetchone()
            if row is None:
                break
            plate = str(row[0])
            results = query(driver, delay, plate)
            if results is not None:
                #print results # for debug
                fileString = repairLineBreaks(results)
                #remove non-ascii
                ##fileString = "".join(filter(lambda x:x in string.printable, fileString))
            foundCurrentPlate = False
            while True:
                try:
                    responseType, startNum, endNum = findResponseType(plate, fileString)
                except:
                    responseType = None
                    if foundCurrentPlate == False:
                        print "\n", plate, ' Plate/Pattern not found'
                        time.sleep(1)
                    break
                if responseType != None: # there must be a valid text record to process
                    foundCurrentPlate = True
                    #print 'main:', responseType, startNum, endNum # for debug
                    typeString = fileString[startNum:endNum + 1]
                    #print typeString # for debug
                    fileString = fileString[:startNum] + fileString[endNum + 1:] # what is this for ?
                    listData = parseRecord(responseType, typeString)
                    #csvString = csvStringFromList(listData)
                    # make txdot data record here
                    recordList.append(listData)
                    print listData
                    assert(len(listData)==12)
            loopCount += 1 # debug loop

        #recordList =[['DEALER', '05798V', 'Roadrunner Services, LLC', '125 Stable Creek Rd', '', 'Fayetteville', 'GA', '30215', '', '', '', ''],\
        #            ['NORECORD', '057B0392', '', '', '', '', '', '', '', '', '', ''],\
        #            ['NORECORD', '057C086', '', '', '', '', '', '', '', '', '', '']    ]
        for csvRecord in recordList:
            txDotRecord = txDotDataFill(txDotDataInit(), csvRecord)
            dbRecord = recordInit()
            dbRecord = txDotToDbRecord(txDotRecord, dbRecord)

            sql = "INSERT INTO Sheet1 (Plate, Plate_St, [Combined Name], Address, City, State, ZipCode), [Completed: Yes / No Record] \
                        VALUES (     '{plate}', '{plate_st}', '{combined_name}', '{address}', '{city}', '{state}', \
                                    '{zip}', '{completed}')"\
                        .format(**dbRecord)

            dbcursor.execute(sql)

        print("Comitting changes")
        dbcursor.commit()

    finally:
        print("Closing databases")
        dbConnect.close()

            #dbcursor.execute('''SELECT Plate, Plate_St, [Combined Name], Address, City, State, ZipCode, \
            #    [Title Date], [Start Date], [End Date], [Vehicle Make], [Vehicle Model], [Vehicle Body], [Vehicle Year], \
            #    [Total Image Reviewed], [Total Image corrected], Reason, [Time Stamp], [Agent Initial] \
            #    FROM Sheet1''')

            #    Title_Month, Title_Day, Title_Year, [Sent to Collections Agency],
            #    Multiple, Unassign, [Completed: Yes / No Record],
            #   [E-Tags (Temporary Plates)], [Dealer Plates]

            #sql = "INSERT INTO Sheet1 (Plate, Plate_St, [Combined Name], Address, City, State, ZipCode,[Start Date], [End Date]) \
            #            VALUES (     '{plate}', '{plate_st}', '{combined_name}', '{address}', '{city}', '{state}', \
            #                       '{zip:d}', '{start_date:d}', '{end_date:d}')"\
            #            .format(**record)

            #sql = "INSERT INTO Sheet1 (PLATE, [COMBINED NAME]) \
            #    VALUES ('{}', '{}')".format(plate, combined_name )

        """
            { "plate":'', "plate_st":'', "combined_name":'', "address":'', "city":'', "state":'', "zip":'', \
            "title_date":'', "start_date":'', "end_date":'' , "make":'' , "model":'' , "body":'' , "vehicle_year":'' , \
            "images_reviewed":'' , "images_corrected":'', "reason":'', "time_stamp":'', "agent":'', \
            "title_month":'', "title_day":'', "title_year":'', "collections":'', \
            "multiple":'', "unassign":'', "completed":'', \
            "temp_plate":'', "dealer_plate":''                    }

            Inserts a record in to the Access database
            (PLATE, PLATE_ST, [COMBINED NAME], ADDRESS, CITY, ZIPCODE, STATE,
            [TITLE DATE], [START DATE], [END DATE], [VEHICLE MAKE], [VEHICLE MODEL], [VEHICLE BODY])
            """
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

def printDbColumnNames():
    """
        rowcount = 0
        while True:
            row = dbcursor.fetchone()
            if row is None:
                break
            rowcount += 1
            print "Plate {}".format(row[0])
            #print "entire row -->", row
        print rowcount
        """
    """
        for column in dbcursor.columns(table='US State'):
            print column.column_name
        dbcursor.execute('''SELECT Field1
                            FROM [US State]''')
        while True:
            row = dbcursor.fetchone()
            if row is None:
                break
            print "entire row -->{}".format(row[0])
        """


            #dbcursor.execute("DELETE * FROM {}".format(table))
            #rows = dbcursor.fetchall()
            #dbfacilities = {unicode(row[1]):row[0] for row in rows}

        #s7incidents = {unicode(row[0]):S7Incident(*row) for row in rows if incre.match(row[0])}
        #s7cursor.execute("SELECT DISTINCT RAISED FROM INCIDENTS")
        #s7productions = [r[0] for r in rows]
        #s7ad1s = [S7AD1(*row) for row in rows]
        #[p.Process(dbcursor) for p in s7financials]
        #s7sc3s = [S7SC3(*row) for row in rows]
        #print("Writing SC3s ({})".format(len(s7sc3s)))

        # do the SELECT @@IDENTITY to give us the autonumber index.
        # To make sure everything is case-insensitive convert the hash keys to UPPERCASE.

        #for p in sorted(s7productions):
        #    dbcursor.execute("INSERT INTO PRODUCTIONS (PRODUCTION) VALUES ('{}')".format(p))
        #    dbcursor.execute("SELECT @@IDENTITY")
        #    dbproductions[p.upper()] = dbcursor.fetchone()[0]


        ## Now process the incidents etc. that we have retrieved from the S7 database
        #
        #print("Writing incidents ({})".format(len(s7incidents)))
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
        self.priority = {u'P1':1, u'P2':2, u'P3':3, u'P4':4, u'P5':5} [unicode(priority.upper())]
        self.begin = begin
        self.acknowledge = acknowledge
        self.diagnose = diagnose
        self.workaround = workaround
        self.fix = fix
        self.handoff = True if handoff else False
        self.lro = True if lro else False
        self.nlro = True if nlro else False
        self.facility = unicode(facility)
        self.ctas = ctas
        self.summary = "** NONE ***" if type(summary) is NoneType else summary.replace("'","")
        self.raised = raised.replace("'","")
        self.code = 0 if code is None else code
        self.production = None
        self.dbid = None

    def __repr__(self):
        return "[{}] ID:{} P{} Prod:{} Begin:{} A:{} D:+{}s W:+{}s F:+{}s\nH/O:{} LRO:{} NLRO:{} Facility={} CTAS={}\nSummary:'{}',Raised:'{}',Code:{}".format(
        self.id_incident,self.dbid, self.priority, self.production, self.begin,
        self.acknowledge, self.diagnose, self.workaround, self.fix,
        self.handoff, self.lro, self.nlro, self.facility, self.ctas,
        self.summary, self.raised, self.code)

    def ProcessIncident(self, cursor, facilities, productions):
        """
        Produces the SQL necessary to insert the incident in to the Access
        database, executes it and then gets the autonumber ID (dbid) of the newly
        created incident (this is used so LRO, NRLO CTAS and AD1 can refer to
        their parent incident.

        If the incident is classed as LRO, NLRO, CTAS then the appropriate
        record is created. Returns the dbid.
        """
        if self.raised.upper() in productions:
            self.production = productions[self.raised.upper()]
        else:
           self.production = 0

        sql="""INSERT INTO INCIDENTS (ID_INCIDENT, PRIORITY, FACILITY, BEGIN,
        ACKNOWLEDGE, DIAGNOSE, WORKAROUND, FIX, HANDOFF, SUMMARY, RAISED, CODE, PRODUCTION)
        VALUES ('{}', {}, {}, #{}#, {}, {}, {}, {}, {}, '{}', '{}', {}, {})
        """.format(self.id_incident, self.priority, facilities[self.facility], self.begin,
           self.acknowledge, self.diagnose, self.workaround, self.fix,
           self.handoff, self.summary, self.raised, self.code, self.production)
        cursor.execute(sql)
        cursor.execute("SELECT @@IDENTITY")
        self.dbid = cursor.fetchone()[0]

        if self.lro:
            self.ProcessLRO(cursor, facilities[self.facility])

        if self.nlro:
            self.ProcessNLRO(cursor, facilities[self.facility])

        if self.ctas:
            self.ProcessCTAS(cursor, facilities[self.facility], self.ctas)

        return self.dbid


class S7AD1:
    """
    S7.AD1 records.
    """
    def __init__(self, id_ad1, date, ref, commentary, adjustment):
        self.id_ad1 = id_ad1
        self.date = date
        self.ref = unicode(ref)
        self.commentary = unicode(commentary)
        self.adjustment = float(adjustment)
        self.pid = 0
        self.production = 0

    def __repr__(self):
        return "[{}] Date:{} Parent:{} PID:{} Amount:{} Commentary: {} "\
           .format(self.id_ad1, self.date.strftime("%d/%m/%y"), self.ref, self.pid, self.adjustment, self.commentary)

    def SetPID(self, pid):
        self.pid = pid

    def SetProduction(self, p):
        self.production = p

    def Process(self, cursor):
        sql = "INSERT INTO AD1 (pid, begin, commentary, production, adjustment) VALUES ({}, #{}#, '{}', {}, {})"\
          .format(self.pid, self.date.strftime("%d/%m/%y"), self.commentary, self.production, self.adjustment)
        cursor.execute(sql)

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
    """
    Miscellaneous S7 SC3 stuff. The new table is identical to the old one.
    """
    def __init__(self, begin, month, year, p1ot, p2ot, totchg, succchg, chgwithinc, fldchg, egychg):
        self.begin = begin
        self.p1ot = p1ot
        self.p2ot = p2ot
        self.changes = totchg
        self.successful = succchg
        self.incidents = chgwithinc
        self.failed = fldchg
        self.emergency = egychg

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
