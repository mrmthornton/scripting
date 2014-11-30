#-------------------------------------------------------------------------------
# Name:        parseTxDot
# Purpose:     read text output from the TxDot DMV database lookup
#
# Author:      mthornton
#
# Created:     24/11/2014
# Copyright:   (c) mthornton 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import re
import io
import xlrd
import xlwr

def findStartEnd(fileString,startPattern, endPattern):
    # the iterator is used to search for all possible endLoc instances,
    # since the search of a substring uses a smaller set of numbers
    found = startPattern.search(fileString)
    if found != None:
        startLoc = found.start()
        #print "findStartEnd: found start", startLoc
        iterator = endPattern.finditer(fileString)
        for found in iterator:
            if found.start() > startLoc and found != None:
                endLoc = found.end()
                #print "findStartEnd: found end", endLoc
                return [startLoc,endLoc]
    return [None, None]

def findResponseType(plate, fileString):

    # NO RECORD
    targetType = 'NORECORD'
    startPattern = re.compile('REG 00' + '[\s]+' + plate)
    endPattern = re.compile('NO RECORD IN RTS DATABASE')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  '\nfindResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # DEALER
    targetType = 'DEALER'
    startPattern = re.compile('DEALER' + '[\s]+' + plate)
    endPattern = re.compile('CODE ' + '[A-Z]{2,2}' + '[\s]+' + '[0-9]+')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  '\nfindResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # STANDARD
    targetType = 'STANDARD'
    startPattern = re.compile('LIC ' + plate + ' [A-Z]{3,3}' + '/' '[0-9]{4,4}')
    endPattern = re.compile('TITLE' + '[.]')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  '\nfindResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # TXIRP
    targetType = 'TXIRP'
    startPattern = re.compile('LIC ' + plate + ' EXPIRES')
    endPattern = re.compile('REMARKS')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  '\nfindResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # PERMIT
    targetType = 'PERMIT'
    startPattern = re.compile('SELECTION REQUEST:' + '[\s]+' + 'PERMIT'
                                                            + '[\s]+' + plate)
    endPattern = re.compile('ISSUING OFFICE: ')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  '\nfindResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # TEMPORARY
    targetType = 'TEMPORARY'
    startPattern = re.compile('SELECTION REQUEST:' + '[\s]+' + 'TEMPORARY TAG' + '[\s]+' + plate)
    endPattern = re.compile('[0-9]{5,5}' + '-' + '[0-9]{4,4}')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  '\nfindResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # PLACARD
    targetType = 'PLACARD'
    startPattern = re.compile('SELECTION REQUEST:' + '[\s]+' + 'PLACARD')
    endPattern = re.compile('SELECTION REQUEST:' + '[\s]+' + 'PLACARD')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  '\nfindResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # CANCELED
    targetType = 'CANCELED'
    canceledPattern = re.compile(plate + '[ ]*' + '(CANCELED|CANCELLED)')
    canceledStartPattern = re.compile('LIC ' + '[A-Z0-9]+' + ' [A-Z]{3,3}' + '/' '[0-9]{4,4}')
    canceledEndPattern = re.compile('TITLE' + '[.]')
    found = canceledPattern.search(fileString)
    foundtemp = found.group()
    if found != None:
        startCancel = found.start()
        startNumbers = canceledStartPattern.finditer(fileString)
        startNum = 0
        for e in startNumbers:
            num = e.start()
            if num < startCancel and num > startNum:
                startNum = num
            else:
                break
        foundEnd = canceledEndPattern.search(fileString[startNum:])
        endNum = foundEnd.end()
        endNum += startNum
        print  '\nfindResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]


    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print 'findResponseType:CANCELED:', startNum, endNum

        assert found != None and startNum < found.start() and found.end() < endNum
        print  '\nfindResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    return None

def parseRecord(responseType, typeString):
    if responseType == 'NORECORD':
        return parseNoRecord(responseType, typeString)
    if responseType == 'PLACARD':# effectively, no record, not a plate number
        return parseNoRecord(responseType, typeString)
    if responseType == 'DEALER':
        return parseDealer(responseType, typeString)
    if responseType == 'STANDARD':
        return parseStandard(responseType, typeString)
    if responseType == 'TXIRP':
        return parseTxirp(responseType, typeString)
    if responseType == 'PERMIT':
        return parsePermit(responseType, typeString)
    if responseType == 'TEMPORARY':
        return parseTemporary(responseType, typeString)
    if responseType == 'CANCELED':
        return parseCanceled(responseType, typeString)
    return None


#['response type', 'plate', 'name', 'addr', 'apt', 'city', 'state', 'zip', 'owned']
linePattern = re.compile('^.+')
wordPattern = re.compile('\w+')
csvPattern = re.compile('[A-Z0-9 .#]*,')
commaToEOLpattern = re.compile(',[A-Z0-9 .#]+$')
LICpattern = re.compile('^LIC ')
issuedPattern = re.compile('ISSUED ')
reg_dtPattern = re.compile('REG DT ')
datePattern = re.compile('[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}') # mo/dy/year

def parseNoRecord(responseType, typeString):
    noRecordPattern = re.compile('REG 00 ')
    header = noRecordPattern.search(typeString)
    typeString = typeString[header.end():]
    nextWord = wordPattern.search(typeString)
    plate = nextWord.group()
    return [responseType, plate, '', '', '', '', '', '', '']

def parseDealer(responseType, typeString):
    dealerPattern = re.compile('DEALER' + '[\s]+')
    #strip header
    header = dealerPattern.search(typeString)
    typeString =  typeString[header.end():]
    #get plate and remove line
    foundPlate = linePattern.search(typeString)
    plate = foundPlate.group()
    typeString =  typeString[foundPlate.end() + 1:]
    #remove next line
    nextLine = linePattern.search(typeString)
    typeString =  typeString[nextLine.end() + 1:]
    # get name and remove next line
    nextLine = linePattern.search(typeString)
    name = nextLine.group()
    typeString =  typeString[nextLine.end() + 1:]
    # get name and remove next line
    nextLine = linePattern.search(typeString)
    addr = nextLine.group()
    typeString =  typeString[nextLine.end() + 1:]
    #get city and remove
    nextWord = wordPattern.search(typeString)
    city = nextWord.group()
    typeString =  typeString[nextWord.end() + 1:]
    # get state and remove
    nextWord = wordPattern.search(typeString)
    state = nextWord.group()
    typeString =  typeString[nextWord.end() + 1:]
    #get zip
    nextWord = wordPattern.search(typeString)
    zip = nextWord.group()
    typeString =  typeString[nextWord.end() + 1:]
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zip, '']

def parseStandard(responseType, typeString):
    # remove header
    header = LICpattern.search(typeString)
    typeString = typeString[header.end():]
    nextWord = wordPattern.search(typeString)
    # get plate and remove
    plate = nextWord.group()
    typeString = typeString[header.end():]
    # get ISSUED date and remove
    nextRemove = issuedPattern.search(typeString)
    typeString = typeString[nextRemove.end():]
    nextDate = datePattern.search(typeString)
    issued = nextDate.group()
    # get REG DT
    nextRemove = reg_dtPattern.search(typeString)
    typeString = typeString[nextRemove.end():]
    nextDate = datePattern.search(typeString)
    reg_dt = nextDate.group()
    # get owner and remove
    ownerPattern = re.compile('OWNER\s+')
    nextRemove = ownerPattern.search(typeString)
    typeString = typeString[nextRemove.end():]
    nextCsv = csvPattern.search(typeString)
    name = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get second  owner and remove
    nextCsv = csvPattern.search(typeString)
    name2 = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get addr and remove
    nextCsv = csvPattern.search(typeString)
    addr = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get addr2 and remove
    nextCsv = csvPattern.search(typeString)
    addr2 = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get city and remove
    nextCsv = csvPattern.search(typeString)
    city = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get state and remove
    nextCsv = csvPattern.search(typeString)
    state = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get zip
    nextWord = wordPattern.search(typeString)
    zip = nextWord.group().replace(',' , '')
    # check for RNWL RCP entries and replace OWNER entries
    renewalPattern = re.compile('RNWL RCP\s+')
    nextRemove = renewalPattern.search(typeString)
    if nextRemove != None:
        typeString = typeString[nextRemove.end():]
        nextCsv = csvPattern.search(typeString)
        Rname = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get addr and remove
        nextCsv = csvPattern.search(typeString)
        Raddr = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get addr2 and remove
        nextCsv = csvPattern.search(typeString)
        Raddr2 = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get city and remove
        nextCsv = csvPattern.search(typeString)
        Rcity = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get state and remove
        nextCsv = csvPattern.search(typeString)
        Rstate = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get zip
        nextWord = wordPattern.search(typeString)
        Rzip = nextWord.group().replace(',' , '')
        # replace renewal information with owner informaton,
        # if the renewal information exists.
        if Rname != '':
            name = Rname
        if Raddr != '':
            addr = Raddr
        if Raddr2 != '':
            name2 = Raddr2
        if Rcity != '':
            city = Rcity
        if Rstate != '':
            state = Rstate
        if Rzip != '':
            zip = Rzip
    #print [responseType, plate, issued, reg_dt, name, name2, addr, addr2, city, state, zip]
    return [responseType, plate.strip(), name.strip(), addr.strip(), addr2.strip(), city.strip(), state.strip(), zip, issued]

def parseTxirp(responseType, typeString):
    #remove first word and get plate
    nextWord = wordPattern.search(typeString)
    typeString =  typeString[nextWord.end() + 1:]
    nextWord = wordPattern.search(typeString)
    plate = nextWord.group()
    #find address line
    addrLinePattern = re.compile('ISSUED TO:')
    addrLine = addrLinePattern.search(typeString)
    typeString =  typeString[addrLine.end():]
    #parse addr-line string from end to front due to company ( company, inc. )
    addrLine = linePattern.search(typeString)
    addrString = addrLine.group()
    commaToZipPattern = re.compile(',[A-Z]{2,2}\s+[0-9]{5,5}')
    #get state and zip and split
    stateAndZip = commaToZipPattern.search(addrString)#why not ,toEOL?
    state, zip = stateAndZip.group().split()
    state = state.replace(',' , '')
    addrString = addrString[:stateAndZip.start()]
    #get city and remove
    nextCsv = commaToEOLpattern.search(addrString)
    addrString = addrString[:nextCsv.start()]
    city = nextCsv.group()
    city = city.replace(',' , '')
    #get addr and remove
    nextCsv = commaToEOLpattern.search(addrString)
    addrString = addrString[:nextCsv.start()]
    addr = nextCsv.group()
    addr = addr.replace(',' , '')
    #get name
    name = addrString.replace(',' , '')
    name = name.replace('.' , '')
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zip, '']

def parsePermit(responseType, typeString):
    return [responseType]

def parseTemporary(responseType, typeString):
    # find header and remove
    startPattern = re.compile('SELECTION REQUEST:' + '[\s]+' + 'TEMPORARY TAG' + '[\s]+')
    header = startPattern.search(typeString)
    typeString = typeString[header.end():]
    # get plate
    nextWord = wordPattern.search(typeString)
    plate = nextWord.group()
    # find valid date string, and convert to issued date
    validDatePattern = re.compile(r'\d{4,4}/\d{2,2}/\d{2,2}')
    validDate = validDatePattern.search(typeString)
    dateYearFirst = validDate.group()
    issued = dateYearFirst[5:] + '/' + dateYearFirst[0:4]
    typeString = typeString[validDate.end():]
    # find name and address, remove everything up to that point
    tempNamePattern = re.compile(r'NAME:\s+')
    junk = tempNamePattern.search(typeString)
    typeString = typeString[junk.end():]
    # get name and remove
    nextCsv = csvPattern.search(typeString)
    name = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get addr and remove
    nextCsv = csvPattern.search(typeString)
    addr = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get city and remove
    nextCsv = csvPattern.search(typeString)
    city = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get state and remove
    nextCsv = csvPattern.search(typeString)
    state = nextCsv.group().replace(',' , '')
    typeString = typeString[nextCsv.end():]
    # get zip
    nextWord = wordPattern.search(typeString)
    zip = nextWord.group()
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zip, issued]

def parseCanceled(responseType, typeString):
    #save the plate
    plateCanceledPattern = re.compile(r'\w+' + '[ ]*' + 'CANCEL')
    plateCancel = plateCanceledPattern.search(typeString)
    plate = plateCancel.group()[:-6]
    # pass to parseStandard, since the format is the same
    parsedList = parseStandard(responseType, typeString)
    parsedList[1] = plate.strip()
    return parsedList


def csvStringFromList(listData):
    csvString = ''
    for stringValue in listData:
        csvString += stringValue + ', '
    if listData[0] == "NORECORD":
        csvString += "NORECORD" + ', '
    csvString += '\n'
    return csvString


def main():
    plates = ['BRS1234', 'PLATE100', 'PLATE99', '88K8888', 'OK1AHO', 'OKLAHO', '5F1234']
    #plates = ['889463G', '20N7867', 'DMY8231', '5F0629', '27E344', '27E344'
    #                                , '1E16714', '1A30026', 'BCM3557', '289868']
    with open('testFile.txt','r') as infile:
        with open('data.csv', 'w') as outfile:
            outfile.truncate()
            fileString = infile.read()
            for plate in plates:
                foundCurrentPlate = False
                while True:
                    try:
                        responseType, startNum, endNum = findResponseType(plate, fileString)
                    except:
                        responseType = None
                        if foundCurrentPlate == False:
                            print "\n", plate, 'No Informaton'
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
            outfile.flush()
            outfile.close()
            print "main: Finished parsing TxDot file."

if __name__ == '__main__':
    main()
