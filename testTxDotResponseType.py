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

def main():
    # move to LIB ?? as  TODO
    inputFileName = 'testCasesNoPii.txt'
    plateFileName = 'platesNoPii.txt'
    outputFileName = 'tempResponseResults.txt'

    with open(outputFileName, 'w') as outfile, \
         open(inputFileName, 'r') as infile, \
         open(plateFileName, 'r') as platefile:

        outfile.truncate()

        results = infile.read()
        if (results is not None and results != ""):
            ##print("main: ", results) # for debug
            fileString = repairLineBreaks(results)
            ##print("main: ", fileString) # for debug

        plates = platefile.readlines()
        for plate in plates:
            plate = plate.strip().upper()
            if plate is None or plate == "":
                break

            foundCurrentPlate = False
            while True:
                try:
                    responseType, startNum, endNum = findResponseType(plate, fileString)
                except:
                    responseType = None
                    if foundCurrentPlate == False:
                        print('main: Searching for plate "', plate, '". Plate or Pattern not found.')
                        outfile.write('main: ' + plate + ' Plate/Pattern not found\n')
                    break
                if responseType is not None:
                    foundCurrentPlate = True
                    ##print('main: type, start, end: ', responseType, startNum, endNum) # for debug
                    # save only the 'core' string
                    typeString = fileString[startNum:endNum + 1] # extract the string for the specific type
                    ##print("main: typestring: ", typeString) # for debug
                    #remove the current working string from the larger string
                    fileString = fileString[:startNum] + fileString[endNum + 1:] #the rest of the original string
                    listData = parseRecord(responseType, typeString)
                    assert(len(listData)==17)
                    print("main: listdata: ", listData) # for debug
                    csvString = csvStringFromList(listData)
                    outfile.write(csvString)
        outfile.write('----------------\n')
        outfile.flush()
    print("main: Finished.")


from TxDot_LIB import findAmbiguousPlates

def testAmbig():
    text = """
LIC JJJ111 JAN/2018 OLD # DONN   JAN/2017 EWT  5200 GWT   6200
PASSENGER-TRUCK PLT, STKR            REG CLASS  35   $ 83.25 HARRISON CNTY
TITLE 12345678901234567 ISSUED 01/21/2017 ODOMETER 196765 REG DT 01/13/2017
YR:2009 MAK:FORD MODL:F1  BDY STYL:PK VEH CLS:TRK<=1     SALE PRC:       $0.00
VIN: 123VIN12345678901 BODY VIN: N/A COLOR: WHITE
PREV TTL: JUR TX TTL # 12345678901234567 ISSUE 06/22/2010
PREV OWN  DUB SIMPLETON,ALVARADO,TX
OWNER     DONALD TRUMP,,1 PENN AVE,,WASHINGTON,TX,75672
PLATE AGE:  0  LAST ACTIVITY 01/20/2017 RLSAUT OFC: 297
REMARKS PLATE POND   CANCELLED ON 2017/01/13.ACTUAL MILEAGE.DATE OF ASSIGNME
NT:2017/01/01.PAPER TITLE.
"""
    foundPlates = findAmbiguousPlates("P0ND", text)
    for eachPlate in foundPlates:
        print("testTxDotResponseType:testAmbig: ", eachPlate)

if __name__ == '__main__':
    main()
    testAmbig()

