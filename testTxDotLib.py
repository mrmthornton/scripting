#-------------------------------------------------------------------------------
# Name:        testTxDotLib
# Purpose:
#
# Author:      mthornton
#
# Created:     2016 OCT 06
# Modified:    2016 OCT 07
# Copyright:   (c) mthornton 2016
# input(s)     broken.txt
# output(s)    test-output.txt
#------------------------------------------------------------------------------


import csv
#import os
#import datetime
import string
#import tkFileDialog
import tkMessageBox
from Tkinter import *
from TxDot_LIB import *

def waitForUser(msg="enter login credentials"):
    #Wait for user input
    root = Tk()
    tkMessageBox.askokcancel(message=msg)
    root.destroy()

if __name__ == '__main__':
    #create an instance of IE and set some options
    driver = webdriver.Ie()
    delay=10
    url = 'https://mvinet.txdmv.gov'
    driver.get(url)
    waitForUser()

    # read input values
    with open('broken.txt', 'r') as plateFile:
        csvInput = csv.reader(plateFile)
        plates = [row[0] for row in csvInput]

    # loop over input values, writing to  outfile
    with open('test-output.txt', 'a') as outfile, open('txdotText.txt', 'a') as rawTextFile:
        outfile.truncate()
        rawTextFile.truncate()
        for plate in plates:
            results = query(driver, delay, plate)
            if results is not None:
                #print '\n------------------------------------\n' # for debug
                #print results # for debug
                rawTextFile.write(results)
                rawTextFile.write('\n------------------------------------\n')

                fileString = repairLineBreaks(results)

            foundCurrentPlate = False
            while True:
                try:
                    responseType, startNum, endNum = findResponseType(plate, fileString)
                except:
                    responseType = None
                    if foundCurrentPlate == False:
                        print fileString # for debug
                        print "\n", plate, ' Plate/Pattern not found' # for debug
                        print '\n------------------------------------\n' # for debug
                        outfile.write(fileString)
                        outfile.write(',' + plate + ' Plate/Pattern not found\n')
                        rawTextFile.write('\n------------------------------------\n')
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
        rawTextFile.flush()
    print "TxDotToText: Finished writing file."
    driver.close()
    driver.quit()