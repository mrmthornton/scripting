#-------------------------------------------------------------------------------
# Name:        TxDotToCSV
# Purpose:     gather output from TXDMV RTS database, parse the raw text,
#              and save to CSV text file
# Author:      mthornton
#
# Created:     24/11/2014
# Updates:     24/06/2015
# Copyright:   (c) mthornton 2014, 2015
#-------------------------------------------------------------------------------

import re
import io
import csv
import string

from TxDotParse import repairLineBreaks
from TxDotParse import findResponseType
from TxDotParse import parseRecord
from TxDotParse import csvStringFromList


def main():

    #workbook = xlrd.open_workbook('plates.xlsx')
    #sheet = workbook.sheet_by_index(0)
    #print sheet
    #data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

    with open('dealerPlates.csv', 'r') as plateFile:
        csvInput = csv.reader(plateFile)
        plates = [row[0] for row in csvInput]
    #print plates

    with open('dataCSV.txt', 'a') as outfile, open('txdotText.txt', 'a') as rawTextFile:
        outfile.truncate()
        rawTextFile.truncate()
        for plate in plates:
            results = query(plate)
            for e in results:
                rawTextFile.write(fileString)
                rawTextFile.write('\n\n------------------------------------\n\n')
                fileString = filter(lambda x: x in string.printable, e.text)
                print fileString

            fileString = repairLineBreaks(fileString)
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


from TxDotQuery import credentials
from TxDotQuery import connect
from TxDotQuery import query

# input - 'dealerPlates.csv'
# output - 'dataCSV.txt'
if __name__ == '__main__':
    credentials()
    connect()
    main()
