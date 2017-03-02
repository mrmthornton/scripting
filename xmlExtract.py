# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        xmlExtract.py
#
# Purpose:     Reads a PDF file line by line until "start" text is found.
#              Prints each subsequent line until the "stop" text is found.
#
# Author:      mthornton, based on ExtractXML.java by satchwinston BAE Systems
#
# Created:     2017 FEB 22
# Update:      2017 MAR 01
# Copyright:   (c) mthornton 2017
#-------------------------------------------------------------------------------

import sys

def extractXML(start, stop, filename):
        try:
            with open(filename) as xmlFile:
                while start not in xmlFile.readline():
                    continue
                allLines = [line for line in xmlFile.readlines()]
                extracted = allLines[:allLines.index(stop) + 1]
                return extracted
        except ValueError:
            print("can't find %s" %stop)


import argparse

if __name__ == "__main__":
    # get two arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile")
    parser.add_argument("outputFile")
    args = parser.parse_args()

    # extract just the xml from the pdf file
    xml = extractXML("USCTbankruptcynotice", "</ebn:EBNBatch>\n", args.inputFile)
    # write the xml to a file
    with open(args.outputFile, 'w') as outfile:
        outfile.writelines(xml)
    #for line in xml:
    #    sys.stdout.write(line)
    #sys.stdout.flush()



