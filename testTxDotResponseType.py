#-------------------------------------------------------------------------------
# Name:        testTxDotResponse
# Purpose:     input reponses from TX DMV RTS database, in raw text format.
#
# Author:      mthornton
#
# Created:     2017 MAR 31
# Updates:     2017 APR 04
# Copyright:   (c) mthornton 2017
# input(s)     tempResponseTypes.txt
# output(s)    tempResponseResults.txt
#-------------------------------------------------------------------------------

import re
import io
import csv
import string

from TxDot_LIB import findResponseType, cleanUpString, repairLineBreaks, parseRecord, csvStringFromList

def main():
    # move to LIB ?? as
    with open('tempResponseResults.txt', 'a') as outfile, \
         open('tempResponseTypes.txt', 'r') as infile, \
         open('tempPlates.txt', 'r') as platefile:

        outfile.truncate()
        plates = platefile.readlines()

        for plate in plates:
            plate = plate.strip()
            if plate is None or plate == "":
                break
            results = infile.read()
            if (results is not None and results != ""):
                ##print("main: ", results) # for debug
                fileString = repairLineBreaks(results)
                ##print("main: ", fileString) # for debug
            foundCurrentPlate = False
            while True:
                try:
                    responseType, startNum, endNum = findResponseType(plate, fileString)
                except:
                    responseType = None
                    if foundCurrentPlate == False:
                        print("\n", plate, ' Plate/Pattern not found')
                        outfile.write(',' + plate + ' Plate/Pattern not found\n')
                    break
                if responseType is not None:
                    foundCurrentPlate = True
                    print('main:', responseType, startNum, endNum)
                    # save only the 'core' string
                    typeString = fileString[startNum:endNum + 1]
                    ##print("main: ", typeString) # for debug
                    #remove the current working string from the larger string
                    fileString = fileString[:startNum] + fileString[endNum + 1:]
                    listData = parseRecord(responseType, typeString)
                    print("main: ", listData) # for debug
                    csvString = csvStringFromList(listData)
                    outfile.write(csvString)
        outfile.write('----------------\n')
        outfile.flush()
    print("main: Finished.")

if __name__ == '__main__':
    main()
