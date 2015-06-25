#-------------------------------------------------------------------------------
# Name:        parseTxDot
# Purpose:     test parse modules
#
# Author:      mthornton
#
# Created:     25/06/2015
# Copyright:   (c) mthornton 2015
#-------------------------------------------------------------------------------

import io
import csv

from TxDotParse import repairLineBreaks
from TxDotParse import findResponseType
from TxDotParse import parseRecord
from TxDotParse import csvStringFromList

def main():

    with open('dealerPlates.csv', 'r') as plateFile:
        csvInput = csv.reader(plateFile)
        plates = [row[0] for row in csvInput]
        #print plates

    with open('txdotText.txt','r') as infile:
        with open('data.csv', 'a') as outfile:
            outfile.truncate()
            fileString = infile.read()
            fileString =  repairLineBreaks(fileString)
            for plate in plates:
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

# input - 'txdotText.txt'
# input - 'dealerPlates.csv'
# output - 'data.csv'
if __name__ == '__main__':
    main()
