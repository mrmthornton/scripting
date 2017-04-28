# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        testTxDotResponse
# Purpose:     input reponses from TX DMV RTS database, in raw text format.
#
# Author:      mthornton
#
# Created:     2017 MAR 31
# Updates:     2017 APR 19
# Copyright:   (c) mthornton 2017
#
#-------------------------------------------------------------------------------

from TxDot_LIB import findResponseType, repairLineBreaks, parseRecord, csvStringFromList

def extractFields(plate, fileString, logfile=None): #TODO make outfile optional >>/dev/null?
    """
    plates - a clean licence plate string
    fileString  -  the input text as a single string
    logfile - a file handle for the log of events
    """
    if logfile is None: outfile = open("nul", 'w')
    else: outfile = logfile

    listData = []
    foundCurrentPlate = False
    while True:
        try:
            responseType, startNum, endNum = findResponseType(plate, fileString)
        except:
            responseType = None
            if foundCurrentPlate == False:
                print('extractFields: Searching for plate "', plate, '". Plate or Pattern not found.')
                outfile.write('extractFields: ' + plate + ' Plate/Pattern not found\n')
            break
        if responseType is not None:
            foundCurrentPlate = True
            ##print('extractFields: type, start, end: ', responseType, startNum, endNum) # for debug
            # save only the 'core' string
            typeString = fileString[startNum:endNum + 1] # extract the string for the specific type
            ##print("extractFields: typestring: ", typeString) # for debug
            #remove the current working string from the larger string
            fileString = fileString[:startNum] + fileString[endNum + 1:] #the rest of the original string
            listData = parseRecord(responseType, typeString)
            assert(len(listData)==17)
            #print("extractFields: listdata: ", listData) # for debug
            csvString = csvStringFromList(listData)
            outfile.write(csvString)
    outfile.write('----------------\n')
    outfile.flush()
    if logfile is None: outfile.close()
    return listData


def main():
    with open('testCasesNoPii.txt', 'r') as infile, \
         open('platesNoPii.txt', 'r') as platefile, \
         open('tempResponseResults.txt', 'w') as outfile:
        outfile.truncate()

        results = infile.read()
        if (results is not None and results != ""):  # why check for None? TODO
            ##print("main: ", results) # for debug
            fileString = repairLineBreaks(results)
            ##print("main: ", fileString) # for debug
        platesRaw = platefile.readlines()
        plates = [plate.strip().upper() for plate in platesRaw if plate is not None or plate !=""]  # why check for None? TODO
        for plate in plates:
            print(extractFields(plate, fileString))

    print("main: Finished.")


if __name__ == '__main__':
    main()

