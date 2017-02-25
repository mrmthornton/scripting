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


class ExtractXML():
    def __init__(self, startText, rootElementName, file):
        self.start = startText
        self.stop = "</" + rootElementName
        self.filename = file

    def extract(self):
        try:
            with open(filename) as xmlFile:
                while xmlFile.readline() != self.start:
                    continue
                while xmlFile.readline() != self.stop:
				    print(line)
        except:
            println("file not found")



import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile")
    args = parser.parse_args()
    filename = args.inputFile
    xml = ExtractXML("USCTbankruptcynotice", "ebn:EBNBatch", filename)
    xml.extract()
