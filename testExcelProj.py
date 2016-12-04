# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        testExcelProj.py
# Purpose:     demostrate the feasibilty of some process automation
#
# Author:      mthornton
#
# Created:     01 DEC 2016
# Modified:    03 DEC 2016
# Copyright:   (c) mthornton 2016
#-------------------------------------------------------------------------------


import datetime
import pyodbc
import string
import tkFileDialog
import tkMessageBox
from Tkinter import *
from TxDot_LIB import *
import xlwings


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


def waitForUser(msg="enter login credentials"):
    #Wait for user input
    root = Tk()
    tkMessageBox.askokcancel(message=msg)
    root.destroy()


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
        sql.append(", [Start Date], [End Date]")
        sval.append(", '{start_date}', '{end_date}'")
        sql.append(", [Vehicle Make], [Vehicle Model], [Vehicle Body]")
        sval.append(", '{make}', '{model}', '{body}'")
    if dictStruct["vehicle_year"]!=0:
        sql.append(", [Vehicle Year]")
        sval.append(", {vehicle_year}")
    sql.append(", [Total Image Reviewed], [Total Image corrected], Reason, \
[Time_Stamp], [Agent Initial], \
[Sent to Collections Agency],  Multiple, Unassign, [Completed: Yes / No Record], \
[E-Tags (Temporary Plates)], [Dealer Plates] )")
    sval.append(", '{images_reviewed}', '{images_corrected}', '{reason}', \
'{time_stamp}', '{agent}', \
{collections}, {multiple}, {unassign}, '{completed}', \
{temp_plate}, {dealer_plate} )")
    SQL = "".join(sql)
    SVAL = "".join(sval)
    return SQL + SVAL


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



def commonCode(lpList):
    if txdotBool:
        txDriver = openBrowser('https://mvinet.txdmv.gov')
        waitForUser('enter credentials for DMV')
    if vpsBool:
        driver = openBrowser(parameters['url'])
        waitForUser('VPS login')

    try:
        for cell in lpList:
            cell = str(cell)
            if cell is None:
                print "main() : Finished, no more LP's ."
                break
            plateString = cell

            #VPS section   *****************************************************************
            if vpsBool:
                startPageTextLocator = (By.XPATH, '//TD/H1[contains(text(),"Violation Search")]')
                ##startWindow = findTargetPage(driver, findWindowDelay, startPageTextLocator, "mainframe")
                startWindow = findTargetPage(driver, findWindowDelay, startPageTextLocator)
                if startWindow is None:
                    print "Start Page not found."
                    break
                element = findElementOnPage(driver, delay, parameters['inputLocator'])
                submitted = fillFormAndSubmit(driver, startWindow, element, plateString, parameters) # why so slow?  IeDriver64 ??
                time.sleep(1)  #page may not be there yet!  how long to wait?
                pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['staleLocator2'])
                foundFrame = findAndSelectFrame(driver, delay, "fraRL")
                #time.sleep(1)  #text may not be there yet!  how long to wait?
                text = getTextResults(driver, delay, plateString, parameters, "fraRL")
                if text is not None: # if there is text, process it
                    sys.stdout.write("Initial # of " + plateString + ", " + str(text) + '\n')
                    startNum = int( str(text))
                    waitForUser('examine and correct images')
                    # navigate to search position
                    if type(parameters['buttonLocator']) is None: # no button, start at 'top' of the page
                        driver.switch_to_default_content()  # 'buttonLocator' : (By.XPATH,'//input[@value="Query"]'),
                    else: # there is a button. find it/click it/wait for page to load
                        clicked = findAndClickButton(driver, delay, parameters)
                        pageLoaded = newPageElementFound(driver, delay, None, parameters['staleLocator'])
                    element = findElementOnPage(driver, delay, parameters['inputLocator'])
                    submitted = fillFormAndSubmit(driver, startWindow, element, plateString, parameters) # why so slow?  IeDriver64 ??
                    time.sleep(1)  #page may not be there yet!  how long to wait?
                    pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['staleLocator2'])
                    foundFrame = findAndSelectFrame(driver, delay, "fraRL")
                    #time.sleep(1)  #text may not be there yet!  how long to wait?
                    text = getTextResults(driver, delay, plateString, parameters, "fraRL")
                    endNum = int( str(text))
                    diffNum = startNum - endNum
                    print  startNum, endNum, diffNum
                # navigate to search position
                if type(parameters['buttonLocator']) is None: # no button, start at 'top' of the page
                    driver.switch_to_default_content()
                else: # there is a button. find it/click it/wait for page to load
                    pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['staleLocator2'])
                    foundFrame = findAndSelectFrame(driver, delay, "fraRL")
                    clicked = findAndClickButton(driver, delay, parameters)
                    pageLoaded = newPageElementFound(driver, delay, None, parameters['staleLocator'])

            if txdotBool:
                #TXDOT section   *****************************************************************
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

            if dbBool:
                # Database section   *****************************************************************
                for csvRecord in recordList:
                    txDotRecord = txDotDataFill(txDotDataInit(), csvRecord)
                    dbRecord = recordInit()
                    dbRecord = txDotToDbRecord(txDotRecord, dbRecord)
                    print dbRecord # for debug
                    sqlString = makeSqlString(dbRecord)
                    #print sqlString # for debug
                    sql = sqlString.format(**dbRecord)
                    """sql = "INSERT INTO Sheet1 (Plate, Plate_St, [Combined Name], Address, City, State, ZipCode, \
                                              [Title Date], [Start Date], [End Date], \
                                              [Vehicle Make], [Vehicle Model], [Vehicle Body], [Vehicle Year], \
                                              [Total Image Reviewed], [Total Image corrected], Reason, \
                                              [Time_Stamp], [Agent Initial], \
                                              [Sent to Collections Agency],  Multiple, Unassign, [Completed: Yes / No Record], \
                                              [E-Tags (Temporary Plates)], [Dealer Plates] \
                                              ) \
                                VALUES (    '{plate}', '{plate_st}', '{combined_name}', '{address}', '{city}', '{state}', {zip}, \
                                            '{title_date}', '{start_date}', '{end_date}', \
                                            '{make}', '{model}', '{body}', {vehicle_year},\
                                             {images_reviewed}, {images_corrected}, '{reason}', \
                                            '{time_stamp}', '{agent}', \
                                             {collections}, {multiple}, {unassign}, '{completed}', \
                                             {temp_plate}, {dealer_plate} \
                                             ) ".format(**dbRecord)"""
                    '''"title_month":'', "title_day":'', "title_year":'','''   # where is this added ?
                    dbcursor.execute(sql)
                print("Comitting changes")
                dbcursor.commit()
                time.sleep(SLEEPTIME)

# from TxDot lib --> ['response type', 'plate', 'name', 'addr', 'addr2', 'city', 'state', 'zip', 'ownedStartDate', 'startDate', 'endDate', 'issued']
#"""  ALMOST FULL WRITE TO DATABASE missing title day, month, year -->  this will never happen. some fields are exclusive of others. """

    finally:
        if dbBool:
            print("Closing databases")
            dbConnect.close()
        if vpsBool:
            driver.close() # close browser window
            driver.quit()  # close command (cmd) window
        if txdotBool:
            txDriver.close()
            txDriver.quit()

def excelHook():
    indexList = range(1,NUMBERtoProcess)
    plates = [str( xlwings.Range((i,2)).value ) for i in indexList]
    commonCode(plates)

    xlwings.Range((2,2)).options(transpose=True).value = [ j+1 for j in indexList]


# global costants
NUMBERtoProcess = 7
vpsBool   = False  # true when using VPS images
txdotBool = True # true when using DMV records
dbBool    = False # true when using access file
findWindowDelay = 1
SLEEPTIME = 0 #180
delay=10
parameters = setParameters()
parameters['operatorMessage'] = "Use debug mode, \n open VPS, new violator search window, \n open DMV window, \n run to completion"
#print parameters['operatorMessage']


if __name__ == '__main__':
    excelHook()


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


