#-------------------------------------------------------------------------------
# Name:        TxDot_VPS_compare_dates
# Purpose:     gather date ranges from TX-DMV, RTS database
#
# Author:      mthornton
#
# Created:     2016 JUL 25
# Updates:
# Copyright:   (c) mthornton 2016
# input - 'temp_plates.csv'
# output - 'temp_dates_CSV.txt'
#-------------------------------------------------------------------------------

import re
import io
import csv
import string

from TxDot_LIB import *

def txdot_body(driver, delay, plate):
    results = query(driver, delay, plate)
    if results is not None:
        print results # for debug
        rawTextFile.write(results)
        rawTextFile.write('\n\n------------------------------------\n\n')
        fileString = repairLineBreaks(results)
    foundCurrentPlate = False
    while True: # loop while there is more lp info sections
        try:
            responseType, startNum, endNum = findResponseType(plate, fileString)
        except:
            responseType = None
            if foundCurrentPlate == False:
                print "\n", plate, ' Plate/Pattern not found'
                outfile.write(',' + plate + ' Plate/Pattern not found\n')
            break
        if responseType != None:
            foundCurrentPlate = True
            #print 'main:', responseType, startNum, endNum
            typeString = fileString[startNum:endNum + 1]
            #print typeString
            fileString = fileString[:startNum] + fileString[endNum + 1:]
            listData = parseRecord(responseType, typeString)
            csvString = csvStringFromList(listData)
            outfile.write(csvString)

def credentials():
    # Go to the main web page and wait while the user enters credentials
    url = 'https://mvinet.txdmv.gov'
    driver.get(url)

#from TxDotQuery import credentials
#from TxDotQuery import connect
from TxDotQuery import query

if __name__ == '__main__':
    print "Login to TX DMV RTS database, navigate to INQUIRY-SINGLE PLATE"
    delay = 5
    driver = webdriver.Ie()
    credentials() # PAUSE after this to allow the user to enter credentials
    #connect()

    #workbook = xlrd.open_workbook('plates.xlsx')
    #sheet = workbook.sheet_by_index(0)
    #print sheet
    #data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    #read the input file
    with open('temp_plates.csv', 'r') as plateFile:
        csvInput = csv.reader(plateFile)
        plates = [row[0] for row in csvInput]

    #open the output file(s)
    with open('temp_dates_CSV.txt', 'a') as outfile, open('txdotText.txt', 'a') as rawTextFile:
        #outfile.truncate()
        #rawTextFile.truncate()

        #process the input
        for lp in plates:
            time.sleep(1)
#NEED a common data structure for these types of data: txdot , vps, database
            txdot_body(driver, delay, lp) #TXDOT PROCESSING
            #vps_body(driver,delay, lp) #VPS PROCESSING
            #db_body(driver, delay, lp) #DATABASE PROCESSING
        outfile.write('----------------\n')
        outfile.flush()
    print "main: Finished with input file."
