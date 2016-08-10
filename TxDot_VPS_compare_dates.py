#-------------------------------------------------------------------------------
# Name:        TxDot_VPS_compare_dates
# Purpose:     gather date ranges from TX-DMV, RTS database
#
# Author:      mthornton
#
# Created:     2016 JUL 25
# Updates:     2016 AUG 8
# Copyright:   (c) mthornton 2016
# input - 'temp_plates.csv'
# output - 'compare_dates.csv'
#-------------------------------------------------------------------------------

import re
import io
import csv
import string

from TxDot_LIB import *
from VPS_LP_Change import vps_body, violationSearch

def txdot_body(driver, delay, plate, outfile, rawTextFile):
    results = query(driver, delay, plate)
    if results is not None:
        print results # for debug
        rawTextFile.write(results)
        rawTextFile.write('\n\n------------------------------------\n\n')
        fileString = repairLineBreaks(results)
    foundCurrentPlate = False
    while True: # loop while there is more lp info sections
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
            #print 'main:', responseType, startNum, endNum # for debug
            typeString = fileString[startNum:endNum + 1]
            #print typeString # for debug
            fileString = fileString[:startNum] + fileString[endNum + 1:]
            listData = parseRecord(responseType, typeString)
            csvString = csvStringFromList(listData)
            outfile.write(csvString)
            return csvString

def credentials():
    # Go to the main web page and wait while the user enters credentials
    url = 'https://mvinet.txdmv.gov'
    driver.get(url)

def txdotGetRecord(driver, parameters):
    delay = parameters['delay']
    startPageTextLocator = (By.XPATH, '//TD/H1[contains(text(),"Violation Search")]')
    # pause on next line for entry of credentials, and window navigation.
    startWindow = findTargetPage(driver, findStartWindowDelay, startPageTextLocator)
    if startWindow is None:
        print "Start Page not found."
        return None
    with open(parameters['dataInFileName'], 'r') as infile, open(parameters['dataOutFileName'], 'a') as outfile:
        outfile.truncate()
        csvInput = csv.reader(infile)
        for row in csvInput:
            rawString = row[0]
            if rawString == "" or rawString == 0:  #end when first input does not exist
                break
            plateString = cleanUpString(rawString)
            rawString = row[1]
            if rawString == "" or rawString == 0:  #end when second input does not exist
                break
            replacementString = cleanUpString(rawString)

            #select from Violation Status menu
            menuLocator = (By.XPATH, '//select[@name="P_L_VST_VIOL_STATUS_DESCR"]')
            menuElement = findElementOnPage(driver, delay, menuLocator)
            Selector = Select(menuElement)
            count = 0
            while Selector is None:  # menu select is sometimes None, why ?
                count = count + 1
                print "retrying excusal menu selection. Count: ", count
                Selector = Select(menuElement)
            Selector.select_by_visible_text("ZipCash; Uninvoiced") # does this need to be instanciated each time?

            element = findElementOnPage(driver, delay, parameters['inputLpLocator'])
            submitted = fillFormAndSubmit(driver, startWindow, element, plateString, parameters) # why so slow?
            time.sleep(1)  #page may not be there yet!  how long to wait?
            pageLoaded = newPageElementFound(driver, delay, (By.XPATH, '//frame[@name="fraTOP"]'), parameters['pageLocator2'])

            #while there is a violation to correct
            while True:
                foundFrame = findAndSelectFrame(driver, delay, "fraRL")
                #time.sleep(1)  #text may not be there yet!  how long to wait?
                text = getTextResults(driver, delay, plateString, parameters, "fraRL")
                if text is not None and text != 0: # there's more to correct
                    #click on the first record
                    element = findElementOnPage(driver, delay, parameters['LpLocator'])
                    element.click()
                    #change the value
                    handle = driver.current_window_handle
                    driver.switch_to_window(handle)
                    foundFrame = findAndSelectFrame(driver, delay, "fraVF")
                    element = findElementOnPage(driver, delay, parameters['inputLpLocator'])
                    submitted = fillFormAndSubmit(driver, startWindow, element, replacementString, parameters)
                    #loop
                    time.sleep(1)  #page may not be there yet!  how long to wait?
                    handle = driver.current_window_handle
                    driver.switch_to_window(handle)
                    continue
                break
            handle = driver.current_window_handle
            driver.switch_to_window(handle)
            foundFrame = findAndSelectFrame(driver, delay, "fraRL")
            clicked = findAndClickButton(driver, delay, parameters)

                # click the query button.
            #test with multiple plate changes

    print "main: Finished with LP_correction file."

if __name__ == '__main__':
    print "Login to TX DMV RTS database, navigate to INQUIRY-SINGLE PLATE"
    print "Login to VPS, navigate to VIOLATION SEARCH"
    delay = 5
    driver = webdriver.Ie()
    url = 'https://mvinet.txdmv.gov'
    driver.get(url)

    #workbook = xlrd.open_workbook('plates.xlsx')
    #sheet = workbook.sheet_by_index(0)
    #data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    #read the input file
    with open('temp_plates.csv', 'r') as plateFile:
        csvInput = csv.reader(plateFile)
        plates = [row[0] for row in csvInput]

    #open the output file(s)
    with open('compare_dates.csv', 'a') as outfile, open('txdotText.txt', 'a') as rawTextFile:
        outfile.truncate()
        rawTextFile.truncate()

        #process the input
        for lp in plates:
            # NEED a common data structure for these types of data: txdot , vps, database
            # dictionary ?
            txdot_info_csv = txdotGetRecord(driver, delay, lp, outfile, rawTextFile) #TXDOT PROCESSING
            violationSearch()
            vps_info = vps_body(driver,delay, lp) #VPS PROCESSING
            #db_body(driver, delay, lp) #DATABASE PROCESSING
        outfile.write('----------------\n')
        outfile.flush()
    print "main: Finished with input file."
