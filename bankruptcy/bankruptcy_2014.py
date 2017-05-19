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


import csv
import io
from os import path
import re


"""
def dbDictInit():
    return {
    "Record Type":'',
    "Filing Date":'',
	"bad Bankruptcy Filing Date":'',
    "341 Date":'',
    "bad 341 Date":'',
    "CaseDocketID":'',
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


def dbDictFill(aList):
    return {
    "RecordType":aList[0],
    "FilingDate":aList[1],
	"longBankruptcyFilingDate":aList[2],
    "341Date":aList[3],
    "long341Date":aList[4],
    "CaseNumber":aList[5][:7], # only (nn-nnnnn)
    "Chapter":aList[6],
    "PrimaryGivenName":aList[7],
    "PrimaryMiddleName":aList[8],
    "PrimarySurName":aList[9],
    "PrimarySuffix":aList[10],
    "PrimaryAlias":aList[11],
    "PrimaryAliasAlternateName":aList[12],
    "SecondaryGivenName":aList[13],
    "SecondaryMiddleName":aList[14],
	"SecondarySurName":aList[15],
    "SecondarySuffix":aList[16],
    "SecondaryAlias":aList[17],
    "SecondaryAliasAlternateName":aList[18],
    "PrimaryAddressLine1":aList[19],
    "PrimaryAddressLine2":aList[20],
    "PrimaryAddressCity":aList[21],
    "PrimaryAddressState":aList[22],
    "PrimaryAddressZipCode":aList[23],
    "LawFirmName":aList[24],
    "AttorneyName":aList[25],
    "AttorneyPhone Number":aList[26],
    "AttorneyAddressLine1":aList[27],
    "AttorneyAddressLine2":aList[28],
    "AttorneyAddressCity":aList[29],
    "AttorneyAddressState":aList[30],
    "AttorneyAddressZipCode":aList[31],
    "AccountNumber":aList[32],
    "BankruptcyCourtName":aList[33],
    "CourtPhoneNumber":aList[34],
    "CourtAddressLine1":aList[35],
    "CourtAddressLine2":aList[36],
    "CourtAddressCity":aList[37],
    "CourtAddressState":aList[38],
    "CourtAddressZipCode":aList[39],
    "CourtDistrict":aList[40],
    }


def main():

    with open('bankruptcy_2014.csv', 'r') as infile, \
         open('bankruptcy_2014.txt', 'a') as outfile, \
         open('processed.txt', 'a') as donefile:

        # start with a clean ouput file
        outfile.truncate()
        # read all the input file into a list
        rows = [r for r in csv.reader(infile)]
        if rows[0][0] == 'Record Type':
            rows = rows[1:] # skip the header

        # process each row, and mark it as done
        for row in rows:
            if row[0] == 'PROCESSED': continue # skip rows already done
            d = dbDictFill(row)
            for k,v in d.items():
                print(k,v)





            row[0] = 'PROCESSED'  # mark as done
            outfile.write("")
            outfile.flush()
    print "main: Finished."

if __name__ == '__main__':
    main()
