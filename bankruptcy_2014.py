# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        bankruptcy_2014.py
# Purpose:     get values from the CSV sheet, one row at a time,
#              check bankruptcy database for existing case#-name combination
#              for each VID, excuse and comment as appropriate
#
# Author:      mthornton
#
# Created:     2017MAY17
# Updates:     2017MAY17
# Copyright:   (c) m. thornton 2017
#-------------------------------------------------------------------------------

import re
import io
import csv
#import string

# stringValue = stringValue.replace(',' , '') # remove any commas


def dbDictInit():
    return {
    "Record Type":'',
    "Filing Date":'',
	"bad Bankruptcy Filing Date":'',
    "341 Date":'',
    "bad 341 Date":'',
    "Case":'',
    "Chapter":'',
    "Primary First Name":'',
    "Primary Middle Name":'',
    "Primary Last Name":'',
    "Primary Suffix":'',
    "Primary First AKA":'',
    "Primary Second AKA":'',
    "Secondary First Name":'',
    "Secondary Middle Name":'',
	"Secondary Last Name":'',
    "Secondary Suffix":'',
    "Secondary First AKA":'',
    "Secondary Second AKA":'',
    "Primary Address Line 1":'',
    "Primary Address Line 2":'',
    "Primary Address City":'',
    "Primary Address State":'',
    "Primary Address Zip Code and extension":'',
    "Law Firm Name":'',
    "Attorney Name":'',
    "Attorney Phone Number":'',
    "Attorney Address Line 1":'',
    "Attorney Address Line 2":'',
    "Attorney Address City":'',
    "Attorney Address State Postal Code":'',
    "Attorney Address Zip Code and extension":'',
    "Account Number or Client Unique ID":'',
    "Bankruptcy Court Name":'',
    "Court Phone Number":'',
    "Court Address Line 1":'',
    "Court Address Line 2":'',
    "Court Address City":'',
    "Court Address State Postal Code":'',
    "Court Address Zip Code and extension":'',
    "Court District":'',
    }


def dbDictFill(aList):
    return {
    "Record Type":aList[0],
    "Filing Date":aList[1],
	"bad Bankruptcy Filing Date":aList[2],
    "341 Date":aList[3],
    "bad 341 Date":aList[4],
    "Case":aList[5],
    "Chapter":aList[6],
    "Primary First Name":aList[7],
    "Primary Middle Name":aList[8],
    "Primary Last Name":aList[9],
    "Primary Suffix":aList[10],
    "Primary First AKA":aList[11],
    "Primary Second AKA":aList[12],
    "Secondary First Name":aList[13],
    "Secondary Middle Name":aList[14],
	"Secondary Last Name":aList[15],
    "Secondary Suffix":aList[16],
    "Secondary First AKA":aList[17],
    "Secondary Second AKA":aList[18],
    "Primary Address Line 1":aList[19],
    "Primary Address Line 2":aList[20],
    "Primary Address City":aList[21],
    "Primary Address State":aList[22],
    "Primary Address Zip Code and extension":aList[23],
    "Law Firm Name":aList[24],
    "Attorney Name":aList[25],
    "Attorney Phone Number":aList[26],
    "Attorney Address Line 1":aList[27],
    "Attorney Address Line 2":aList[28],
    "Attorney Address City":aList[29],
    "Attorney Address State Postal Code":aList[30],
    "Attorney Address Zip Code and extension":aList[31],
    "Account Number or Client Unique ID":aList[32],
    "Bankruptcy Court Name":aList[33],
    "Court Phone Number":aList[34],
    "Court Address Line 1":aList[35],
    "Court Address Line 2":aList[36],
    "Court Address City":aList[37],
    "Court Address State Postal Code":aList[38],
    "Court Address Zip Code and extension":aList[39],
    "Court District":aList[40],
    }


"""
def dbDictFill(aDict, aList):
    return {
    "Record Type":'',
    "Filing Date":'',
	"bad Bankruptcy Filing Date":'',
    "341 Date":'',
    "bad 341 Date":'',
    "Case":'',
    "Chapter":'',
    "Primary First Name":'',
    "Primary Middle Name":'',
    "Primary Last Name":'',
    "Primary Suffix":'',
    "Primary First AKA":'',
    "Primary Second AKA":'',
    "Secondary First Name":'',
    "Secondary Middle Name":'',
	"Secondary Last Name":'',
    "Secondary Suffix":'',
    "Secondary First AKA":'',
    "Secondary Second AKA":'',
    "Primary Address Line 1":'',
    "Primary Address Line 2":'',
    "Primary Address City":'',
    "Primary Address State":'',
    "Primary Address Zip Code and extension":'',
    "Law Firm Name":'',
    "Attorney Name":'',
    "Attorney Phone Number":'',
    "Attorney Address Line 1":'',
    "Attorney Address Line 2":'',
    "Attorney Address City":'',
    "Attorney Address State Postal Code":'',
    "Attorney Address Zip Code and extension":'',
    "Account Number or Client Unique ID":'',
    "Bankruptcy Court Name":'',
    "Court Phone Number":'',
    "Court Address Line 1":'',
    "Court Address Line 2":'',
    "Court Address City":'',
    "Court Address State Postal Code":'',
    "Court Address Zip Code and extension":'',
    "Court District":'',
    }
"""


def main():

    with open('bankruptcy_2014.csv', 'r') as infile, open('bankruptcy_2014.txt', 'a') as outfile:
        outfile.truncate()
        csvInput = csv.reader(infile)

        for row in csvInput:
            d = dbDictFill(row)
            for k,v in d.items:
                print(k,v)

            outfile.write(nameString + plateStrings)
            outfile.flush()
    print "main: Finished parsing TxDot file."

if __name__ == '__main__':
    main()
