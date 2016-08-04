#-------------------------------------------------------------------------------
# Name:        TxDotToCSV
# Purpose:     gather output from TXDMV RTS database, parse the raw text,
#              and save to CSV text file
# Author:      mthornton
#
# Created:     2014 NOV 24
# Updates:     2016 FEB 11
# Copyright:   (c) mthornton 2014, 2015, 2016
# input(s)
# output(s)
#-------------------------------------------------------------------------------

import re
import io
import csv
import string

from TxDot_LIB import *

def main():

    #workbook = xlrd.open_workbook('plates.xlsx')
    #sheet = workbook.sheet_by_index(0)
    #print sheet
    #data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

    with open('plates.csv', 'r') as plateFile:
        csvInput = csv.reader(plateFile)
        plates = [row[0] for row in csvInput]
    #print plates

    with open('dataCSV.txt', 'a') as outfile, open('txdotText.txt', 'a') as rawTextFile:
        outfile.truncate()
        rawTextFile.truncate()
        for plate in plates:
            results = query(driver, delay, plate)
            if results is not None:
                print results # for debug
                rawTextFile.write(results)
                rawTextFile.write('\n\n------------------------------------\n\n')
                fileString = repairLineBreaks(results)
            foundCurrentPlate = False
            while True:
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
        outfile.write('----------------\n')
        outfile.flush()
    print "main: Finished parsing TxDot file."
    driver.close()


if __name__ == '__main__':
    #create an instance of IE and set some options
    driver = webdriver.Ie()
    delay=10
    url = 'https://mvinet.txdmv.gov'
    driver.get(url)
    main()
