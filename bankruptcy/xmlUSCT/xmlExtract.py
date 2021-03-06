# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        xmlExtract.py
#
# Purpose:     Reads a file with embedded xml, by line until "start" pattern.
#              Prints each subsequent line until the "stop" pattern.
#
# Author:      mthornton
#
# Created:     2017 FEB 22
# Update:      2017 MAR 11
# Copyright:   (c) mthornton 2017
#-------------------------------------------------------------------------------

import sys

#  file --> XML
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
    #  cmd --> args
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help='show results on stdout', action="store_true")
    parser.add_argument("inputFile")
    parser.add_argument("outputFile")
    args = parser.parse_args()

    #  PDF --> XML
    xml = extractXML("USCTbankruptcynotice", "</ebn:EBNBatch>\n", args.inputFile)
    ##xml = extractXML2("USCTbankruptcynotice", "</ebn:EBNBatch>\n", args.inputFile)
    
    #  XML --> file
    with open(args.outputFile, 'w') as outfile:
        outfile.writelines(xml)
        
    #  XML --> print()
    if args.verbose: #add argument to print
        for line in xml:
            sys.stdout.write(line)
        sys.stdout.flush()



