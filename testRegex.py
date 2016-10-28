#-------------------------------------------------------------------------------
# Name:        testRegex.py
# Purpose:     test some regex patterns which are userful for correcting
#              multi-line broken words and numbers
#
# Author:      mthornton
#
# Created:     2016 OCT 19
# modified     2016 OCT 21
# Copyright:   (c) mthornton 2016
#-------------------------------------------------------------------------------
import re
from TxDot_LIB import *
import string

linePattern = re.compile('^.+')
wordPattern = re.compile('\w+')
csvPattern = re.compile('[A-Z0-9 .#&]*,')
commaToEOLpattern = re.compile(',[A-Z0-9 .#&]+$')
LICpattern = re.compile('^LIC ')
issuedPattern = re.compile('ISSUED ')
reg_dtPattern = re.compile('REG DT ')
datePattern = re.compile('[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}') # mo/day/year
dateYearFirstPattern = re.compile(r'\d{4,4}/\d{2,2}/\d{2,2}') # year/mo/day


def main():

# faux information

    badWord = """
SELECTION REQUEST: TEMPORARY TAG  00Y0000

TEMPORARY TAG:    00Y0000   VALID:2016/05/21 00:00:00--2016/05/27 00:00:00
YR:2016 MAK:GMC                 GMC                      STYL:4D
VIN: 12345678901234567   COLOR: WHITE

DEALER TEMPORARY TAG - VEHICLE
NAME:     myBUICK GMC,00000 GULFCOAST FWY,SOMEPLACE,T
          X,5555-4444
"""

    badNum = """
SELECTION REQUEST: TEMPORARY TAG  22N4444

TEMPORARY TAG:    22N4444   VALID:2015/11/11 00:00:00--2015/11/13 00:00:00
YR:2016 MAK:RAM                 RAM                      STYL:4D
VIN: 12345678901234567   COLOR: WHITE

DEALER TEMPORARY TAG - VEHICLE
NAME:     CHRYSLER Company,1000000 W PLANO PKWY,SOMEPLACE,TX,5
          5555-4444
"""
    fixed =  repairLineBreaks(badNum)
    print fixed
    fixed =  repairLineBreaks(badWord)
    print fixed

if __name__ == '__main__':
    main()
