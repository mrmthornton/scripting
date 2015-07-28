#-------------------------------------------------------------------------------

import re
import io
import csv
import string

# stringValue = stringValue.replace(',' , '') # remove any commas

def main():

    with open('siftCSV.csv', 'r') as infile, open('siftDATA.txt', 'a') as outfile:
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
