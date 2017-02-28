# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        TxDotTestQuery.py
#
# Purpose: *	Reads a PDF file line by line until reaches a specified "start text".
#               Then prints	each subsequent line until the specifed root element name closing tag is reached.
#
# Author:      mthornton, based on ExtractXML.java by satchwinston BAE Systems
#
# Created:     2017 FEB 22
# Update:
# Copyright:   (c) mthornton 2017
#-------------------------------------------------------------------------------

import sys

class ExtractXML():
    def __init__(self, startText, rootElementName, file):
        self.start = startText
        self.stop = "</" + rootElementName
        self.filename = file

    def extract(self):
        try:
            with open(filename) as xmlFile, open("./tempfile",'w') as outfile:
                while self.start in xmlFile.readline():
                    break
                while True:
                    line = xmlFile.readline()
                    sys.stdout.write(line)
                    outfile.write(line)
                    if self.stop in line:
                        break
        except:
            print("file not found")

        sys.stdout.flush()
        #outfile.flush()
        outfile.close()


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile")
    args = parser.parse_args()
    filename = args.inputFile
    xml = ExtractXML("USCTbankruptcynotice", "ebn:EBNBatch", filename)
    #xml = ExtractXML("USCTbankruptcynotice", "ebn", filename)
    xml.extract()
