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
    # move to LIB ?? as
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

if __name__ == '__main__':
    main()
