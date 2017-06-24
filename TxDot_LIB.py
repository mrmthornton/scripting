# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        TxDot_LIB
# Purpose:     code to parse the multi-formated results
#              retreived from the TX DMV RTS-database
#
# Author:      mthornton
#
# Created:     2014 NOV 24
# Updates:     2017 APR 27
# Copyright:   (c) mthornton 2014, 2015, 2016, 2017
#-------------------------------------------------------------------------------


import re
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from UTIL_LIB import nextIndex, permutationPattern, returnLargest
from VPS_LIB import findElementOnPage


linePattern = re.compile('^.+') # from start of line to newline(\n)
wordPattern = re.compile('\w+') # any non-whitespace
csvPattern = re.compile('[A-Z0-9 .#&]*,') #   almost-anything followed by a comma
commaToEOLpattern = re.compile(',[A-Z0-9 .#&]+$') # comma almost-anything end-of-line
LICpattern = re.compile(r'LIC\s+([A-Z0-9]{1,10})\s+[A-Z]{3,3}/[0-9]{4,4}')# group(1) is the LP
issuedPattern = re.compile('ISSUED ')
reg_dtPattern = re.compile('REG DT ')
datePattern = re.compile('[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}') # mo/day/year
dateYearFirstPattern = re.compile(r'\d{4,4}/\d{2,2}/\d{2,2}') # year/mo/day
zipPlusPattern = re.compile(r'\d{5,5}-\d{4,4}')
zipCodePattern = re.compile(r',\d{5,5}|\s+\w{2,2}\s+\d{5,5}')  # commaZIP or spaceSTspaceZIP


def csvStringFromList(listData):
    """
    Remove any commas that may be part of the text,
    since the new delimiter is a comma.
    """
    return insertCommas([removeCommas(e) for e in listData])


def findAmbiguousPlates(plate,text):
    platesPattern = permutationPattern(plate)
    foundIter = platesPattern.finditer(text)
    plateGen = (e.group() for e in foundIter)
    for foundPlate in plateGen: print("TxDot_LIB:findAmbiguousPlates: ", foundPlate) # debug
    return plateGen


def findStartEnd(fileString,startPattern, endPattern):
    # the iterator is used to search for all possible endLoc instances,
    # since the search of a substring uses a smaller set of numbers
    found = startPattern.search(fileString)
    if found is not None:
        startLoc = found.start()
        #print("findStartEnd: found start", startLoc)
        iterator = endPattern.finditer(fileString)
        for found in iterator:
            if found.start() > startLoc and found is not None:
                endLoc = found.end()
                #print("findStartEnd: found end", endLoc)
                return [startLoc,endLoc]
    return [None, None]


def findResponseType(plate, fileString):

    # NO RECORD
    startPattern = re.compile('PLATE:' + '[\s]+' + plate)
    endPattern = re.compile('NO RECORD IN RTS DATABASE')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum is not None:
        #print('TxDot_LIB: findResponseType::', targetType, plate)
        return ['NORECORD', startNum, endNum]

    # DEALER
    startPattern = re.compile('DEALER' + '[\s]+' + plate)
    endPattern = re.compile('CODE ')
    #endPattern = re.compile('CODE ' + '[A-Z]{2,2}' + '[\s]+' + '[0-9]+')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum is not None:
        #print('TxDot_LIB: findResponseType::', targetType, plate)
        return ['DEALER', startNum, endNum]

    # STANDARD
    startPattern = re.compile('LIC\s+' + plate + '\s+[A-Z]{3,3}/[0-9]{4,4}')
    endPattern = re.compile(r'TITLE[D.]')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum is not None:
        #print('TxDot_LIB: findResponseType::', targetType, plate)
        return ['STANDARD', startNum, endNum]

    # TXIRP
    startPattern = re.compile('LIC' + plate + ' EXPIRES')
    endPattern = re.compile('REMARKS')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum is not None:
        #print('TxDot_LIB: findResponseType::', targetType, plate)
        return ['TXIRP', startNum, endNum]

    # PERMIT
    permitStartPattern = re.compile(r'SELECTION REQUEST:\s+PERMIT\s+' + plate)
    permitEndPattern = re.compile('ISSUING OFFICE: ')
    startNum, endNum = findStartEnd(fileString,permitStartPattern, permitEndPattern)
    if startNum is not None:
        #print('TxDot_LIB: findResponseType::', targetType, plate)
        return ['PERMIT', startNum, endNum]

    # TEMPORARY
    startPattern = re.compile(r'SELECTION REQUEST:\s+TEMPORARY TAG\s+' + plate)
    endPattern = re.compile(r',\w{2,2},\d{5,5}')  # ,ST,Zip
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum is not None:
        #print('TxDot_LIB: findResponseType::', targetType, plate)
        return ['TEMPORARY', startNum, endNum]

    # SPECIAL
    startPattern = re.compile(r'SPECIAL PLATE\s+' + plate)
    endPattern = zipCodePattern
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum is not None:
        #print('TxDot_LIB: findResponseType::', targetType, plate)
        return ['SPECIAL', startNum, endNum]

    # PLACARD
    startPattern = re.compile(r'SELECTION REQUEST:\s+PLACARD\s+' + plate )
    endPattern = re.compile('DISABLED PERSON#:\s+\d+')
    startNum, endNum = findStartEnd(fileString,startPattern, endPattern)
    if startNum is not None:
        #print('TxDot_LIB: findResponseType::', targetType, plate)
        return ['PLACARD', startNum, endNum]

    # CANCELED
    canceledPattern = re.compile(plate + '[ ]*(CANCELED|CANCELLED)')
    canceledStartPattern = re.compile(r'LIC [A-Z0-9]{1,10} [A-Z]{3,3}/[0-9]{4,4}')
    canceledEndPattern = re.compile('TITLE[D.]')
    found = canceledPattern.search(fileString)
    if found is not None:
        startCancel = found.start()
        #print("TxDot_LIB: findResponseType: cancel found at: ", startCancel)
        backFromRemarksDistance = 1000  # how far back is the start? guesstimate.
        startSearchAt = returnLargest(0, startCancel-backFromRemarksDistance)
        #print("findResponseType:CANCELED: ",fileString[startSearchAt:]) # debug
        found = canceledStartPattern.search(fileString[startSearchAt:])
        startNum = found.start() + startSearchAt

        # find the end position
        ##print("findResponseType:CANCELED: ",fileString[startCancel:])
        foundEnd = canceledEndPattern.search(fileString[startCancel:])
        endNum = foundEnd.end() + startCancel
        #print ('findResponseType:', targetType, plate)
        return ['CANCELED', startNum, endNum]
    return None


def insertCommas(strings):
    """
    Insert commas between elements of a string list
    returning a single string.
    """
    return "".join([(e + ',') for e in strings])


def make(stringText):
    makPattern = re.compile('(?<=MAK:)\w+')
    make = makPattern.search(stringText)
    if make:
        return make.group()
    return ""


def model(stringText):
    modlPattern = re.compile('(?<=MODL:)\w+')
    modl = modlPattern.search(stringText)
    if modl:
        return modl.group()
    return ""



# parseRecord() calls the appropriate 'parse<RESPONSETYPE>()' function,
# which returns a list of strings as follows:
# ['response type', 'plate', 'name', 'addr', 'addr2', 'city', 'state', 'zipCode', 'ownedStartDate', 'startDate', 'endDate', 'issued',
#   yr, mak, modl, styl, vin]
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
    return [responseType, plate, '', '', '', '', '', '', '', '', '', '','','','','','']

def parsePlacard(responseType, typeString):
    headerPattern = re.compile(r'SELECTION REQUEST:\s+PLACARD\s+')
    header = headerPattern.search(typeString)
    if header is not None:
        typeString = typeString[header.end():]
        nextWord = wordPattern.search(typeString)
        if nextWord is not None:
            plate = nextWord.group()
    return [responseType, plate.strip(), 'NOT a licence plate!', '', '', '', '', '', '', '', '', '','','','','','']


def parseDealer(responseType, typeString): # TODO get expiration date
    dealerPattern = re.compile('DEALER[\s]+([\w]+)')
    header = dealerPattern.search(typeString)
    plate = header.group(1)
    #skip the rest of this line
    skipLine = linePattern.search(typeString)
    typeString =  typeString[skipLine.end() + 1:]
    ##genNewStr = nextIndex(typeString)
    ##shortenStr = genNewStr(header.end() + 1)
    ##s = shortenStr(header.end() + 1)
    ##print(s)
    #skip next line
    skipLine = linePattern.search(typeString)
    ###print(genNewStr(skipLine.end() + 1))
    typeString =  typeString[skipLine.end() + 1:]
    # get name and remove next line
    ##nextLine = linePattern.search(genNewStr(header.end() + 1))
    nextLine = linePattern.search(typeString)
    name = nextLine.group()
    print(typeString[header.end() + skipLine.end() + 1:])
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
    #get zipCode
    nextWord = wordPattern.search(typeString)
    zipCode = nextWord.group()
    typeString =  typeString[nextWord.end() + 1:]
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zipCode, '', '', '', '','','','','','']


def parseStandard(responseType, typeString):
    # remove header
    header = LICpattern.search(typeString)
    ##typeString = typeString[header.end():]
    ##nextWord = wordPattern.search(typeString)
    # get plate and remove
    plate = header.group(1)
    #plate = nextWord.group()
    typeString = typeString[header.end():]
    # get ISSUED date and remove
    nextRemove = issuedPattern.search(typeString)
    typeString = typeString[nextRemove.end():]
    nextDate = datePattern.match(typeString)
    if nextDate is not None:
        ownedStartDate = nextDate.group()
    else:
        # get REG DT
        nextRemove = reg_dtPattern.search(typeString)
        typeString = typeString[nextRemove.end():]
        nextDate = datePattern.search(typeString)
        ownedStartDate = nextDate.group()

    yr = year(typeString)
    mak = make(typeString)
    modl = model(typeString)
    styl = style(typeString)
    vin = vinNumber(typeString)

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
    # get zipCode
    nextWord = wordPattern.search(typeString)
    zipCode = nextWord.group().replace(',' , '')
    # check for RNWL RCP entries and replace OWNER entries
    renewalPattern = re.compile('RNWL RCP\s+')
    nextRemove = renewalPattern.search(typeString)
    if nextRemove is not None:
        typeString = typeString[nextRemove.end():]
        # get renewal name and remove
        nextCsv = csvPattern.search(typeString)
        Rname = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get second  owner and remove
        nextCsv = csvPattern.search(typeString)
        Rname2 = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get addr and remove
        nextCsv = csvPattern.search(typeString)
        Raddr = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get addr2 and remove
        #nextCsv = csvPattern.search(typeString)
        #Raddr2 = nextCsv.group().replace(',' , '')
        #typeString = typeString[nextCsv.end():]
        # get city and remove
        nextCsv = csvPattern.search(typeString)
        Rcity = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get state and remove
        nextCsv = csvPattern.search(typeString)
        Rstate = nextCsv.group().replace(',' , '')
        typeString = typeString[nextCsv.end():]
        # get zipCode
        nextWord = wordPattern.search(typeString)
        Rzip = nextWord.group().replace(',' , '')
        # replace renewal information with owner informaton,
        # if the renewal information exists.
        if Rname != '':
            name = Rname
            name2 = Rname2
        if Raddr != '':
            addr = Raddr
            #addr2 = Raddr2
            city = Rcity
            state = Rstate
            zipCode = Rzip
    return [responseType, plate.strip(), name.strip(), addr.strip(), addr2.strip(), city.strip(), state.strip(), zipCode, ownedStartDate,
            '', '', '', yr, mak, modl, styl, vin]

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
    state, zipCode = stateAndZip.group().split()
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
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zipCode, '', '', '' , '','','','','','']

def parsePermit(responseType, typeString):
    # find header and remove
    permitHeaderPattern = re.compile(r'(ONE TRIP PERMIT:|30 DAY [\w ]*PERMIT:|144-HOUR PERMIT:)\s+')
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
    if found is not None:
        state, zipCode = found.group().split()
        city = typeString[:found.start()]
    # if addr2 line is city, state, zip
    else:
        found = stateAndZipPattern.search(addr2)
        if found is not None:
            state, zipCode = found.group().split()
            city = addr2[:found.start()]
    #get year make style vin  '(\d{4})\s+(\w+)\s+([\d\w]{2,})'
    yearMakeStylePattern = re.compile('(\d{4})\s+(\w+)\s+([\d\w]{2,})')
    found = yearMakeStylePattern.search(typeString)
    if found:
        yr = found.group(1)
        mak = found.group(2)
        styl = found.group(3)
    vin = vinNumber(typeString)
    #TODO interpret the make and model and  style ?

    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state, zipCode, '', '', '', issued,\
             yr, mak, '', styl, vin]

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

    yr = year(typeString)
    #yr = ''
    mak = make(typeString)
    #mak = ''
    modl = model(typeString)
    #modl = ''
    styl = style(typeString)
    #styl = ''
    vin = vinNumber(typeString)
    #vin = ''

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
    zipCode = nextWord.group()
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zipCode, '', startDate, endDate,
            '',yr, mak, modl, styl, vin]

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
    if found is not None:
        state, zipCode = found.group().split()
        city = typeString[:found.start()]
    # if addr2 line is city, state, zip
    else:
        found = stateAndZipPattern.search(addr2)
        if found is not None:
            state, zipCode = found.group().split()
            city = addr2[:found.start()]
    return [responseType, plate.strip(), name.strip(), addr.strip(), '', city.strip(), state.strip(), zipCode, '', '', '', '' ,'','','','','']

    #CANCELED
def parseCanceled(responseType, typeString):
    #save the plate
    plateCanceledPattern = re.compile(r'(\w+)[ ]*CANCEL')
    found = plateCanceledPattern.search(typeString)
    plate = found.group(1)
    # pass to parseStandard, since the format is the same
    parsedList = parseStandard(responseType, typeString)
    parsedList[1] = plate.strip() # replace the "standard" plate with the canceled !!!the dates must be compared!!!
    return parsedList


def query(driver, delay, plate):
    # the input field is uniquely defined by the MANDATORY class attributes
    # class="v-textfield v-widget v-has-width iw-child v-textfield-iw-child iw-mandatory v-textfield-iw-mandatory"
    plateSubmitLocator = (By.XPATH, '//input[contains(@class,"v-textfield-iw-mandatory")]')
    plateSubmitElement = findElementOnPage(driver, delay, plateSubmitLocator)

    if plateSubmitElement is None:
        print("TxDot_LIB:query: plate submission FORM not found on page")
        return (None, None)
    plateSubmitElement.clear()
    plateSubmitElement.send_keys(plate)
    plateSubmitElement.send_keys('\n')

    elemLocator =  (By.XPATH, '//div[@style="font-family: Courier New;"]')
    # wait until an lp match is found
    ambiguousPattern = permutationPattern(plate)
    try:
        while True:
            try:
                textElement = findElementOnPage(driver, delay, elemLocator)
                uText = textElement.text
            except StaleElementReferenceException:
                continue
            found = ambiguousPattern.search(uText)
            if found is not None:
                correctPlate = found.group()
                break
            continue
    except TimeoutException:
        print("TxDot_LIB:query:ERROR: Timeout, input licence plate may not match the record.")
        return (None, None)
    plateSubmitElement.clear() # does this need to be cleared ? TODO
    return (str(uText.encode('ascii', 'ignore')), correctPlate.encode('ascii', 'ignore'))#  TEST  TODO


def removeCommas(stringValue):
    """
    Remove commas from a string.
    """
    return stringValue.replace(',' , '')


def repairLineBreaks(fileString):
    # broken keywords words have a pattern of
    # partial-word, newline(\n) white-space, partial word, identifier(, . -)

    # broken ZipPlus numbers have a pattern of
    # five-numbers, dash(-), [white space], [return(\r)], newline(\n), [white-space], partial-number or
    # partial-number, [white space], [return(\r)], newline(\n), [white-space], partial-number, dash(-), four-numbers

    # broken address lines ?  TODO

    wordBreakPattern = re.compile(r'[A-Z]+ *\n\s+[A-Z]+(,|\.|-)',re.MULTILINE) # find broken words
    while True:
        broken = wordBreakPattern.search(fileString)
        if broken is not None:
            #print('TxDot_LIB:repairLineBreaks:words:' , broken.group()) # debug
            fileStringBegin = fileString[:broken.start()]
            fileStringMiddle = broken.group()
            fileStringMiddle = fileStringMiddle.replace('\n', '')
            fileStringMiddle = fileStringMiddle.replace(' ', '')
            fileStringEnd = fileString[broken.end():]
            fileString = fileStringBegin + fileStringMiddle + fileStringEnd
            #print('TxDot_LIB:repairLineBreaks:words:' , fileStringMiddle) # debug
        else:
            break

    numberBreakPattern = re.compile(r',\d{1,4}\s*\n\s*\d{1,4}',re.MULTILINE) # find broken Zip
    # total of 5 digits around a line break?
    while True:
        broken = numberBreakPattern.search(fileString)
        if broken is not None:
            #print('TxDot_LIB:repairLineBreaks:number:' , broken.group()) # debug
            fileStringBegin = fileString[:broken.start()]
            fileStringMiddle = broken.group()
            fileStringMiddle = fileStringMiddle.replace('\n', '')
            fileStringMiddle = fileStringMiddle.replace(' ', '')
            fileStringEnd = fileString[broken.end():]
            ##if re.search(zipPlusPattern, fileStringMiddle) is not None:
            fileString = fileStringBegin + fileStringMiddle + fileStringEnd
            #if re.search(zipCodePattern, fileString) is not None: #debug
            #    print('TxDot_LIB:repairLineBreaks:number:', fileStringMiddle) # debug
        else:
            break
    #print 'TxDot_LIB:repairLineBreaks:\n' + fileString # debug
    return fileString


def style(stringText):
    stylPattern = re.compile('(?<=STYL:)\w+')
    styl = stylPattern.search(stringText)
    if styl:
        return styl.group()
    return ""


def timeout():
    print("TxDotQuery: timeout!")
    quit()


def vinNumber(stringText):
    vinPattern = re.compile('(?<=VIN: )\w+')
    vin = vinPattern.search(stringText)
    if vin:
        return vin.group()
    return ""


def year(stringText):
    yrPattern = re.compile('(?<=YR:)\d{4}')
    yr = yrPattern.search(stringText)
    if yr:
        return yr.group()
    return ""

if __name__ == "__main__":
    print("TxDot_LIB: TESTING TxDot_LIB")

    '''
    # TEST 'repairLineBreaks()
    with open('temp.txt', 'r') as infile:
        raw = infile.readline()
        #csv.reader(substr())
        platesCsv = csv.reader(infile.readline())
        lpList = [plate for plate in platesCsv]
        text = infile.read()
        print(text)
        text = repairLineBreaks(text)
        print(text)
        for lp in lpList:
            result = findResponseType(lp, text)
            if result is not None: print(result[0])
    '''

    # test findAmbiguousPlates

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

    assert("abcd") == removeCommas("a,b,c,d,")
    assert("a,b,c,d,") == insertCommas("abcd")
    assert("name one,name two,addr,apt," == csvStringFromList(["name, one", "name, two", "addr", "apt"]))

