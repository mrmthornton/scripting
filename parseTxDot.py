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
#import xlrd
#import xlwt
#import xlutils
import csv

linePattern = re.compile('^.+')
wordPattern = re.compile('\w+')
csvPattern = re.compile('[A-Z0-9 .#]*,')
commaToEOLpattern = re.compile(',[A-Z0-9 .#]+$')
LICpattern = re.compile('^LIC ')
issuedPattern = re.compile('ISSUED ')
reg_dtPattern = re.compile('REG DT ')
datePattern = re.compile('[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}') # mo/day/year
dateYearFirstPattern = re.compile(r'\d{4,4}/\d{2,2}/\d{2,2}') # year/mo/day

def repairLineBreaks(fileString):
    #broken keywords words have a pattern of
    # partial-word, newline(\n) white-space, partial word, identifier(, . -)

    # broken ZipPlus numbers have a pattern of
    # partial-number, optional dash(-), partial-number, newline(\n), white-space, partial-number
    # or partial-number, newline(\n), white-space, partial-number, optional dash(-), partial-number

    # broken address lines ?

    wordBreakPattern = re.compile(r'[A-Z]+\n [A-Z]+(,|\.|-)') # find broken words
    while True:
        broken = wordBreakPattern.search(fileString)
        if broken != None:
            fileStringBegin = fileString[:broken.start()]
            fileStringMiddle = broken.group()
            fileStringMiddle = fileStringMiddle.replace('\n ', '')
            fileStringEnd = fileString[broken.end():]
            fileString = fileStringBegin + fileStringMiddle + fileStringEnd
        else:
            break
    numberBreakPattern = re.compile(r'\d+-\d*\n \d+|\d+\n \d*-\d+') # find broken numbers
    zipPlusPattern = re.compile(r'\d{5,5}-\d{4,4}')
    zipCodePattern = re.compile(r'\d{5,5}')
    while True:
        broken = numberBreakPattern.search(fileString)
        if broken != None:
            fileStringBegin = fileString[:broken.start()]
            fileStringMiddle = broken.group()
            fileStringMiddle = fileStringMiddle.replace('\n ', '')
            fileStringEnd = fileString[broken.end():]
            if re.search(zipPlusPattern, fileStringMiddle) != None:
                fileString = fileStringBegin + fileStringMiddle + fileStringEnd
                print 'repairLineBreaks:' + fileStringMiddle
        else:
            break
    #print 'repairLineBreaks:' + fileString
    return fileString

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
        print  'findResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # DEALER
    targetType = 'DEALER'
    startPattern = re.compile('DEALER' + '[\s]+' + plate)
    endPattern = re.compile('CODE ' + '[A-Z]{2,2}' + '[\s]+' + '[0-9]+')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # STANDARD
    targetType = 'STANDARD'
    startPattern = re.compile('LIC ' + plate + ' [A-Z]{3,3}' + '/' '[0-9]{4,4}')
    endPattern = re.compile(r'TITLE[.]|NON-TITLED')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # TXIRP
    targetType = 'TXIRP'
    startPattern = re.compile('LIC ' + plate + ' EXPIRES')
    endPattern = re.compile('REMARKS')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # PERMIT
    targetType = 'PERMIT'
    permitStartPattern = re.compile('SELECTION REQUEST:' + '[\s]+' + 'PERMIT' + '[\s]+' + plate)
    permitEndPattern = re.compile('ISSUING OFFICE: ')
    startNum, endNum = findStartEnd(fileString,permitStartPattern, permitEndPattern)
    if startNum != None:
        print  'findResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # TEMPORARY
    targetType = 'TEMPORARY'
    startPattern = re.compile('SELECTION REQUEST:' + '[\s]+' + 'TEMPORARY TAG' + '[\s]+' + plate)
    endPattern = re.compile('[0-9]{5,5}' + '-' + '[0-9]{4,4}')  #ZipPlus
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # SPECIAL
    targetType = 'SPECIAL'
    startPattern = re.compile(r'SPECIAL PLATE\s+' + plate)
    endPattern = re.compile(r'CODE XYZ')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # PLACARD
    targetType = 'PLACARD'
    startPattern = re.compile(r'SELECTION REQUEST:\s+PLACARD\s+' + plate )
    endPattern = re.compile('DISABLED PERSON#:\s+\d+')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]

    # CANCELED
    targetType = 'CANCELED'
    canceledPattern = re.compile(plate + '[ ]*' + '(CANCELED|CANCELLED)')
    canceledStartPattern = re.compile('LIC ' + '[A-Z0-9]+' + ' [A-Z]{3,3}' + '/' '[0-9]{4,4}')
    canceledEndPattern = re.compile('TITLE' + '[.]')
    found = canceledPattern.search(fileString)
    foundtemp = found.group()     # found at least one cancelel pattern
    # examine all start-positions for closest, but not past canceled-position
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
        # find the end position
        foundEnd = canceledEndPattern.search(fileString[startNum:])
        endNum = foundEnd.end()
        endNum += startNum
        print  'findResponseType:', targetType, startNum, endNum
        return [targetType, startNum, endNum]
    return None

# parse<RESPONSETYPE>() return a list of strings as follows
# ['response type', 'plate', 'name', 'addr', 'apt', 'city', 'state', 'zip', 'owned']
def parseRecord(responseType, typeString):
    if responseType == 'NORECORD':
        return parseNoRecord(responseType, typeString)
    if responseType == 'PLACARD':# effectively, no record, not a plate number
        return parsePlacard(responseType, typeString)
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
    if responseType == 'SPECIAL':
        return parseSpecial(responseType, typeString)
    if responseType == 'CANCELED':
        return parseCanceled(responseType, typeString)
    return None

def parseNoRecord(responseType, typeString):
    noRecordPattern = re.compile('REG 00 ')
    header = noRecordPattern.search(typeString)
    typeString = typeString[header.end():]
    nextWord = wordPattern.search(typeString)
    plate = nextWord.group()
    return [responseType, plate, '', '', '', '', '', '', '']

def parsePlacard(responseType, typeString):
    headerPattern = re.compile(r'SELECTION REQUEST:\s+PLACARD\s+')
    header = headerPattern.search(typeString)
    if header != None:
        typeString = typeString[header.end():]
        nextWord = wordPattern.search(typeString)
        if nextWord != None:
            plate = nextWord.group()
    return [responseType, plate.strip(), '', '', '', '', '', '', '']

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
    #get next word and remove
    nextWord = wordPattern.search(typeString)
    word = nextWord.group()
    typeString =  typeString[nextWord.end() + 1:]
    if len(word) != 2:
        city = city + ' ' + word
        # get state and remove
        nextWord = wordPattern.search(typeString)
        state = nextWord.group()
        typeString =  typeString[nextWord.end() + 1:]
    else:
        state = word
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
    nextDate = datePattern.match(typeString)
    if nextDate != None:
        ownedStartDate = nextDate.group()
    else:
        # get REG DT
        nextRemove = reg_dtPattern.search(typeString)
        typeString = typeString[nextRemove.end():]
        nextDate = datePattern.search(typeString)
        ownedStartDate = nextDate.group()
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
            name2 = ''
        if Raddr != '':
            addr = Raddr
            addr2 = Raddr2
            city = Rcity
            state = Rstate
            zip = Rzip
    #print [responseType, plate, reg_dt, name, name2, addr, addr2, city, state, zip, ownedStartDate]
    return [responseType, plate.strip(), name.strip(), addr.strip(), addr2.strip(), city.strip(), state.strip(), zip, ownedStartDate]

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
    permitHeaderPattern = re.compile(r'(ONE TRIP PERMIT:|30 DAY PERMIT:|144-HOUR PERMIT:)\s+')
    header = permitHeaderPattern.search(typeString)
    typeString = typeString[header.end():]
    nextWord = wordPattern.search(typeString)
    plate = nextWord.group()
    validDate = dateYearFirstPattern.search(typeString)
    dateYearFirst = validDate.group()
    issued = dateYearFirst[5:] + '/' + dateYearFirst[0:4]
    typeString = typeString[validDate.end():]
    permitNamePattern = re.compile(r'(APPLICANT NAME :|BUSINESS  NAME :)\s+')
    header = permitNamePattern.search(typeString)
    typeString = typeString[header.end():]
    found = linePattern.search(typeString)
    name = found.group()
    typeString = typeString[found.end() + 1:] # remove, including \n
    found = linePattern.search(typeString)
    addr = found.group()
    typeString = typeString[found.end() + 1:] # remove, including \n
    found = linePattern.search(typeString)
    cityToZip = found.group()
    typeString = typeString[:found.end()]
    nextWord = wordPattern.search(typeString)
    city = nextWord.group()
    typeString = typeString[nextWord.end() + 1:]
    nextWord = wordPattern.search(typeString)
    state = nextWord.group()
    typeString = typeString[nextWord.end() + 1:]
    nextWord = wordPattern.search(typeString)
    zip = nextWord.group()
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city, state, zip, issued]

def parseTemporary(responseType, typeString):
    # find header and remove
    startPattern = re.compile('SELECTION REQUEST:' + '[\s]+' + 'TEMPORARY TAG' + '[\s]+')
    header = startPattern.search(typeString)
    typeString = typeString[header.end():]
    # get plate
    nextWord = wordPattern.search(typeString)
    plate = nextWord.group()
    # find valid date string, and convert to issued date
    validDate = dateYearFirstPattern.search(typeString)
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
    # get addr1 and remove
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
    if len(city) == 2:
        state = city
        city = addr2
    else:
        # get state and remove
        nextCsv = csvPattern.search(typeString)
        state = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
    # get zip
    nextWord = wordPattern.search(typeString)
    zip = nextWord.group()
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zip, issued]

    # SPECIAL
def parseSpecial(responseType, typeString):
    #find and remove header
    specialStartPattern = re.compile(r'SPECIAL PLATE\s+')
    header = specialStartPattern.search(typeString)
    typeString = typeString[header.end() + 1:]
    # find plate and remove
    found = linePattern.search(typeString)
    typeString = typeString[found.end() + 1:]
    plate = found.group()
    # find next line, and remove
    nextLine = linePattern.search(typeString)
    typeString = typeString[nextLine.end() + 1:]
    # find name and remove
    nextLine = linePattern.search(typeString)
    typeString = typeString[nextLine.end() + 1:]
    name = nextLine.group()
    # find addr and remove
    nextLine = linePattern.search(typeString)
    typeString = typeString[nextLine.end() + 1:]
    addr = nextLine.group()
    # find state and zip
    stateAndZipPattern = re.compile('[A-Z]{2,2}\s+[0-9]{5,5}')
    found = stateAndZipPattern.search(typeString)
    state, zip = found.group().split()
    addrString = typeString[:found.start()]
    # find one or two lines,
    # if the line2 is empty, line one is 'city'
    # otherwise line one is 'addr2' and line2 is 'city'
    nextLine = linePattern.search(addrString)
    line1 = nextLine.group()
    addrString = addrString[nextLine.end() + 1:]
    nextLine = linePattern.search(addrString)
    if nextLine != None:
        line2 = nextLine.group()
        if line2.strip() != '':
            city = line2
            addr2 = line1
        else:
            city = line1
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zip, '']

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
        csvString += "NORECORD"
    if listData[0] == "PLACARD":
        csvString += "PLACARD"
    csvString += '\n'
    return csvString

def main():

    #workbook = xlrd.open_workbook('plates.xlsx')
    #sheet = workbook.sheet_by_index(0)
    #print sheet
    #data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

    with open('plates.csv', 'r') as plateFile:
        csvInput = csv.reader(plateFile)
        plates = [row[0] for row in csvInput]
    #print plates

    with open('testFile.txt','r') as infile:
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

if __name__ == '__main__':
    main()
