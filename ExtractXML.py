# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        ExtractXML.py
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
                extracted = []
                #while stop not in xmlFile.readline():
                #    sys.stdout.write(line)
                #    extracted.append(line)
                while True:
                    line = xmlFile.readline()
                    sys.stdout.write(line)
                    extracted.append(line)
                    if stop in line:
                        break
                return extracted
        except:
            print("file not found")

        sys.stdout.flush()


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile")
    parser.add_argument("outputFile")
    args = parser.parse_args()

    xml = extractXML("USCTbankruptcynotice", "</ebn:EBNBatch", args.inputFile)
    with open(args.outputFile, 'w') as outfile:
        outfile.writelines(xml)
