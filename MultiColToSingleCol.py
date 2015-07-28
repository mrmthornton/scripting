#-------------------------------------------------------------------------------
# Name:        MultiColToSingle.py
# Purpose:     get a name from column 1 and multiple plates from column 2,
#              create a new spreadsheet with a single column,
#              where each name is followed by the associated  plates.
#              save to text file, in CSV format.
# Author:      mthornton
#
# Created:     2015jul27
# Updates:     2015jul28
# Copyright:   (c) michael thornton 2015
#-------------------------------------------------------------------------------

import re
import io
import csv
import string

# stringValue = stringValue.replace(',' , '') # remove any commas

def main():

    with open('scrubONE.csv', 'r') as infile, open('scrubDATAcsv.txt', 'a') as outfile:
        outfile.truncate()
        csvInput = csv.reader(infile)
        for row in csvInput:
            nameString = '"' + row[0] +'"\n'
            plateStrings = row[1] + '\n'
            plateStrings = plateStrings.replace(' ' , '') # remove any spaces
            plateStrings = plateStrings.replace('"' , '') # remove any quotes
            plateStrings = plateStrings.replace('\t' , '') # remove any tabs
            plateStrings = plateStrings.replace(',' , '\n') # replace , with \n
            for n in range(10):
                plateStrings = plateStrings.replace('\n\n' , '\n') # replace \n\n, with \n
            #plateStrings = plateStrings.replace('\n\n' , '\n') # replace \n\n, with \n
            #plateStrings = plateStrings.replace('\n\n' , '\n') # replace \n\n, with \n
            print nameString, plateStrings

            outfile.write(nameString + plateStrings)
            outfile.flush()
    print "main: Finished parsing TxDot file."

if __name__ == '__main__':
    main()
