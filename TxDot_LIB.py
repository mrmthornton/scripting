#-------------------------------------------------------------------------------
# Name:        TxDot_LIB
# Purpose:     code to parse the multi-formated results
#              retreived from the TX DMV RTS-database
#
# Author:      mthornton
#
# Created:     2014 NOV 24
# Update:      2016 OCT 24
# Copyright:   (c) mthornton 2014, 2015, 2016
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import re
import io
import csv
from VPS_LIB import *

linePattern = re.compile('^.+')
wordPattern = re.compile('\w+')
csvPattern = re.compile('[A-Z0-9 .#&]*,')
commaToEOLpattern = re.compile(',[A-Z0-9 .#&]+$')
LICpattern = re.compile('^LIC ')
issuedPattern = re.compile('ISSUED ')
reg_dtPattern = re.compile('REG DT ')
datePattern = re.compile('[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}') # mo/day/year
dateYearFirstPattern = re.compile(r'\d{4,4}/\d{2,2}/\d{2,2}') # year/mo/day

def repairLineBreaks(fileString):
    #broken keywords words have a pattern of
    # partial-word, newline(\n) white-space, partial word, identifier(, . -)

    # broken ZipPlus numbers have a pattern of
    # five-numbers, dash(-), [white space], [return(\r)], newline(\n), [white-space], partial-number or
    # partial-number, [white space], [return(\r)], newline(\n), [white-space], partial-number, dash(-), four-numbers

    # broken address lines ?

    wordBreakPattern = re.compile(r'[A-Z]+ *\n\s+[A-Z]+(,|\.|-)',re.MULTILINE) # find broken words
    while True:
        broken = wordBreakPattern.search(fileString)
        if broken != None:
            print 'repairLineBreaks:' + broken.group()
            fileStringBegin = fileString[:broken.start()]
            fileStringMiddle = broken.group()
            fileStringMiddle = fileStringMiddle.replace('\n', '')
            fileStringMiddle = fileStringMiddle.replace(' ', '')
            fileStringEnd = fileString[broken.end():]
            fileString = fileStringBegin + fileStringMiddle + fileStringEnd
            print 'repairLineBreaks:' + fileStringMiddle
        else:
            break
    #numberBreakPattern = re.compile(r'\d+\s*\n\s*\d*-\d{4,4}',re.MULTILINE) # find broken ZipPlus
    #numberBreakPattern = re.compile(r',\d{1,4}\s*\n\s*\d{2,4}',re.MULTILINE) # find broken Zip
    numberBreakPattern = re.compile(r',\d+\s*\n\s*\d+-',re.MULTILINE) # find broken Zip
    # total of 5 digits around a line break?
    zipPlusPattern = re.compile(r'\d{5,5}-\d{4,4}')
    zipCodePattern = re.compile(r',\d{5,5}')
    while True:
        broken = numberBreakPattern.search(fileString)
        if broken != None:
            print 'repairLineBreaks:' + broken.group()
            fileStringBegin = fileString[:broken.start()]
            fileStringMiddle = broken.group()
            fileStringMiddle = fileStringMiddle.replace('\n', '')
            fileStringMiddle = fileStringMiddle.replace(' ', '')
            fileStringEnd = fileString[broken.end():]
            #if re.search(zipPlusPattern, fileStringMiddle) != None:
            fileString = fileStringBegin + fileStringMiddle + fileStringEnd
            if re.search(zipCodePattern, fileString) != None:
                print 'repairLineBreaks:' + fileStringMiddle
        else:
            break
    #print 'repairLineBreaks:' + fileString
    return fileString

#def fixLine(lineString):
#    # repair lines broken with \n and/or \r and following spaces
##    # get owner line and remove
#    ownerStartPattern = re.compile(r'OWNER')
#    ownerEndPattern = re.compile(r' RNWL RCP| PLATE AGE:| LIEN')
#    ownerStartFound = ownerStartPattern.search(typeString)
#    ownerStart = ownerStartFound.start()
#    ownerEndFound = ownerEndPattern.search(typeString)
#    ownerEnd = ownerEndFound.start()
#    ownerLine = typeString[ownerStartFound.start():ownerEndFound.start()]
#    print 'parseStandard: ' + ownerLine
#    return lineString

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
    startPattern = re.compile('PLATE:' + '[\s]+' + plate)
    endPattern = re.compile('NO RECORD IN RTS DATABASE')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, plate
        return [targetType, startNum, endNum]

    # DEALER
    targetType = 'DEALER'
    startPattern = re.compile('DEALER' + '[\s]+' + plate)
    endPattern = re.compile('CODE ')
    #endPattern = re.compile('CODE ' + '[A-Z]{2,2}' + '[\s]+' + '[0-9]+')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, plate
        return [targetType, startNum, endNum]

    # STANDARD
    targetType = 'STANDARD'
    #startPattern = re.compile('LIC ' + plate + ' [A-Z]{3,3}' + '/' '[0-9]{4,4}')
    startPattern = re.compile('LIC ' + plate + ' [A-Z]{3,3}/[0-9]{4,4}')
    endPattern = re.compile(r'TITLE[.]|NON-TITLED|REMARKS')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, plate
        return [targetType, startNum, endNum]

    # TXIRP
    targetType = 'TXIRP'
    startPattern = re.compile('LIC ' + plate + ' EXPIRES')
    endPattern = re.compile('REMARKS')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, plate
        return [targetType, startNum, endNum]

    # PERMIT
    targetType = 'PERMIT'
    permitStartPattern = re.compile(r'SELECTION REQUEST:\s+PERMIT\s+' + plate)
    permitEndPattern = re.compile('ISSUING OFFICE: ')
    startNum, endNum = findStartEnd(fileString,permitStartPattern, permitEndPattern)
    if startNum != None:
        print  'findResponseType:', targetType, plate
        return [targetType, startNum, endNum]

    # TEMPORARY
    targetType = 'TEMPORARY'
    startPattern = re.compile(r'SELECTION REQUEST:\s+TEMPORARY TAG\s+' + plate)
    endPattern = re.compile(r',\w{2,2},\d{5,5}')  # ,ST,Zip
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, plate
        return [targetType, startNum, endNum]

    # SPECIAL
    targetType = 'SPECIAL'
    startPattern = re.compile(r'SPECIAL PLATE\s+' + plate)
    endPattern = re.compile(r'CODE XYZ')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, plate
        return [targetType, startNum, endNum]

    # PLACARD
    targetType = 'PLACARD'
    startPattern = re.compile(r'SELECTION REQUEST:\s+PLACARD\s+' + plate )
    endPattern = re.compile('DISABLED PERSON#:\s+\d+')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum != None:
        print  'findResponseType:', targetType, plate
        return [targetType, startNum, endNum]

    # CANCELED
    targetType = 'CANCELED'
    canceledPattern = re.compile(plate + '[ ]*' + '(CANCELED|CANCELLED)')
    canceledStartPattern = re.compile('LIC ' + '[A-Z0-9]+' + ' [A-Z]{3,3}' + '/' '[0-9]{4,4}')
    canceledEndPattern = re.compile('TITLE' + '[.]')
    found = canceledPattern.search(fileString)
    #foundtemp = found.group()     # found at least one cancelel pattern  # is this needed?
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
        print  'findResponseType:', targetType, plate
        return [targetType, startNum, endNum]
    return None

# parseRecord() calls the appropriate 'parse<RESPONSETYPE>()',
# which returns a list of strings as follows:
# ['response type', 'plate', 'name', 'addr', 'addr2', 'city', 'state', 'zip', 'ownedStartDate', 'startDate', 'endDate', 'issued']
# Other than 'response type' and 'plate', the strings may be empty.
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
    noRecordPattern = re.compile('PLATE: ')
    header = noRecordPattern.search(typeString)
    typeString = typeString[header.end():]
    nextWord = wordPattern.search(typeString)
    plate = nextWord.group()
    return [responseType, plate, '', '', '', '', '', '', '', '', '', '']

def parsePlacard(responseType, typeString):
    headerPattern = re.compile(r'SELECTION REQUEST:\s+PLACARD\s+')
    header = headerPattern.search(typeString)
    if header != None:
        typeString = typeString[header.end():]
        nextWord = wordPattern.search(typeString)
        if nextWord != None:
            plate = nextWord.group()
    return [responseType, plate.strip(), '', '', '', '', '', '', '', '', '', '']

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
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zip, '', '', '', '']

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
    return [responseType, plate.strip(), name.strip(), addr.strip(), addr2.strip(), city.strip(), state.strip(), zip, ownedStartDate, '', '', '']

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
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zip, '', '', '' , '']

def parsePermit(responseType, typeString):
    # find header and remove
    permitHeaderPattern = re.compile(r'(ONE TRIP PERMIT:|30 DAY PERMIT:|144-HOUR PERMIT:)\s+')
    header = permitHeaderPattern.search(typeString)
    typeString = typeString[header.end():]
    # find plate
    nextWord = wordPattern.search(typeString)
    plate = nextWord.group()
    # find  valid start date
    validDate = dateYearFirstPattern.search(typeString)
    dateYearFirst = validDate.group()
    issued = dateYearFirst[5:] + '/' + dateYearFirst[0:4]
    ##typeString = typeString[validDate.end():]
    # find header and remove
    permitNamePattern = re.compile(r'(APPLICANT NAME :|BUSINESS  NAME :)\s+')
    header = permitNamePattern.search(typeString)
    typeString = typeString[header.end():]
    # find name remove
    found = linePattern.search(typeString)
    name = found.group()
    typeString = typeString[found.end() + 1:] # remove, including \n
    # find addr1 and remove
    found = linePattern.search(typeString)
    addr = found.group()
    typeString = typeString[found.end() + 1:] # remove, including \n

    # find next line, remove and hold
    nextLine = linePattern.search(typeString)
    typeString = typeString[nextLine.end() + 1:]
    addr2 = nextLine.group()
    # find state and zip
    stateAndZipPattern = re.compile('[A-Z]{2,2}\s+[0-9]{5,5}')
    found = stateAndZipPattern.search(typeString)
    if found != None:
        state, zip = found.group().split()
        city = typeString[:found.start()]
    # if addr2 line is city, state, zip
    else:
        found = stateAndZipPattern.search(addr2)
        if found != None:
            state, zip = found.group().split()
            city = addr2[:found.start()]
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state, zip, '', '', '', issued]

def parseTemporary(responseType, typeString):
    # find header and remove
    startPattern = re.compile('SELECTION REQUEST:' + '[\s]+' + 'TEMPORARY TAG' + '[\s]+')
    header = startPattern.search(typeString)
    typeString = typeString[header.end():]
    # get plate
    nextWord = wordPattern.search(typeString)
    plate = nextWord.group()
    # find valid date string, and convert to Start Date
    validDate = dateYearFirstPattern.search(typeString)
    dateYearFirst = validDate.group()
    startDate = dateYearFirst[5:] + '/' + dateYearFirst[0:4]
    typeString = typeString[validDate.end():]
    # find valid date string, and convert to End Date
    validDate = dateYearFirstPattern.search(typeString) # why doesn't this work?
    dateYearFirst = validDate.group()
    endDate = dateYearFirst[5:] + '/' + dateYearFirst[0:4]
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
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zip, '', startDate, endDate, '']

    # SPECIAL
def parseSpecial(responseType, typeString):
    #find and remove header
    specialStartPattern = re.compile(r'SPECIAL PLATE\s+')
    header = specialStartPattern.search(typeString)
    typeString = typeString[header.end():]
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
    # find addr1 and remove
    nextLine = linePattern.search(typeString)
    typeString = typeString[nextLine.end() + 1:]
    addr = nextLine.group()
    # find next line, remove and hold
    nextLine = linePattern.search(typeString)
    typeString = typeString[nextLine.end() + 1:]
    addr2 = nextLine.group()
    # find state and zip
    stateAndZipPattern = re.compile('[A-Z]{2,2}\s+[0-9]{5,5}')
    found = stateAndZipPattern.search(typeString)
    if found != None:
        state, zip = found.group().split()
        city = typeString[:found.start()]
    # if addr2 line is city, state, zip
    else:
        found = stateAndZipPattern.search(addr2)
        if found != None:
            state, zip = found.group().split()
            city = addr2[:found.start()]
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zip, '', '', '', '']

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
        # remove any commas that may be part of the text,
        # since the delimiter is a comma.
        stringValue = stringValue.replace(',' , '') # remove any commas
        csvString += stringValue + ', '
    if listData[0] == "NORECORD":
        csvString += "NORECORD"
    if listData[0] == "PLACARD":
        csvString += "PLACARD"
    csvString += '\n'
    return csvString

def timeout():
    print "TxDotQuery: timeout!"
    quit()


def query(driver, delay, plate):
    # the input field is uniquely defined by the MANDATORY class attributes
    # class="v-textfield v-widget v-has-width iw-child v-textfield-iw-child iw-mandatory v-textfield-iw-mandatory"
    plateSubmitLocator = (By.XPATH, '//input[contains(@class,"v-textfield-iw-mandatory")]')
    plateSubmitElement = findElementOnPage(driver, delay, plateSubmitLocator)

    if plateSubmitElement is None:
        print "query: plate submission form not found on page"
        return None
    plateSubmitElement.clear()
    plateSubmitElement.send_keys(plate)
    plateSubmitElement.send_keys('\n')

    elemLocator =  (By.XPATH, '//div[@style="font-family: Courier New;"]')
    # wait until text element is rendered
    try:
        #WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element_value(elemLocator,plate))
        WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element(elemLocator,plate))
        textElement = findElementOnPage(driver, delay, elemLocator)
        uText = textElement.text
    except TimeoutException:
        print "ERROR: Timeout, record LP may not match input LP"
        return None
    plateSubmitElement.clear() # does this need to be cleaned to be found?
    return str(uText)

if __name__ == "__main__":
    # TEST 'repairLineBreaks()
    with open('temp.txt', 'r') as infile:
        raw = infile.readline()
        csv.reader(substr())
        platesCsv = csv.reader(infile.readline())
        lpList = [plate for plate in platesCsv]
        text = infile.read()
        print text
        text = repairLineBreaks(text)
        print text
        for lp in lpList:
            result = findResponseType(lp, text)
            if result is not None: print result[0]

