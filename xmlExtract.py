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
                allLines = [line for line in xmlFile.readlines()] # side effect of previous line pointer retained
                print len(allLines)
                extracted = allLines[:allLines.index(stop) + 1]
                return extracted
        except ValueError:
            print("can't find %s" %stop)

def extractXML2(start, stop, filename):
        try:
            f = open(filename)
            allLines = f.readlines()
            f.close()
            print len(allLines)
            pass
        except ValueError:
            print("can't find %s" %stop)


import argparse

if __name__ == "__main__":
    #  CMD --> arg1 arg2
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile")
    parser.add_argument("outputFile")
    args = parser.parse_args()

    #  PDF --> XML
    xml = extractXML("USCTbankruptcynotice", "</ebn:EBNBatch>\n", args.inputFile)
    ##xml = extractXML2("USCTbankruptcynotice", "</ebn:EBNBatch>\n", args.inputFile)
    #  XML --> file
    with open(args.outputFile, 'w') as outfile:
        outfile.writelines(xml)
    #  file --> print()
    ##for line in xml:
    ##    sys.stdout.write(line)
    ##sys.stdout.flush()



