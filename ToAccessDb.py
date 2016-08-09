# -*- coding: UTF-8 -*-
"""
Routine to migrate the S7 data from MySQL to the new Access
database.

We're using the pyodbc libraries to connect to Microsoft Access
Note that there are 32- and 64-bit versions of these libraries
available but in order to work the word-length for pyodbc and by
implication Python and all its associated compiled libraries must
match that of MS Access. Which is an arse as I've just had to
delete my 64-bit installation of Python and replace it and all
the libraries with the 32-bit version.

Tim Greening-Jackson 08 May 2013 (timATgreening-jackson.com)
"""

import pyodbc
import re
import datetime
import tkFileDialog
from Tkinter import *

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

    def ProcessLRO(self, cursor, facility):
        sql = "INSERT INTO LRO (PID, DURATION, FACILITY) VALUES ({}, {}, {})"\
              .format(self.dbid, self.workaround, facility)
        cursor.execute(sql)

    def ProcessNLRO(self, cursor, facility):
        sql = "INSERT INTO NLRO (PID, DURATION, FACILITY) VALUES ({}, {}, {})"\
              .format(self.dbid, self.workaround, facility)
        cursor.execute(sql)

    def ProcessCTAS(self, cursor, facility, code):
        sql = "INSERT INTO CTAS (PID, DURATION, FACILITY, CODE) VALUES ({}, {}, {}, {})"\
              .format(self.dbid, self.workaround, facility, self.ctas)
        cursor.execute(sql)


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

def ConnectToAccessFile():
        """
        Prompt the user for an Access database file, connect, create a cursor,
        get a hash of the facilities table keyed on facility name returning facility id
        """
        # Prompts the user to select which Access DB file he wants to use and then attempts to connect
        root = Tk()
        dbname = tkFileDialog.askopenfilename(parent=root, title="Select output database",
                    filetypes=[('Access locked', '*.accde'), ('Access db', '*.accdb')])
        root.destroy()
        # Connect to the Access (new) database and clean its existing incidents etc. tables out as
        # these will be replaced with the new data
        dbTXDOT = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+dbname+";")
        dbcursor=dbTXDOT.cursor()
        print("Connected to {}".format(dbname))

        dbcursor.execute("SELECT Plate FROM Sheet1")
        rowcount = 0
        #while True:
        #    row = dbcursor.fetchone()
        #    pyodbc.Cursor.fetchone.__get__
        #    if row is None:
        #        break
        #    rowcount += 1
        #    print (u"Plate {0}".format(row[0]))
        #    #print ("Plate {0}".format(row.get("Plate")))
        #print rowcount

        #for table in ["US STATE"]:
        #    #print("Clearing table {}...".format(table))
        #    #dbcursor.execute("DELETE * FROM {}".format(table))
        #    # Get the list of facilities from the Access database...
        #    dbcursor.execute("SELECT id, facility FROM facilities")
        #    rows = dbcursor.fetchall()
        #    dbfacilities = {unicode(row[1]):row[0] for row in rows}
        return dbTXDOT, dbcursor

# Entry point

incre = re.compile("INC\d{12}[A-Z]?") # Regex that matches incident references

try:
    dbTXDOT, dbcursor = ConnectToAccessFile()
    for row in dbcursor.columns(table='Sheet1'):
        print row.column_name
    #dbcursor.execute("SELECT * FROM Sheet1")
    dbcursor.execute("SELECT plate FROM [list of plate 9 without matching sheet1]")
    #dbcursor.execute("SELECT Plate, Plate_St, [Combined Name], Address, City, State, ZipCode, \
    #    [Title Date], [Start Date], [End Date], [Vehicle Make], [Vehicle Model], [Vehicle Body], [Vehicle Year], \
    #    [Total Image Reviewed], [Total Image corrected], Reason, [Time Stamp], [Agent Initial] \
    #    FROM Sheet1")
    """
    dict = {
    plate: , plate_st: , combined_name: , address: , city, state, zip, title_date,
    start_date, end_date, make, model, body, vehicle_year,
    images_reviewed, images_corrected, reason, time_stamp, agent,

    Title_Month
    Title_Day
    Title_Year
    [Sent to Collections Agency]
    Multiple
    Unassign
    [Completed: Yes / No Record]
    [E-Tags (Temporary Plates)]
    [Dealer Plates]
    """
    #dbcursor.execute("SELECT PLATE, PLATE_ST, COMBINED NAME, ADDRESS, CITY, ZIPCODE, STATE FROM Sheet1")
    #, TITLE DATE, START DATE, END DATE, VEHICLE MAKE, VEHICLE MODEL, VEHICLE BODY")
    rowcount = 0
    while True:
        row = dbcursor.fetchone()
        pyodbc.Cursor.fetchone.__get__
        if row is None:
            break
        rowcount += 1
        #print (u"Plate {0} {1}".format(row[0], row[1]))
        print row
    print rowcount
    ## Connect to the MySQL S7 (old) database and read the incidents and ad1 tables
    #s7cxn = pyodbc.connect("DRIVER={MySQL ODBC 3.51 Driver}; SERVER=localhost;DATABASE=s7; UID=root; PASSWORD=********; OPTION=3")
    #print("Connected to MySQL S7 database")
    #s7cursor = s7cxn.cursor()
    #s7cursor.execute("""
    #    SELECT id_incident, priority, begin, acknowledge,
    #    diagnose, workaround, fix, handoff, lro, nlro,
    #    facility, ctas, summary, raised, code FROM INCIDENTS""")
    #rows = s7cursor.fetchall()
    ## Discard any incidents which don't have a reference of the form INC... as they are ancient
    #print("Fetching incidents")
    #s7incidents = {unicode(row[0]):S7Incident(*row) for row in rows if incre.match(row[0])}

    ## Get the list of productions from the S7 database to replace the one we've just deleted ...

    #print("Fetching productions")
    #s7cursor.execute("SELECT DISTINCT RAISED FROM INCIDENTS")
    #rows = s7cursor.fetchall()
    #s7productions = [r[0] for r in rows]

    ## ... now get the AD1s ...

    #print("Fetching AD1s")
    #s7cursor.execute("SELECT id_ad1, date, ref, commentary, adjustment from AD1")
    #rows = s7cursor.fetchall()
    #s7ad1s = [S7AD1(*row) for row in rows]

    ## ... and the financial records ...

    #print("Fetching Financials")
    #s7cursor.execute("SELECT month, year, gco, cta, support, sc1, sc2, sc3, ad1 FROM Financials")
    #rows = s7cursor.fetchall()
    #s7financials = [S7Financial(*row) for row in rows]
    #print("Writing financials ({})".format(len(s7financials)))
    #[p.Process(dbcursor) for p in s7financials]

    ## ... and the SC3s.

    #print("Fetching SC3s")
    #s7cursor.execute("SELECT begin, month, year, p1ot, p2ot, totchg, succhg, chgwithinc, fldchg, egcychg from SC3")
    #rows = s7cursor.fetchall()
    #s7sc3s = [S7SC3(*row) for row in rows]
    #print("Writing SC3s ({})".format(len(s7sc3s)))
    #[p.Process(dbcursor) for p in s7sc3s]

    # Re-create the productions table in the new database. Note we refer to production
    # by number in the incidents table so need to do the SELECT @@IDENTITY to give us the
    # autonumber index. To make sure everything is case-insensitive convert the
    # hash keys to UPPERCASE.

    #dbproductions = {}
    #print("Writing productions ({})".format(len(s7productions)))
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

    print("Comitting changes")
    dbcursor.commit()
finally:
    print("Closing databases")
    dbTXDOT.close()
